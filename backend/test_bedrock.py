from backend.services.bedrock_service import call_bedrock

print("Testing Bedrock...")
result = call_bedrock("Respond with a JSON: {\"hello\": \"world\"}")
print("✅ Result:", result)
