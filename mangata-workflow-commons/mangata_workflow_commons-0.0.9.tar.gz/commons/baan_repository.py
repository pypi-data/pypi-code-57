# Copyright (C) 2020 Taylor Publishing Company. All Rights Reserved.
#
# Project:  digital-workflow-handler
# Module:   manage.py
# Created:  2020-04-01

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
import logging
from urllib.parse import quote_plus
from typing import List, Dict, Any, Optional
import datetime


from commons.utils import get_last_two_months_val, get_last_three_months_val
from commons.models import DigitalAnnoucementOrders


class BaanRepository(object):

    def __init__(self, config_file):
        """
        Initializing the class to make sql calls to Baan database

        """
        self._config = config_file
        # Initializing logging
        self._log = logging.getLogger(__name__)

        # Create session
        self._baan_user_name = quote_plus(self._config.USER_NAME)
        self._baan_pass = quote_plus(self._config.USER_PASSWORD)
        self._baan_host = self._config.DB_HOST
        self._baan_port = self._config.DB_PORT
        self._baan_host_db = self._config.DB_NAME
        self._baan_db_uri = f"oracle+cx_oracle://{self._baan_user_name}:{self._baan_pass}@{self._baan_host}:" \
                            f"{self._baan_port}/{self._baan_host_db}"
        self._log.debug(self._baan_db_uri)

        self._engine = create_engine(self._baan_db_uri, pool_recycle=3600)
        Session = sessionmaker(bind=self._engine)
        self._session = Session()

    def get_orders_from_last_two_months(self, date_obj: Optional[datetime.date] = None) -> List[str]:
        """
        SQL query to get the last two months of orders as a list
        :param: optional datetime.date object
        :return: list of orders
        """
        last_two_mo = get_last_two_months_val(date_obj)
        q_orders = self._session.execute(f"select * from triton.ttmxch404100 WHERE T$PDAT >='{last_two_mo}'")
        query_list = [str(row[u't$orno']).strip() for row in q_orders]

        return list(set(query_list))

    def get_orders_from_last_three_months(self, date_obj: Optional[datetime.date] = None) -> List[str]:
        """
        SQL query to get the last three months of orders as a list
        :param: optional datetime.date object
        :return: list of orders
        """
        last_three_mo = get_last_three_months_val(date_obj)
        q_orders = self._session.execute(f"select * from triton.ttmxch404100 WHERE T$PDAT >='{last_three_mo}'")
        query_list = [str(row[u't$orno']).strip() for row in q_orders]

        return list(set(query_list))

    def query_order(self, order_no: int, seqn_no: int) -> Optional[DigitalAnnoucementOrders]:
        """
        SQL query to return first query object
        :param: int order_no
        :param: int seqn_no
        :return: first SQL query object of ttmxch404100 table
        """
        order_obj = self._session.query(DigitalAnnoucementOrders) \
            .filter(DigitalAnnoucementOrders.orno == order_no) \
            .filter(DigitalAnnoucementOrders.seqn == seqn_no) \
            .first()

        return order_obj

    def query_all_orders(self) -> List[DigitalAnnoucementOrders]:
        """
        SQL query to return all query objects of ttmxch404100 table
        :return: list all query objects of ttmxch404100 table
        """
        q_orders = self._session.query(DigitalAnnoucementOrders).all()

        return q_orders

    def add_or_update_orders_json(self, message: Dict) -> None:
        """
        SQL insert or update order to ttmxch404100 table
        :param: dict message
        :return: None
        """
        del message['tar_data']
        order_no = int(message['orno'])
        seqn_no = int(message['seqn'])
        orno_record = self.query_order(order_no, seqn_no)

        if orno_record:
            try:
                orno_id = orno_record.orno
                seqn_no = orno_record.seqn
                self._session.query(DigitalAnnoucementOrders) \
                    .filter(DigitalAnnoucementOrders.orno == orno_id) \
                    .filter(DigitalAnnoucementOrders.seqn == seqn_no) \
                    .update(message)
                self._session.commit()
            except SQLAlchemyError as e:
                self._log.exception(str(e))
        else:
            try:
                self._session.add(DigitalAnnoucementOrders(**message))
                self._session.commit()
            except SQLAlchemyError as e:
                self._log.info(str(e))

        self._log.debug(f"Order number {order_no} is updated")

    def delete_order(self, order_no: int) -> None:
        """
        SQL delete order of ttmxch404100 table
        :param: int order_no
        :return: None
        """
        self._session.query(DigitalAnnoucementOrders) \
            .filter(DigitalAnnoucementOrders.orno == order_no) \
            .delete()
        self._session.commit()
        self._log.info(f"Order number {order_no} is deleted")





























