# -*- coding: utf-8 -*-
"""LLM(Llama2).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1W1pIwV6zCW9NIz4d8bqPWtTzfMdiG2G3
"""

# !pip install -q accelerate==0.21.0 peft==0.4.0 bitsandbytes==0.40.2 transformers==4.31.0 trl==0.4.7 sentencepiece

import torch
from huggingface_hub import notebook_login
from transformers import GenerationConfig, LlamaForCausalLM, LlamaTokenizer

notebook_login()

MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = LlamaTokenizer.from_pretrained(MODEL_NAME)

model = LlamaForCausalLM.from_pretrained(
    MODEL_NAME,
    return_dict=True,
    load_in_8bit=True,
    torch_dtype=torch.float16,
    device_map="auto",
)

generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
generation_config

def format_prompt(prompt: str, system_prompt: str) -> str:
    return f"""
{system_prompt}
{prompt}
""".strip()

def generate_response(prompt: str, max_new_tokens: int = 128) -> str:
    encoding = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.inference_mode():
        outputs = model.generate(
            **encoding,
            max_new_tokens=max_new_tokens,
            temperature=1.0,
            generation_config=generation_config,
        )
    answer_tokens = outputs[:, encoding.input_ids.shape[1] :]
    return tokenizer.decode(answer_tokens[0], skip_special_tokens=True)

SYSTEM_PROMPT = """
You have to generate a response based on text input from the user. The response needs to be formal and should follow the Indian Penal Code without any compromise.
You have to guve proper sections which will be applicable to the collective statements of witnesses and follow the Indian penal code to the T.
You cannnot use anyother law than Indian Penal Code.
The response needs to be formal and must tell wether the section applicable is cognizable, give a proper short description of the section to the user, tell whether the offense is bailable or not.
""".strip()

import pandas as pd
import random as rand

data = pd.read_csv('/content/FIR_DATASET(updated).csv')

data['Description'] = data['Description'].astype(str)

prompt = rand.choice(data['Offense'])
prompt

generate_response(format_prompt('what is the length of string input we can give as prompt to you?', ''))
