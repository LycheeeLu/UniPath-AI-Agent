import boto3, json, os
from dotenv import load_dotenv

load_dotenv()
region = os.getenv("AWS_REGION", "us-east-1")
model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet")


if os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"):
    bedrock = boto3.client(
        "bedrock-runtime",
        region_name=region,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
else:
    bedrock = boto3.client("bedrock-runtime", region_name=region)

def call_bedrock(prompt: str) -> str:
    """
        cross-region inference profile
    """
    body = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "anthropic_version": "bedrock-2023-05-31"
        }

    response = bedrock.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body)
    )

    out = json.loads(response["body"].read().decode("utf-8"))

        # Try Claude 4.x format
    if "output" in out and "message" in out["output"]:
        text = out["output"]["message"]["content"][0]["text"]
        return text.strip()


     # Otherwise, return raw response
    else:
        return str(out)
