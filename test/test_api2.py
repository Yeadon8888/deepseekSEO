from openai import OpenAI
  
client = OpenAI(
    base_url="https://api.ppinfra.com/v3/openai",
    api_key="sk_lBPmVmoH57YDiskY3e2teS-1-Zf-JFlysM7Lh2W6ZSc",
)

model = "deepseek/deepseek-r1/community"
stream = True # or False
max_tokens = 10240
system_content = """你是派欧算力云 AI 助手，你会以诚实专业的态度帮助用户，用中文回答问题。\n开启深度思考。请用 <think> 和</think> 包裹你的内部推理过程，最终回复要简洁自然。\n"""
temperature = 1
top_p = 1
min_p = 0
top_k = 50
presence_penalty = 0
frequency_penalty = 0
repetition_penalty = 1
response_format = { "type": "text" }

chat_completion_res = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": system_content,
        },
        {
            "role": "user",
            "content": "你是谁",
        }
    ],
    stream=stream,
    max_tokens=max_tokens,
    temperature=temperature,
    top_p=top_p,
    presence_penalty=presence_penalty,
    frequency_penalty=frequency_penalty,
    response_format=response_format,
    extra_body={
      "top_k": top_k,
      "repetition_penalty": repetition_penalty,
      "min_p": min_p
    }
  )

if stream:
    for chunk in chat_completion_res:
        print(chunk.choices[0].delta.content or "", end="")
else:
    print(chat_completion_res.choices[0].message.content)
  
  