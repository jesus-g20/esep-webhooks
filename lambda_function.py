import json
import os
import urllib.request

def lambda_handler(event, context):
    # Log the incoming event (for debugging)
    print("GitHub Webhook received:")
    print(json.dumps(event))

    # Extract the issue URL from the GitHub Issues event payload
    try:
        issue_url = event["issue"]["html_url"]
    except Exception as e:
        print("Error extracting issue URL:", e)
        return {
            "statusCode": 400,
            "body": "Invalid GitHub Issues payload"
        }

    # Create Slack message payload
    slack_payload = {
        "text": f"Issue Created: {issue_url}"
    }

    # Get Slack webhook URL from environment variable
    slack_url = os.environ.get("SLACK_URL")

    if not slack_url:
        return {
            "statusCode": 500,
            "body": "SLACK_URL environment variable not set"
        }

    # Convert the payload to JSON
    data = json.dumps(slack_payload).encode("utf-8")

    # Prepare request to send to Slack
    request = urllib.request.Request(
        slack_url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    # Send the request to Slack
    try:
        response = urllib.request.urlopen(request)
        response_body = response.read().decode("utf-8")
        print("Slack response:", response_body)
    except Exception as e:
        print("Error sending to Slack:", e)
        return {
            "statusCode": 500,
            "body": "Failed to send Slack message"
        }

    return {
        "statusCode": 200,
        "body": f"Webhook received, issue sent to Slack: {issue_url}"
    }
