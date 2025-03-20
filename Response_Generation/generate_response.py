#Wanted to clean it up a bit

import openai
import os
import torch
import google.generativeai as genai
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, OPTForQuestionAnswering
from dotenv import load_dotenv
import cohere
from llamaapi import LlamaAPI
import ollama
from dotenv import load_dotenv
load_dotenv()


#ChatGPT o3 Mini
def generate_response_chato3m(prompt):
    Api_key = os.getenv("Chat_GPT_API_Key")
    client = openai.OpenAI(api_key=Api_key)
    completion = client.chat.completions.create(
        model="o3-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content

def generate_response_deepseek(prompt):
    Api_key = os.getenv("DeepSeek_API_Key")
    client = openai.OpenAI(api_key=Api_key, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": prompt}
    ],
    stream=False
)
    return response.choices[0].message.content

#Meta OPT
# def generate_response_meta(self, prompt):
#     self.prompt = prompt
    
#     torch.manual_seed(4)

#     self.tokenizer = AutoTokenizer.from_pretrained("facebook/opt-350m")
#     self.model = AutoModelForCausalLM.from_pretrained("facebook/opt-350m")
    
#     self.inputs = self.tokenizer(self.prompt, return_tensors="pt")
    
#     with torch.no_grad():
#         self.outputs = self.model.generate(
#             input_ids=self.inputs.input_ids,
#             num_return_sequences=1,
#             max_new_tokens=30,
#             pad_token_id=self.tokenizer.eos_token_id,

#         )

#     self.predicted = self.tokenizer.decode(self.outputs[0], skip_special_tokens=True)
#     return self.predicted[(len(self.prompt) + 1):]





# def generate_response_deepseek(self, prompt):
#     messages = [{"role": "user", "content": "Who are you?"},]
#     pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-V3", trust_remote_code=True)
#     pipe(messages)

#Bloom
def generate_response_bloom(prompt):
    checkpoint = "bigscience/bloomz-1b7"

    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForCausalLM.from_pretrained(checkpoint)

    input = tokenizer.encode(prompt, return_tensors="pt")

    outputs = model.generate(input, max_length=2500)

    message = tokenizer.decode(outputs[0])
    # print(message)
    return message[(len(prompt) + 1):]

#Gemini
def generate_response_gemini(prompt):
        
    prompt = prompt
    genai.configure(api_key=os.getenv("Google_Gemini_API_Key"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    message = response.text
    
    return message

#ChatGPT 4o Mini
def generate_response_chat4om(prompt):
    Api_key = os.getenv("Chat_GPT_API_Key")
    client = openai.OpenAI(api_key=Api_key)
    completion = client.chat.completions.create(
        model="o3-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content

def generate_response_Cohere(prompt):  
        Api_key = os.getenv("Cohere_API_Key")
        co = cohere.ClientV2(Api_key)
        response = co.chat(
            model="command-r7b-12-2024",
            messages=[{"role": "user", "content": prompt}]
        )
        print(response.message.content[0].text)
        return response.message.content[0].text.strip()

# def generate_response_Llama(self, prompt):
    
#     self.prompt = prompt
#     # Replace 'Your_API_Token' with your actual API token
#     self.Api_key = os.getenv("Llama_API_Key")
#     self.llama = LlamaAPI(self.Api_key)
    
#     # API Request JSON Cell
#     self.api_request_json = {
#     "model": "llama3-70b",
#     "messages": [
#         {"role": "system", "content": ""},
#         {"role": "user", "content": self.prompt},
#     ]
#     }

#     # Make your request and handle the response
#     self.response = self.llama.run(self.api_request_json)
#     self.jsonfile = self.response.json()
#     self.message = self.jsonfile['choices'][0]['message']['content']
    
#     return self.message


#Ran out of tokens, so running Llama3 locally with Ollama
#Download Ollama and run ollama pull Llama3
def generate_response_Llama(prompt):
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    return response['message']['content'].strip()