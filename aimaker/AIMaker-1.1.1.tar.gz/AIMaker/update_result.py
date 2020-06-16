import os
import requests
import json
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

KEY_RESULT_VALUE = "result"

def sendUpdateRequest(result):

    try:
        job = os.environ['AI_MAKER_JOB_ID']
        pod_name = os.environ['HOSTNAME']
        token = os.environ['AI_MAKER_TOKEN']
        url = os.environ['AI_MAKER_HOST']
    except KeyError as e:
        logging.error("[KeyError] Please assign {} value".format(str(e)))
        return "Update result failed, please contact your system administrator"

    HEADERS = {"content-type" : "application/json",
               "Authorization" : "bearer "+token}
    body = json.dumps({ KEY_RESULT_VALUE : result })
    url = url+"/api/v1/ai-maker/callback/results/jobs/"+job+"/pod/"+pod_name

    logging.debug("Headers: {}".format(HEADERS))
    logging.debug("Body: {}".format(body))
    logging.debug("Url: {}".format(url))

    try:
        r = requests.post(url, data = body, headers = HEADERS)
        logging.debug("Reponse: {}".format(r.text))
        r.raise_for_status()
        return "Update result OK"
    except requests.exceptions.HTTPError as errh:
        logging.error("Http Error: {}".format(errh))
    except requests.exceptions.ConnectionError as errc:
        logging.error("Error Connecting: {}".format(errc))
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error: {}".format(errt))
    except requests.exceptions.RequestException as err:
        logging.error("OOps: Something Else {}".format(err))

    return "Update result failed, please contact your system administrator"

def saveValidationResult(result):

    try:
        cronjob = os.environ['AI_MAKER_CRONJOB_ID']
        token = os.environ['AI_MAKER_TOKEN']
        url = os.environ['AI_MAKER_HOST']
    except KeyError as e:
        logging.error("[KeyError] Please assign {} value".format(str(e)))
        return "Update result failed, please contact your system administrator"

    HEADERS = {"content-type" : "application/json",
               "Authorization" : "bearer "+token}
    body = json.dumps({ KEY_RESULT_VALUE : result })
    url = url+"/api/v1/ai-maker/callback/results/validations/"+cronjob

    logging.debug("Headers: {}".format(HEADERS))
    logging.debug("Body: {}".format(body))
    logging.debug("Url: {}".format(url))

    try:
        r = requests.post(url, data = body, headers = HEADERS)
        logging.debug("Reponse: {}".format(r.text))
        r.raise_for_status()
        return "Update result OK"
    except requests.exceptions.HTTPError as errh:
        logging.error("Http Error: {}".format(errh))
    except requests.exceptions.ConnectionError as errc:
        logging.error("Error Connecting: {}".format(errc))
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error: {}".format(errt))
    except requests.exceptions.RequestException as err:
        logging.error("OOps: Something Else {}".format(err))

    return "Update result failed, please contact your system administrator"
