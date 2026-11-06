import boto3, json, time

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

MODELS = ["us.anthropic.claude-opus-4-7", "us.anthropic.claude-sonnet-4-6"]
QUESTIONS = [
    "How many days of annual leave do I get?",
    "Can you help me write a cover letter?",
    "What's the process for claiming home office expenses?"
]

for model in MODELS:
    for q in QUESTIONS:
        start = time.time()
        resp = bedrock.invoke_model(
            modelId=model,
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 400,
                'system': system_v2,
                'messages': [{"role": "user", "content": q}]
            })
        )
        body = json.loads(resp['body'].read())
        latency_ms = (time.time() - start) * 1000
        answer = next((b['text'] for b in body['content'] if b['type'] == 'text'), '')
        print(f"\n--- {model} ---")
        print(f"Q: {q}")
        print(f"A: {answer[:200]}")
        print(f"Latency: {latency_ms:.0f}ms | In: {body['usage']['input_tokens']} | Out: {body['usage']['output_tokens']}")