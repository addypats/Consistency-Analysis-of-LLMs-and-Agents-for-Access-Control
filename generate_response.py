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

load_dotenv()

class Gen_Resp:
    
    # chatgpt interface
    def generate_response_chat(self, prompt):
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
    
    # meta interface
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
    
        print("META")
        print(self.prompt)
        print("----------------------------------------")
        print(self.predicted[(len(self.prompt) + 1):])
        return self.predicted[(len(self.prompt) + 1):]

    
    
    # bloom interface
    def generate_response_bloom(self, prompt):

        self.prompt = prompt
        self.checkpoint = "bigscience/bloomz-1b7"

        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)
        self.model = AutoModelForCausalLM.from_pretrained(self.checkpoint)

        self.input = self.tokenizer.encode(self.prompt, return_tensors="pt")

        self.outputs = self.model.generate(self.input, max_length=2500)

        self.message = self.tokenizer.decode(self.outputs[0])

        return self.message[(len(self.prompt) + 1):]
    
    
    # Gemini Interface
    def generate_response_gemini(self, prompt):
        
        self.prompt = prompt
        genai.configure(api_key=os.getenv("Google_Gemini_API_Key"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(self.prompt)
        self.message = response.text
        
        return self.message

    def generate_response_claude(self, prompt):
        self.prompt = prompt

        openai_api_key_personal = os.getenv("Chat_GPT_API_Key")

        openai.api_key = openai_api_key_personal

        self.model_engine = "gpt-3.5-turbo"

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
        
    # Cohere Interface
    def generate_response_Cohere(self, prompt):  
        self.prompt = prompt
        Api_key = os.getenv("Cohere_API_Key")
        co = cohere.Client(Api_key)
        response = co.chat(
            message=self.prompt
        )
        return response.text.strip()
        
    # Llama Interface
    def generate_response_Llama(self, prompt):
        
        self.prompt = prompt
        # Replace 'Your_API_Token' with your actual API token
        self.Api_key = os.getenv("Llama_API_Key")
        self.llama = LlamaAPI(self.Api_key)
        
        # API Request JSON Cell
        self.api_request_json = {
        "model": "llama3-70b",
        "messages": [
            {"role": "system", "content": ""},
            {"role": "user", "content": self.prompt},
        ]
        }

        # Make your request and handle the response
        self.response = self.llama.run(self.api_request_json)
        self.jsonfile = self.response.json()
        self.message = self.jsonfile['choices'][0]['message']['content']
        
        return self.message


    # auto generation
    def auto_generate(self, topic, no_of_questions):
        openai_api_key_personal = os.getenv("Chat_GPT_API_Key")

        openai.api_key = openai_api_key_personal
        self.topic = topic
        self.no_of_questions = no_of_questions

        self.prompt = "Generate " + self.no_of_questions + "questions, that are less than 29 characters, related to " + self.topic + "in Computer Science."

        self.model_engine = "gpt-4o-mini"

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