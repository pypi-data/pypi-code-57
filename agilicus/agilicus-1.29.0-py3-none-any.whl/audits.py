from prettytable import PrettyTable

from . import context
from . import input_helpers


def query(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = input_helpers.get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    dt_from = kwargs.pop("dt_from", "now-1day")

    query_results = apiclient.audits_api.list_audits(
        dt_from=dt_from, org_id=org_id, **kwargs
    )

    if query_results:
        return query_results.audits

    return []


def format_audit_list_as_text(audits):
    table = PrettyTable(
        [
            "action",
            "user_id",
            "org_id",
            "source_ip",
            "target_resource_type",
            "target_id",
            "date",
            "trace_id",
        ]
    )
    for record in audits:
        date = "---"
        if record.time:
            date = record.time.strftime("%Y-%m-%d %H:%M:%S %z (%Z)")

        table.add_row(
            [
                record.action,
                record.user_id,
                record.org_id,
                record.source_ip,
                record.target_resource_type,
                record.target_id,
                date,
                record.trace_id,
            ]
        )
    table.align = "l"
    return table
