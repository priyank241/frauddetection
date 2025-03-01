import json
import base64
import urllib3
import boto3
from datetime import datetime

http = urllib3.PoolManager()
sns_client = boto3.client('sns')
s3_client = boto3.client('s3')

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:975049960469:fraud-alerts-topic"  # Replace with your SNS topic ARN
S3_BUCKET_NAME = "creditcardtransactionsstore"  # S3 bucket for storing transactions

def lambda_handler(event, context):
    flask_url = "http://<ec2-public-ip>/predict"

    try:
        partition = list(event['records'].keys())[0]
        messages = event['records'][partition]

        for data in messages:
            decoded_value = base64.b64decode(data['value']).decode('utf-8')
            payload = json.loads(decoded_value)  # `payload` is the transaction dictionary
            print("Received Payload:", payload)

            # Make a POST request using urllib3
            encoded_data = json.dumps(payload).encode('utf-8')
            response = http.request(
                "POST",
                flask_url,
                body=encoded_data,
                headers={"Content-Type": "application/json"}
            )

            response_data = json.loads(response.data.decode('utf-8'))
            print("Response from Flask API:", response_data)

            # Extract prediction result
            is_fraud = isinstance(response_data.get("predictions"), list) and 1 in response_data["predictions"]

            # Add prediction result to the payload
            payload["fraud_prediction"] = 1 if is_fraud else 0
            payload["timestamp"] = datetime.utcnow().isoformat()  # Add timestamp

            # Save transaction to S3
            store_transaction_s3(payload)

            # If fraud detected, send SNS alert
            if is_fraud:
                alert_message = f"🚨 Fraud Alert! Suspicious transaction detected: {payload}"
                sns_client.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=alert_message,
                    Subject="🚨 Fraud Alert"
                )
                print("✅ Fraud alert sent to SNS topic.")

    except Exception as e:
        print(f"❌ Error: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def store_transaction_s3(transaction_data):
    """
    Stores transaction data in an S3 bucket.
    The file will be stored under: s3://creditcardtransactionsstore/YYYY/MM/DD/txn_<txn_id>.json
    """
    try:
        # Generate unique file key based on timestamp
        timestamp = transaction_data["timestamp"][:10]  # YYYY-MM-DD
        file_key = f"transactions/{timestamp}/txn_{transaction_data.get('txn_id', 'unknown')}.json"

        # Upload transaction JSON to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=file_key,
            Body=json.dumps(transaction_data),
            ContentType="application/json"
        )
        print(f"✅ Transaction stored in S3: {file_key}")

    except Exception as e:
        print(f"❌ Error storing transaction in S3: {e}")
