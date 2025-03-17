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


#This is the same code as the other consistency system, but need to add the ability to generate a .conf file


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
    
    
    # Download the generated .conf file
    # I know it is just writing the generated response to a file, but for now it works
    
    
    # from transformers import AutoModelForCausalLM, AutoTokenizer

    # model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
    # tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

    # prompt = "Generate an optimized Apache .conf file for high performance."

    # inputs = tokenizer(prompt, return_tensors="pt")
    # output = model.generate(**inputs, max_length=512)
    # generated_conf = tokenizer.decode(output[0], skip_special_tokens=True)

    # with open("generated_config.conf", "w") as f:
    #     f.write(generated_conf)

    # print("Config file saved.")


    
    
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
    
    
    # Download the generated .conf file
    # I know it is just writing the generated response to a file, but for now it works
    
    
    # from transformers import AutoModelForCausalLM, AutoTokenizer

    # model_name = "bigscience/bloom-7b1"
    # model = AutoModelForCausalLM.from_pretrained(model_name)
    # tokenizer = AutoTokenizer.from_pretrained(model_name)

    # # Read .conf file
    # with open("server.conf", "r") as f:
    #     conf_data = f.read()

    # # Generate output
    # prompt = f"Optimize this configuration file:\n{conf_data}"
    # inputs = tokenizer(prompt, return_tensors="pt")
    # output = model.generate(**inputs, max_length=512)

    # generated_conf = tokenizer.decode(output[0], skip_special_tokens=True)

    # # Save new config
    # with open("optimized_server.conf", "w") as f:
    #     f.write(generated_conf)

    
    
    # Gemini Interface
    def generate_response_gemini(self, prompt):
        
        self.prompt = prompt
        genai.configure(api_key=os.getenv("Google_Gemini_API_Key"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(self.prompt)
        self.message = response.text
        
        return self.message


    # Download the generated .conf file
    # I know it is just writing the generated response to a file, but for now it works
    
    # import google.generativeai as genai

    # genai.configure(api_key="YOUR_GOOGLE_API_KEY")

    # # Read file
    # with open("server.conf", "r") as f:
    #     conf_text = f.read()

    # # Send request to Gemini
    # response = genai.chat(messages=[{"role": "user", "content": f"Optimize this .conf file:\n{conf_text}"}])

    # # Extract result
    # generated_conf = response.last.content

    # # Save new config
    # with open("optimized_server.conf", "w") as f:
    #     f.write(generated_conf)

    # print("Optimized config saved.")

    
    
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
        
        
    # Download the generated .conf file
    # I know it is just writing the generated response to a file, but for now it works
    
    # import anthropic
    # client = anthropic.Anthropic(api_key="YOUR_ANTHROPIC_API_KEY")

    # with open("server.conf", "r") as f:
    #     conf_text = f.read()

    # # Send request to Claude
    # response = client.completions.create(
    #     model="claude-2",
    #     messages=[{"role": "user", "content": f"Optimize this .conf file:\n{conf_text}"}],
    #     max_tokens=1024
    # )

    # generated_conf = response.choices[0].message.content

    # # Save new config
    # with open("optimized_server.conf", "w") as f:
    #     f.write(generated_conf)

    # print("Optimized config saved.")

    
    
    # Cohere Interface
    def generate_response_Cohere(self, prompt):  
        self.prompt = prompt
        Api_key = os.getenv("Cohere_API_Key")
        co = cohere.Client(Api_key)
        response = co.chat(
            message=self.prompt
        )
        return response.text.strip()
        
        
    # Download the generated .conf file
    # I know it is just writing the generated response to a file, but for now it works
    
    # import cohere

    # co = cohere.Client("YOUR_COHERE_API_KEY")

    # with open("server.conf", "r") as f:
    #     conf_text = f.read()

    # # Generate new config
    # response = co.generate(
    #     model="command-r-plus",
    #     prompt=f"Optimize this configuration:\n{conf_text}",
    #     max_tokens=1024
    # )

    # generated_conf = response.generations[0].text

    # # Save the new config
    # with open("optimized_server.conf", "w") as f:
    #     f.write(generated_conf)

    # print("Optimized config saved.")

        
        
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


    # Download the generated .conf file
    # I know it is just writing the generated response to a file, but for now it works
    
    # from transformers import AutoModelForCausalLM, AutoTokenizer

    # model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
    # tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

    # # Read .conf file
    # with open("server.conf", "r") as f:
    #     conf_text = f.read()

    # prompt = f"Optimize this .conf file:\n{conf_text}"
    # inputs = tokenizer(prompt, return_tensors="pt")
    # output = model.generate(**inputs, max_length=512)

    # generated_conf = tokenizer.decode(output[0], skip_special_tokens=True)

    # # Save new config
    # with open("optimized_server.conf", "w") as f:
    #     f.write(generated_conf)

    # print("Config file saved.")

    
    
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