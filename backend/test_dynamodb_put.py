import boto3, os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

dynamo = boto3.client(
    'dynamodb',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

table = "UniPathAIUsers"
item = {
    "user_id": {"S": "test_user"},
    "timestamp": {"S": datetime.utcnow().isoformat()}
}

dynamo.put_item(TableName=table, Item=item)
print("✅ Wrote test item to DynamoDB table!")
