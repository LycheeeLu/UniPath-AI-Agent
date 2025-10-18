import os
import boto3
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv
from datetime import datetime

# Load credentials from .env
load_dotenv()

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)


TABLE_NAME = "UniPathAIUsers"


def get_table():
    """Return a DynamoDB table resource."""
    return dynamodb.Table(TABLE_NAME)


def add_user_item(user_id: str, filename: str, s3_path: str):
    """
    write uploaded data from user
    user_id: userID (or UUID)
    filename: uploaded file name
    s3_path: path in S3
    """
    table = get_table()
    timestamp = datetime.utcnow().isoformat()
    table.put_item(
        Item={
            "user_id": user_id,
            "upload_time": timestamp,
            "filename": filename,
            "s3_path": s3_path,
        }
    )
    return {"status": "success", "user_id": user_id, "upload_time": timestamp}


def get_user_item(user_id: str):
    """fetch user data from user_id """
    table = get_table()
    resp = table.get_item(Key={"user_id": user_id})
    return resp.get("Item", None)


def update_user_item(user_id: str, updates: dict):
    """
    update user data and include recommended program or AI summary
    updates: dic, such as {"summary": "...", "recommended_programs": [...]}
    """
    table = get_table()

    update_expr = "SET " + ", ".join(f"#{k}=:{k}" for k in updates.keys())
    expr_attr_names = {f"#{k}": k for k in updates.keys()}
    expr_attr_values = {f":{k}": v for k, v in updates.items()}

    table.update_item(
        Key={"user_id": user_id},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_attr_names,
        ExpressionAttributeValues=expr_attr_values,
    )
    return {"status": "updated", "user_id": user_id}


def list_all_users():
    """scan the whole sheet and provide a list of all users"""
    table = get_table()
    resp = table.scan()
    return resp.get("Items", [])
