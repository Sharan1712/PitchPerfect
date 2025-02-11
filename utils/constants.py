system_prompt = "You're an Intelligent Custom Cover Letter writer. Your task is to generate a very professional and perfect cover letter based on all the details you get."
model_name_mapping = {
    "GPT-4o mini":"gpt-4o-mini",
    "GPT-4o": "gpt-4o",
    "o1": "o1",
    "o3-mini": "o3-mini",
    "Deepseek-V3": "deepseek-ai/DeepSeek-V3",
    "Deepseek-r1": "deepseek-ai/DeepSeek-R1",
    "Mistral Small 24B": "mistralai/Mistral-Small-24B-Instruct-2501",
    "LLaMa 3.3 70B": "meta-llama/Llama-3.3-70B-Instruct",
    "DeepSeek-R1-Distill-Qwen-32B": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    "Mistral 7B v0.3": "mistralai/Mistral-7B-Instruct-v0.3"
}

model_family_mapping = {
    "GPT-4o mini":"gpt",
    "GPT-4o": "gpt",
    "o1": "gpt",
    "o3-mini": "gpt",
    "Deepseek-V3": "together",
    "Deepseek-r1": "together",
    "Mistral Small 24B": "together",
    "LLaMa 3.3 70B": "together",
    "DeepSeek-R1-Distill-Qwen-32B": "hf",
    "Mistral 7B v0.3": "hf"
}