import sys

import click

import sdccli.usecases.dashboard.panel as use_case


@click.group(name='panel', short_help='Sysdig Monitor Dashboard Panel operations')
def panel():
    pass


@panel.command(name='list', short_help="List all the panels in a dashboard")
@click.argument('dashboard', nargs=1)
@click.pass_obj
def list_panels(cnf, dashboard):
    try:
        panels = use_case.get_panels_from_dashboard(cnf.sdmonitor, dashboard)
        cnf.formatter.format(panels, "panelList")
    except Exception as ex:
        print(f"Error: {str(ex)}")
        sys.exit(1)


@panel.command(name='get', short_help="Get the info from a panel")
@click.argument('dashboard', nargs=1, type=click.INT)
@click.argument('panel', nargs=1, type=click.INT)
@click.pass_obj
def get(cnf, dashboard, panel):
    try:
        panels = use_case.get_panels_from_dashboard(cnf.sdmonitor, dashboard)
        panel_list = [p for p in panels if p["id"] == panel]
        if len(panel_list) == 0:
            raise Exception(f"panel with id {panel} not found in dashboard {dashboard}")

        cnf.formatter.format(panel_list[0], "panel")
    except Exception as ex:
        print(f"Error: {str(ex)}")
        sys.exit(1)


@panel.command(name='add', short_help="Add panel")
@click.argument('dashboard', nargs=1, type=click.INT)
@click.argument('name', nargs=1)
@click.argument('type', nargs=1)
@click.argument('query', nargs=1)
@click.pass_obj
def add(cnf, dashboard, name, type, query):
    valid_types = {
        "timechart": use_case.PANEL_VISUALIZATION_TIMECHART,
        "number": use_case.PANEL_VISUALIZATION_NUMBER,
    }
    type = type.lower()
    if type not in valid_types:
        print(f"Type {type} is not valid, valid types are: {' '.join(valid_types.keys())}")

    try:
        panel = use_case.create_panel_in_dashboard(cnf.sdmonitor, dashboard, name, valid_types[type], query)
        cnf.formatter.format(panel, "panel")
    except Exception as ex:
        print(f"Error: {str(ex)}")
        sys.exit(1)


@panel.command(name='del', short_help="Delete a panel from a dashboard")
@click.argument('dashboard', nargs=1, type=click.INT)
@click.argument('panel', nargs=1, type=click.INT)
@click.pass_obj
def delete(cnf, dashboard, panel):
    try:
        use_case.delete_panel_from_dashboard(cnf.sdmonitor, dashboard, panel)
        print("Success")
    except Exception as ex:
        print(f"Error: {str(ex)}")
        sys.exit(1)


@panel.command(name='add_query', short_help="Add query to a panel")
@click.argument('dashboard', nargs=1, type=click.INT)
@click.argument('panel', nargs=1, type=click.INT)
@click.argument('query', nargs=1)
@click.pass_obj
def add_query(cnf, dashboard, panel, query):
    try:
        use_case.add_query_to_panel(cnf.sdmonitor, dashboard, panel, query)
        panel = [p for p in use_case.get_panels_from_dashboard(cnf.sdmonitor, dashboard) if p["id"] == panel][0]
        cnf.formatter.format(panel, "panel")
    except Exception as ex:
        print(f"Error: {str(ex)}")
        sys.exit(1)

@panel.command(name='del_query', short_help="Add query to a panel")
@click.argument('dashboard', nargs=1, type=click.INT)
@click.argument('panel', nargs=1, type=click.INT)
@click.argument('query', nargs=1, type=click.INT)
@click.pass_obj
def add_query(cnf, dashboard, panel, query):
    try:
        use_case.del_query_from_panel(cnf.sdmonitor, dashboard, panel, query)
        panel = [p for p in use_case.get_panels_from_dashboard(cnf.sdmonitor, dashboard) if p["id"] == panel][0]
        cnf.formatter.format(panel, "panel")
    except Exception as ex:
        print(f"Error: {str(ex)}")
        sys.exit(1)

