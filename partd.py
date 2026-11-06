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

# Simulate a verbose policy document
POLICY_DOC = """ACME CORP HUMAN RESOURCES POLICY HANDBOOK v3.2
Annual Leave: All full-time employees are entitled to 25 days per annum...
[paste a realistic 500-word policy doc here]
"""

# Version 3: verbose — measure token count
resp_verbose = bedrock.invoke_model(
    modelId='us.anthropic.claude-sonnet-4-6',
    body=json.dumps({
        'anthropic_version': 'bedrock-2023-05-31',
        'max_tokens': 400,
        'system': system_v2 + "\n\n" + POLICY_DOC,
        'messages': [{"role": "user", "content": "How many days of annual leave do I get?"}]
    })
)
body_verbose = json.loads(resp_verbose['body'].read())
print("Verbose input tokens:", body_verbose['usage']['input_tokens'])

# Version 4: compressed — same info, fewer words
POLICY_COMPRESSED = "Annual leave: 25 days/yr full-time, 12.5 days part-time. Carry-forward: max 5 days..."
resp_compressed = bedrock.invoke_model(
    modelId='us.anthropic.claude-sonnet-4-6',
    body=json.dumps({
        'anthropic_version': 'bedrock-2023-05-31',
        'max_tokens': 400,
        'system': system_v2 + "\n\n" + POLICY_COMPRESSED,
        'messages': [{"role": "user", "content": "How many days of annual leave do I get?"}]
    })
)
body_compressed = json.loads(resp_compressed['body'].read())
print("Compressed input tokens:", body_compressed['usage']['input_tokens'])
print(f"Token saving: {body_verbose['usage']['input_tokens'] - body_compressed['usage']['input_tokens']}")