from flask import Blueprint, render_template, request


def make_blueprint(station, url_prefix):
    blueprint = Blueprint(
        "fn_station",
        __name__,
        template_folder="templates",
        static_folder="static/fn_station",
        url_prefix=url_prefix,
    )
    tabs = {}

    def register_tab(title, *, icon="", url=None, provide_search=False):
        slug = title.lower()
        if url is None:
            url = f"/{slug}/"
        tabs[slug] = dict(url=url_prefix + url, title=title, slug=slug, icon=icon)

    register_tab("Composers", icon="project-diagram", url="/", provide_search=True)
    register_tab("Dashboards", icon="tachometer-alt", provide_search=True)
    register_tab("Queries", icon="lightbulb")
    register_tab("API", icon="network-wired")

    @blueprint.context_processor
    def context():
        return dict(tabs=tabs)

    def filter_items(query, tags, item):

        strings = [item.description, item.title]

        match_search = (
            any(
                keyword.casefold() in string.casefold()
                for keyword in query.split()
                for string in strings
            )
            or not query
        )

        match_tags = bool(set(item.tags) & set(tags)) or not tags

        return match_tags and match_search

    def items_list(title, items):
        search = request.args.get("search", "")
        selected_tags = set(request.args.getlist("tags"))
        all_tags = {tag for item in items for tag in item.tags}
        tags = [(tag, tag in selected_tags) for tag in all_tags]

        filtered_items = [
            item for item in items if filter_items(search, selected_tags, item)
        ]

        return render_template(
            "fn_station/items.html",
            title=title,
            items=filtered_items,
            search=search,
            tags=tags,
        )

    @blueprint.route("/")
    @blueprint.route("composers/")
    def composers():
        return items_list("Composers", station.composers.values())

    @blueprint.route("dashboards/")
    def dashboards():
        return items_list("Dashboards", station.dashboards)

    @blueprint.route("api/")
    def api():
        return render_template("fn_station/api.html")

    @blueprint.route("queries/")
    def queries():
        columns = [
            dict(name="id", label="ID", placeholder="filter..."),
            dict(name="composer_name", label="COMPOSER"),
            dict(name="client_id", label="CLIENT ID"),
            dict(name="user", label="USER"),
            dict(name="date", label="TIMESTAMP", type="date"),
        ]
        for column in columns:
            column["value"] = request.args.get(column["name"])

        page = int(request.args.get("page") or 1)

        queries, num_pages = station.query_manager.list_queries(
            page, **{col["name"]: col["value"] for col in columns}
        )
        page = min(page, num_pages)

        return render_template(
            "fn_station/queries.html",
            columns=columns,
            queries=queries,
            page=page,
            num_pages=num_pages,
        )

    return blueprint
