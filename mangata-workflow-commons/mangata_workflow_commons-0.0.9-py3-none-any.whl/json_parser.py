import json
import re
import logging
from typing import Dict, List
import commons.constants as C
from dateutil import tz
import datetime

family_id_list = [56, 52, 59, 61, 60]
traditional_list = [52]
contemporary_list = [56, 59, 61, 60]

family_id_map_dict = {
    56: 1,
    52: 4,
    59: 5,
    61: 6,
    60: 7
}

paper_type_dict = {
    "CreamPearl": 3,
    "IcePearl": 1,
    "Ivory": 4,
    "White": 2,
    "Gold": 5
}

ship_method_dict = {
    "": 0,  # Missing
    "Fixed": 1,  # Free Shipping
    "flatrate_flatrate": 2,
    "Expedited": 3,
    "Overnight": 4
}

_log = logging.getLogger(__name__)


def utc_to_central_dt(date: str):
    """Converts an UTC date string to US Central Time date string, format %Y-%m-%d"""
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/Chicago')
    utc_dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    utc = utc_dt.replace(tzinfo=from_zone)
    central_dt = utc.astimezone(to_zone)
    central = datetime.datetime.strftime(central_dt, '%Y-%m-%d')
    return central


def json_parser(message: Dict) -> List:
    """
    This function takes in a message dict from rabbitmq and returns a list of necessary values for the MySQL database
    :param: dict message
    :return: list of values to update MySQL database
    """
    try:
        items_dict, info_buy_request_dict, request_dict, seqn_list = {}, {}, {}, []
        document_nu, boomi_json, pdat = message[C.DOCUMENT], message[C.BOOMI_JSON], message[C.ENDTIME]
        json_data = json.loads(boomi_json)
        morn_id_json = json_data.get("increment_id")
        firstname = json_data.get("shipping_assignments")[0].get('shipping').get('address').get('firstname')
        lastname = json_data.get("shipping_assignments")[0].get('shipping').get('address').get('lastname')
        full_name = f"{firstname} {lastname}"
        address_1 = json_data.get("shipping_assignments")[0].get('shipping').get('address').get('street')[0]
        try:
            address_2 = json_data.get("shipping_assignments")[0].get('shipping').get('address').get('street')[1]
        except Exception as index_error:
            _log.info('No address 2 found, setting blank default')
            address_2 = ' '
        telp = json_data.get("shipping_assignments")[0].get('shipping').get('address').get('telephone')
        email = json_data.get("shipping_assignments")[0].get('shipping').get('address').get('email')
        city = json_data.get("shipping_assignments")[0].get('shipping').get('address').get('city')
        state = json_data.get("shipping_assignments")[0].get('shipping').get('address').get('region_code')
        zip_code = json_data.get("shipping_assignments")[0].get('shipping').get('address').get('postcode')
        ship_meth = json_data.get("shipping_assignments")[0].get('shipping').get('method', '')
        meth = ship_method_dict[ship_meth]
        cnty = json_data.get("shipping_assignments")[0].get('shipping').get('address').get('country_id')
        odat_created_date = json_data.get("created_at")
        odat = utc_to_central_dt(odat_created_date)
        totl = json_data.get("base_grand_total")
        odis = json_data.get("base_discount_amount")
        cpnc = json_data.get("coupon_code", " ")
        ship = json_data.get("shipping_amount")
        tax = json_data.get("tax_amount")
        proc = 2  # default enum value to set processed to false

        order_items = json_data.get('items', [])
        if order_items:
            order_count = 0
            for order in order_items:
                order_count += 1
                idis = order.get('discount_amount')
                idis = idis if idis < 0 else idis * - 1
                iqua = order.get('qty_ordered')
                pric = order.get('base_price')
                ittl = order.get('base_row_total')
                order_request = order.get('product_option').get('info_buyRequest').get('request', "none")
                if order_request == 'none':
                    _log.info("Order: {}, Item No: {}, no Asset found, pass".format(document_nu, order_count))
                else:
                    vendor_payload = order_request.get('item').get('vendor_payload', 'none')
                    if vendor_payload == 'none':
                        _log.info("Order: {}, Item No {} has no vendor_paload".format(document_nu, order_count))
                    else:
                        sku_json = vendor_payload.get('sku')
                        vendor_project = vendor_payload.get('vendor_project')
                        vendor_project = json.loads(vendor_project)
                        vendor_render_domain = vendor_payload.get('vendor_render_domain')
                        vendor_render_url = vendor_payload.get('vendor_render_url')
                        vendor_tar_path = vendor_render_domain + vendor_render_url
                        guid = vendor_project.get('id')
                        id_no = vendor_project.get('family').get('id')
                        ityp = family_id_map_dict[id_no]
                        dsca = vendor_project.get('family').get('name')
                        attribute_values = vendor_project.get('params')[0].get('attribute_values')
                        workspace_size = vendor_project.get('params')[0].get('workspace').get('name')
                        them = vendor_project.get('params')[0].get('theme').get('name')
                        if id_no in traditional_list:
                            digital_workflow_type = 'traditional'
                        if id_no in contemporary_list:
                            digital_workflow_type = 'contemporary'
                        if 'school' in attribute_values.keys():
                            smi_json = attribute_values['school']
                        elif 'School' in attribute_values.keys():
                            smi_json = attribute_values['School']
                        else:
                            _log.info('missing school or School attribute, entering default 1 for smi')
                            smi_json = 1
                        if (smi_json == '') or (smi_json is None):
                            _log.info('missing smi in school attribute, entering default 1')
                            smi_json = 1
                            rep = "BAL1300"
                        try:
                            if not rep:
                                rep = attribute_values['Rep']
                        except Exception as e:
                            rep = ' '
                        them = them[:13]
                        if them.startswith('SR'):
                            prfx = them[:2]
                            them_tar = them[:7]
                        else:
                            prfx = them[:4]
                            them_tar = them
                        # Separate Small Contemporary Thank You's from Regular Contemporary, set to 8 instead of 7
                        if id_no == 60 and prfx == 'THYS':
                            ityp = 8
                        qnty = attribute_values['Quantity']
                        if re.match('Pack of', qnty):
                            qnty = qnty.replace('Pack of ', '')
                        try:
                            paper_type_name = attribute_values['PaperType']
                            ptyp = paper_type_dict[paper_type_name]
                        except Exception:
                            ptyp = 0
                        if digital_workflow_type == 'traditional':
                            srno = them.replace('SR', '')
                            srno = srno[:5]
                            ptyp = 0
                        if digital_workflow_type == 'contemporary':
                            srno = 0

                        refcntd = 0  # These are reserved for Baan Tables, no longer needed
                        refcntu = 0  # These are reserved for Baan Tables, no longer needed

                        tar_data = {'orno': document_nu, 'seqn': order_count, 'them': them_tar, 'prfx': prfx,
                                    'tar_path': vendor_tar_path}

                        order_data = {'orno': document_nu, 'guid': guid, 'item': sku_json, 'idno': str(id_no), 'ityp': ityp,
                                'ptyp': ptyp, 'them': them, 'qnty': int(qnty), 'size': workspace_size, 'morn': morn_id_json,
                                'smin': smi_json, 'srno': int(srno), 'seqn': order_count, 'name': lastname, 'dsca': dsca,
                                "emno": rep, "pdat": pdat, "tar_data": tar_data,
                                'nama': full_name, 'namc': address_1, 'namd': address_2, 'city': city, 'state': state,
                                'namf': zip_code, 'cnty': cnty, 'telp': telp, 'email': email, 'odat': odat, 'totl': totl,
                                'ship': ship, 'tax': tax, 'pric': pric, 'ittl': ittl, 'meth': meth, 'odis': odis,
                                'cpnc': cpnc, 'idis': idis, 'iqua': iqua,
                                # remove for mysql
                                'refcntd': refcntd, 'refcntu': refcntu, 'proc': proc
                                }

                        seqn_list.append(order_data)

            return seqn_list

    except Exception as e:
        _log.exception(e)












