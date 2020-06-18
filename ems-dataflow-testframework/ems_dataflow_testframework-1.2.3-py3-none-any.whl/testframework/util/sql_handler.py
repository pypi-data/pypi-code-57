import logging


class SqlHandler(object):

    QUERY = "SELECT * FROM `{gcp_project_id}.{dataset_name}.{table_name}` WHERE ({partition_filter}) AND ({filter}) AND ({where})"

    def build_query(self, dynamic_content):
        formatted_query = self.QUERY.format(**dynamic_content)
        logging.debug(formatted_query)

        return formatted_query.strip()
