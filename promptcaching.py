import boto3, json

system_v2 = """
You are an HR Policy Assistant for Acme Corp.
You help employees understand company policies on leave, expenses, remote work, and benefits.
Always respond in valid JSON with this schema:
  {"answer": "string", "policy_reference": "string or null", "confidence": "high|medium|low"}
Keep answers under 150 words. If outside HR scope, set answer to a polite refusal and confidence to null.
"""

POLICY_DOC = """ACME CORP HUMAN RESOURCES POLICY HANDBOOK v3.2
Annual Leave: All full-time employees are entitled to 25 days per annum...
[paste a realistic 500-word policy doc here]
"""

bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

# First call — creates the cache
print("--- First call (cache creation) ---")
resp1 = bedrock.invoke_model(
    modelId='us.anthropic.claude-sonnet-4-6',
    body=json.dumps({
        'anthropic_version': 'bedrock-2023-05-31',
        'max_tokens': 400,
        'system': [{"type": "text", "text": system_v2 + "\n\n" + POLICY_DOC, "cache_control": {"type": "ephemeral"}}],
        'messages': [{"role": "user", "content": "What is the remote work policy?"}]
    })
)
body1 = json.loads(resp1['body'].read())
print("Input tokens:", body1['usage']['input_tokens'])
print("Cache created:", body1['usage'].get('cache_creation_input_tokens', 0))
print("Cache read:", body1['usage'].get('cache_read_input_tokens', 0))

# Second call — should read from cache
print("\n--- Second call (cache hit) ---")
resp2 = bedrock.invoke_model(
    modelId='us.anthropic.claude-sonnet-4-6',
    body=json.dumps({
        'anthropic_version': 'bedrock-2023-05-31',
        'max_tokens': 400,
        'system': [{"type": "text", "text": system_v2 + "\n\n" + POLICY_DOC, "cache_control": {"type": "ephemeral"}}],
        'messages': [{"role": "user", "content": "How many days of annual leave do I get?"}]
    })
)
body2 = json.loads(resp2['body'].read())
print("Input tokens:", body2['usage']['input_tokens'])
print("Cache created:", body2['usage'].get('cache_creation_input_tokens', 0))
print("Cache read:", body2['usage'].get('cache_read_input_tokens', 0))