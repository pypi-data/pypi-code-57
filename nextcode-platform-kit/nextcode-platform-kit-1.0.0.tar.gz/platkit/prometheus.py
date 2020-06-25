from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app=None, path="/metrics/", group_by="url_rule")
