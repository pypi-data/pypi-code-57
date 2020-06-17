from prettytable import PrettyTable, PLAIN_COLUMNS

from sdccli.printer import print_item, print_list


def formats():
    return {
        "scanningImage": _print_image,
        "scanningImageList": _print_images,
        "scanningQueryImage": _print_query,
        "scanningVulnImage": _print_vuln,
        "scanningEvaluationImage": _print_evaluation,
    }


def _print_image(image):
    image["imageId"] = image['image_detail'][0].get('imageId', None)
    image["fulltag"] = [d["fulltag"] for d in image['image_detail']]
    if 'image_content' in image and image['image_content']:
        image_content = image['image_content']
        if 'metadata' in image_content and image_content['metadata']:
            image_content_metadata = image_content['metadata']
            image['dockerfile_mode'] = str(image_content_metadata['dockerfile_mode'])
            image['distro'] = str(image_content_metadata['distro'])
            image['distro_version'] = str(image_content_metadata['distro_version'])
            image['size'] = str(image_content_metadata['image_size'])
            image['arch'] = str(image_content_metadata['arch'])
            image['layer_count'] = str(image_content_metadata['layer_count'])

    keys = ["imageDigest", "imageId", "parentDigest", "analysis_status", "image_type", "fulltag",
            "dockerfile_mode", "distro", "distro_version", "size", "arch", "layer_count", "annotations"]
    print_item(image, keys)


def _print_query(res):
    res, query_type = res
    if not query_type:
        for t in res:
            print("%s: available" % (t,))
        return
    if query_type in ['manifest', 'dockerfile', 'docker_history']:
        try:
            print(res.get('metadata', "").decode('base64'))
        except AttributeError:
            print("No metadata %s" % (query_type,))
        return
    if "content" not in res:
        print("No content")
        return

    content = res["content"]
    keys = {
        'os': ['package', 'version', 'license'],
        'files': ['filename', 'size'],
        'npm': ['package', 'version', 'location'],
        'gem': ['package', 'version', 'location'],
        'python': ['package', 'version', 'location'],
        'java': ['package', 'specification-version', 'implementation-version', 'location']
    }
    if query_type in keys:
        print_list(content, keys[query_type])
    else:
        print_list(content, content[0].keys())


def _print_vuln(res):
    res, query_type = res
    if "vulnerabilities" not in res:
        print("No vulnerabilities")
        return

    vulnerabilities = res["vulnerabilities"]
    if query_type in ['os', 'non-os', 'all']:
        keys = ['vuln', 'package', 'severity', 'fix', 'url']
        print_list(vulnerabilities, keys)
    else:
        print_list(vulnerabilities, vulnerabilities[0].keys())


def _print_images(images):
    header = ['Full Tag', 'Image ID', 'Analysis Status', 'Image Digest']
    t = PrettyTable(header)
    t.set_style(PLAIN_COLUMNS)
    t.align = 'l'

    add_rows = []
    for image_record in images:
        for image_detail in image_record['image_detail']:
            imageId = image_detail.get('imageId', "None")
            fulltag = image_detail.get('registry', "None") + "/" + image_detail.get('repo',
                                                                                    "None") + ":" + image_detail.get(
                'tag', "None")

            row = [fulltag, imageId, image_record['analysis_status'], image_record['imageDigest']]
            if row not in add_rows:
                add_rows.append(row)
    for row in add_rows:
        t.add_row(row)
    print(t.get_string(sortby='Full Tag'))


def _print_evaluation(res):
    evals, detail = res
    for eval_record in evals:
        for imageDigest in list(eval_record.keys()):
            for fulltag in eval_record[imageDigest]:
                if not eval_record[imageDigest][fulltag]:
                    evaldata = {
                        "imageDigest": imageDigest,
                        "fulltag": fulltag,
                        "status": 'no_eval_available'
                    }
                    print_item(evaldata, ["imageDigest", "fulltag", "status"])
                    continue

                for evaldata in eval_record[imageDigest][fulltag]:
                    evaldata["imageDigest"] = imageDigest
                    evaldata['fulltag'] = fulltag
                    evaldetail = evaldata['detail']
                    if detail:
                        evaldata['final_action'] = evaldetail['result'].get('final_action', None)
                        evaldata['final_action_reason'] = evaldetail['result'].get('final_action_reason', None)
                    print_item(evaldata,
                               ["imageDigest", "fulltag", "status", "last_evaluation", "policyId", "final_action",
                                "final_action_reason"])
                    print("")

                    if detail:
                        imageId = evaldetail['result']['image_id']
                        evalresults = evaldetail['result']['result'][imageId]['result']
                        values = []
                        for row in evalresults['rows']:
                            status_detail = row[6]
                            if len(row) > 7 and row[7]:
                                eval_whitelist_detail = row[7]
                                status_detail = "whitelisted(" + eval_whitelist_detail['whitelist_name'] + ")"
                            values.append({
                                'Gate': row[3],
                                'Trigger': row[4],
                                'Detail': row[5],
                                'Status': status_detail
                            })
                        print_list(values, ['Gate', 'Trigger', 'Detail', 'Status'])
