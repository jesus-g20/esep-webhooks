import json
import os
import urllib.request

def lambda_handler(event, context):
    print("FunctionHandler received:")
    print(json.dumps(event))

    # event already contains the GitHub payload
    # {"action": "opened", "issue": { ... }}
    if "issue" not in event:
        return {
            "statusCode": 400,
            "body": json.dumps("No issue in payload")
        }

    issue_url = event["issue"]["html_url"]

    payload = {
        "text": f"Issue Created: {issue_url}"
    }

    slack_url = os.environ["SLACK_URL"]

    # Send Slack POST request
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        slack_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            resp_body = resp.read().decode("utf-8")
            print("Slack Response:", resp_body)
    except Exception as e:
        print("Slack ERROR:", str(e))

    return {
        "statusCode": 200,
        "body": json.dumps("Webhook received")
    }
