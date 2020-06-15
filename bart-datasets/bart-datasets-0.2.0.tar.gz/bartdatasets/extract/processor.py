import os
import json
import logging

from datetime import datetime, timedelta
from uuid import uuid4
from bartdatasets.extract.ga_reporting import GoogleAnalyticsReporting

logger = logging.getLogger(__name__)


def extract_by_date_ranger(
    ga_viewId: str,
    ga_credential: str,
    s3_path: str,
    start_date: datetime,
    end_date: datetime,
    loglevel: str = "INFO",
):

    today = datetime.today()

    # CHANGE LOGGER
    level = getattr(logging, loglevel.upper())
    logger = logging.getLogger()
    logger.setLevel(level)

    logger.info("Iniciando o processamento...")
    reporting = GoogleAnalyticsReporting(
        view_id=ga_viewId, credentials_json_dict=json.loads(ga_credential)
    )

    if start_date > end_date:
        raise ValueError("start_date cannot be greater than end_date")
    elif (start_date > today) or (end_date > today):
        raise ValueError("start_date or end_date cannot be in the future")

    days_start = (today - end_date).days or 1
    d_agos = ((end_date - start_date).days or 1) + days_start

    dataset = reporting.extract_data(d_ago=d_agos, start=days_start)

    dataset.to_parquet(os.path.join(s3_path, "ga_pageviews", f"{uuid4()}.parquet"))
    logger.info(f"Processamento Finalizado, dataset gerado {len(dataset)} linhas")

    return 0


def extract_yesterday(ga_viewId: str, ga_credential: str, s3_path: str):

    today = datetime.today()
    return extract_by_date_ranger(
        ga_viewId,
        ga_credential,
        s3_path,
        start_date=today - timedelta(days=1),
        end_date=today,
    )
