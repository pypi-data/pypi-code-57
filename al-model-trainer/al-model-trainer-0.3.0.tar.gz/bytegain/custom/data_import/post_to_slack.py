import argparse
import getpass
import json
import string

import requests


def create_post(client, log_files):
    attachment = {
        "fallback": "Pipeline run",
        "pretext": "Pipeline run",
        "mrkdwn_in": ["fields"],
    }
    fields = []
    for log_file in log_files:
        label, filename = log_file.split(":", 1)
        with open(filename, "r") as f:
            part = 1
            text = ""
            for line in f:
                line = string.replace(line, "    ", "\t")
                # Slack only allows 2K / attachment field, so break up long files
                if len(text) + len(line) > 1990:
                    fields.append({
                        "title": "%s [part %d]" % (label, part),
                        "value": "```%s```" % text,
                        "short": False})
                    part += 1
                    text = ""
                text = text + line

            title = label if part == 1 else "%s [part %d]" % (label, part)
            fields.append({
                "title": title,
                "value": "```%s```" % text,
                "short": False})

    attachment["fields"] = fields
    post = {"text": "*%s* results from %s" % (client, getpass.getuser()),
            "attachments": [attachment]}
    return post


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Copies and Joins S3 data files to Bytegain S3 storage')
    parser.add_argument('--client', type=str, help='Client name', required=True)
    parser.add_argument('--slack_url', type=str, help='Slack Webhook URL',
                        default="https://hooks.slack.com/services/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")
    parser.add_argument('--log_files', type=str, help='Description:filename of logs to upload', nargs="+",
                        required=True)
    args = parser.parse_args()

    post = create_post(args.client, args.log_files)
    r = requests.post(args.slack_url, data=json.dumps(post))
    print(r.content)
