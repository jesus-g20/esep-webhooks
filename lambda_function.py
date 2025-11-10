import json
import os
import urllib.request

def lambda_handler(event, context):
    print("GitHub webhook received event:")
    print(json.dumps(event))

    # Extract issue URL
    try:
        issue_url = event["issue"]["html_url"]
    except Exception as e:
        print("ERROR: Couldn't extract issue URL:", e)
        print("Event received:", json.dumps(event))
        return {"statusCode": 400, "body": "Invalid GitHub issue payload"}

    # Slack message
    payload = {"text": f"Issue Created: {issue_url}"}

    slack_url = os.environ.get("SLACK_URL")
    if not slack_url:
        print("ERROR: SLACK_URL not found in env variables")
        return {"statusCode": 500, "body": "Missing SLACK_URL"}

    print("Sending message to Slack:", payload)

    # Send the POST request
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            slack_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode("utf-8")
            print("Slack Response:", response_body)
    except Exception as e:
        print("Slack ERROR:", str(e))
        return {"statusCode": 500, "body": "Slack send failure"}

    return {"statusCode": 200, "body": "Issue sent to Slack"}
