#Wanted to clean it up a bit

import openai
import os
import requests
import json
import cohere
import json
import torch
import google.generativeai as genai
from llamaapi import LlamaAPI
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, OPTForQuestionAnswering
from dotenv import load_dotenv
import sys
import time
#ChatGPT 4o Mini
def generate_response_chato3m(self, prompt):
    self.prompt = prompt

    openai_api_key_personal = os.getenv("Chat_GPT_API_Key")

    openai.api_key = openai_api_key_personal

    self.model_engine = "o3-mini"

    self.prompt = prompt.strip()
    self.completions = openai.ChatCompletion.create(
        model=self.model_engine,
        messages=[
        {"role": "system", "content": ""},
        {"role": "user", "content": self.prompt},
    ],
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    self.message = self.completions.choices[0].message.content.strip()


    return self.message

#Meta OPT
def generate_response_meta(self, prompt):
    self.prompt = prompt
    
    torch.manual_seed(4)

    self.tokenizer = AutoTokenizer.from_pretrained("facebook/opt-350m")
    self.model = AutoModelForCausalLM.from_pretrained("facebook/opt-350m")
    
    self.inputs = self.tokenizer(self.prompt, return_tensors="pt")
    
    with torch.no_grad():
        self.outputs = self.model.generate(
            input_ids=self.inputs.input_ids,
            num_return_sequences=1,
            max_new_tokens=30,
            pad_token_id=self.tokenizer.eos_token_id,

        )

    self.predicted = self.tokenizer.decode(self.outputs[0], skip_special_tokens=True)
    return self.predicted[(len(self.prompt) + 1):]

#Bloom
def generate_response_bloom(self, prompt):

    self.prompt = prompt
    self.checkpoint = "bigscience/bloomz-1b7"

    self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)
    self.model = AutoModelForCausalLM.from_pretrained(self.checkpoint)

    self.input = self.tokenizer.encode(self.prompt, return_tensors="pt")

    self.outputs = self.model.generate(self.input, max_length=2500)

    self.message = self.tokenizer.decode(self.outputs[0])

    return self.message[(len(self.prompt) + 1):]

#Gemini
def generate_response_gemini(self, prompt):
        
    self.prompt = prompt
    genai.configure(api_key=os.getenv("Google_Gemini_API_Key"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(self.prompt)
    self.message = response.text
    
    return self.message

#ChatGPT 4o Mini
def generate_response_chat4om(self, prompt):
    self.prompt = prompt

    openai_api_key_personal = os.getenv("Chat_GPT_API_Key")

    openai.api_key = openai_api_key_personal

    self.model_engine = "gpt-4o-mini"

    self.prompt = prompt.strip()
    self.completions = openai.ChatCompletion.create(
        model=self.model_engine,
        messages=[
        {"role": "system", "content": ""},
        {"role": "user", "content": self.prompt},
    ],
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    self.message = self.completions.choices[0].message.content.strip()
    return self.message