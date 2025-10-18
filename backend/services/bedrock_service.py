import boto3, json, os
from dotenv import load_dotenv

load_dotenv()
region = os.getenv("AWS_REGION", "us-east-1")
model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet")

bedrock = boto3.client("bedrock-runtime", region_name=region)

def call_bedrock(prompt: str) -> str:
    body = {"inputText": prompt}
    response = bedrock.invoke_model(
        modelId=model_id,
        contentType="application/json",
        body=json.dumps(body)
    )
    out = json.loads(response["body"].read())
    return out["results"][0]["outputText"]
