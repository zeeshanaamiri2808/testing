import boto3, json

system_v2 = """
You are an HR Policy Assistant for Acme Corp.
You help employees understand company policies on leave, expenses, remote work, and benefits.
Always respond in valid JSON with this schema:
  {"answer": "string", "policy_reference": "string or null", "confidence": "high|medium|low"}
Keep answers under 150 words. If outside HR scope, set answer to a polite refusal and confidence to null.
"""

bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

resp = bedrock.invoke_model(
    modelId='us.anthropic.claude-sonnet-4-6',
    body=json.dumps({
        'anthropic_version': 'bedrock-2023-05-31',
        'max_tokens': 400,
        'system': system_v2,
        'messages': [{"role": "user", "content": "How many days of annual leave do I get?"}]
    })
)
body = json.loads(resp['body'].read())
text = next((b['text'] for b in body['content'] if b['type'] == 'text'), None)
if text is None:
    print("No text response from model")
else:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    try:
        data = json.loads(stripped)
        print(data)
    except json.JSONDecodeError:
        print("Model did not return valid JSON:", text)
print("Input tokens:", body['usage']['input_tokens'])
print("Output tokens:", body['usage']['output_tokens'])