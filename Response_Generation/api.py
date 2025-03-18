from Response_Generation.generate_response import Gen_Resp
import sys

GR = Gen_Resp()

class api:

    # function for sensitivity, cross-validation, and checking if the answer is correct
    # for VALIDATING all the answers to the INITIAL questions given to the model
    def process_policy_description(self, questions_list, counter):
        
        self.questions_list = questions_list
        self.counter = counter
        print("SELF.QUESTIONS_LIST and COUNTER in PROCESS_QUESTIONS")
        print(self.questions_list)
        print(self.counter)
        self.count = int(self.counter)

        # for all the questions given to the model
        print("for self.i, self.quest in enumerate(self.questions_list):")
        for self.i, self.quest in enumerate(self.questions_list):
            self.quest = self.quest.strip()
            self.prompt = self.quest
            print("SELF.I")
            print(self.i)
            print("SELF.QUEST")
            print(self.quest)

            # initializations
            self.model_response_check_list_chatgpt = []
            self.model_response_check_list_meta_opt = []
            self.model_response_check_list_bloom = []
            self.model_response_check_list_gemini = []
            self.model_response_check_list_claude = []
            self.model_response_check_list_cohere = []
            self.model_response_check_list_llama = []

            # self.question = " Is this the correct answer for the question: \"" + self.prompt + "\"? Answer with just yes or no"
            # self.question = self.question.strip()

            print("SELF.QUESTION")
            print(self.question)


            # Original response from models for the original question
            self.model_response_for_each_q_chatgpt = GR.generate_response_chat(self.prompt)
            self.model_response_for_each_q_meta_opt = GR.generate_response_meta(self.prompt)
            self.model_response_for_each_q_bloom = GR.generate_response_bloom(self.prompt)
            self.model_response_for_each_q_gemini = GR.generate_response_gemini(self.prompt)
            self.model_response_for_each_q_claude = GR.generate_response_claude(self.prompt)
            
            self.model_response_for_each_q_llama = GR.generate_response_Llama(self.prompt)
            self.model_response_for_each_q_cohere = GR.generate_response_Cohere(self.prompt)
            

            # self.original_response_list_for_each_q_chatgpt.append(self.model_response_for_each_q_chatgpt)
            # self.original_response_list_for_each_q_meta_opt.append(self.model_response_for_each_q_meta_opt)
            # self.original_response_list_for_each_q_bloom.append(self.model_response_for_each_q_bloom)
            # self.original_response_list_for_each_q_gemini.append(self.model_response_for_each_q_gemini)
            # self.original_response_list_for_each_q_claude.append(self.model_response_for_each_q_claude)
            # self.original_response_list_for_each_q_cohere.append(self.model_response_for_each_q_cohere)
            # self.original_response_list_for_each_q_llama.append(self.model_response_for_each_q_llama)

            # self.model_response_and_question_chatgpt = self.model_response_for_each_q_chatgpt + self.question
            # self.model_response_and_question_meta_opt = self.model_response_for_each_q_meta_opt + self.question
            # self.model_response_and_question_bloom = self.model_response_for_each_q_bloom + self.question
            # self.model_response_and_question_gemini = self.model_response_for_each_q_gemini + self.question
            # self.model_response_and_question_claude = self.model_response_for_each_q_claude + self.question
            # self.model_response_and_question_cohere = self.model_response_for_each_q_cohere + self.question
            # self.model_response_and_question_llama = self.model_response_for_each_q_llama + self.question


            # run the loop for the number of times specified by the user
            for self.p in range(self.count):
                self.model_temp_response_chatgpt = GR.generate_response_chat(self.model_response_and_question_chatgpt)
                self.model_response_check_list_chatgpt.append(self.model_temp_response_chatgpt)

            # self.model_response_check_list_super_chatgpt.append(self.model_response_check_list_chatgpt)
            # self.model_response_check_list_super_meta_opt.append(self.model_response_check_list_meta_opt)
            # self.model_response_check_list_super_bloom.append(self.model_response_check_list_bloom)
            # self.model_response_check_list_super_gemini.append(self.model_response_check_list_gemini)
            # self.model_response_check_list_super_claude.append(self.model_response_check_list_claude)
            # self.model_response_check_list_super_cohere.append(self.model_response_check_list_cohere)
            # self.model_response_check_list_super_llama.append(self.model_response_check_list_llama)

        # return results
        # return {
        #     'original_response_list_for_each_q_chatgpt': self.original_response_list_for_each_q_chatgpt,
        #     'model_response_check_list_super_chatgpt': self.model_response_check_list_super_chatgpt,
        #     'original_response_list_for_each_q_meta_opt': self.original_response_list_for_each_q_meta_opt,
        #     'model_response_check_list_super_meta_opt': self.model_response_check_list_super_meta_opt,
        #     'original_response_list_for_each_q_bloom': self.original_response_list_for_each_q_bloom,
        #     'model_response_check_list_super_bloom': self.model_response_check_list_super_bloom,
        #     'original_response_list_for_each_q_gemini': self.original_response_list_for_each_q_gemini,
        #     'model_response_check_list_super_gemini': self.model_response_check_list_super_gemini,
        #     'original_response_list_for_each_q_claude': self.original_response_list_for_each_q_claude,
        #     'model_response_check_list_super_claude': self.model_response_check_list_super_claude,
        #     'original_response_list_for_each_q_cohere': self.original_response_list_for_each_q_cohere,
        #     'model_response_check_list_super_cohere': self.model_response_check_list_super_cohere,
        #     'original_response_list_for_each_q_llama': self.original_response_list_for_each_q_llama,
        #     'model_response_check_list_super_llama': self.model_response_check_list_super_llama,
        #     'cross_valid_chat_list': self.cross_valid_chat_list,
        #     'cross_valid_meta_list': self.cross_valid_meta_list,
        #     'cross_valid_bloom_list': self.cross_valid_bloom_list,
        #     'cross_valid_gemini_list': self.cross_valid_gemini_list,
        #     'cross_valid_claude_list': self.cross_valid_claude_list,
        #     'cross_valid_cohere_list': self.cross_valid_cohere_list,
        #     'cross_valid_llama_list': self.cross_valid_llama_list
        # }
        
        return None

    # function for generating answers to initial questions
    def process_answers(self, questions_list, counter):
        
        self.questions_list = questions_list
        self.counter = counter

        print("SELF.QUESTIONS_LIST and COUNTER in PROCESS_ANSWERS")
        print(self.questions_list)

        # model_response_check_list_super is a list of lists that contains a list of answers for each question
        self.model_response_check_list_super_chatgpt = []
        self.model_response_check_list_super_meta_opt = []
        self.model_response_check_list_super_bloom = []
        self.model_response_check_list_super_gemini = []
        self.model_response_check_list_super_claude = []
        self.model_response_check_list_super_cohere = []
        self.model_response_check_list_super_llama = []

        # Original response lists
        self.original_response_list_for_each_q_chatgpt = []
        self.original_response_list_for_each_q_meta_opt = []
        self.original_response_list_for_each_q_bloom = []
        self.original_response_list_for_each_q_gemini = []
        self.original_response_list_for_each_q_claude = []
        self.original_response_list_for_each_q_cohere = []
        self.original_response_list_for_each_q_llama = []

        self.count = int(self.counter)
        print(self.counter)

        # for all the questions given to the model
        for self.i, self.question in enumerate(self.questions_list):
            self.question = self.question.strip()
            self.prompt = self.question

            print("SELF.I")
            print(self.i)
            print("SELF.QUEST(ion)")
            print(self.question)

            self.model_response_check_list_chatgpt = []
            self.model_response_check_list_meta_opt = []
            self.model_response_check_list_bloom = []
            self.model_response_check_list_gemini = []
            self.model_response_check_list_claude = []
            self.model_response_check_list_cohere = []
            self.model_response_check_list_llama = []

            # Original response from models for the original question
            self.model_response_for_each_q_chatgpt = GR.generate_response_chat(self.prompt)
            self.model_response_for_each_q_meta_opt = GR.generate_response_meta(self.prompt)
            self.model_response_for_each_q_bloom = GR.generate_response_bloom(self.prompt)
            self.model_response_for_each_q_gemini = GR.generate_response_gemini(self.prompt)
            self.model_response_for_each_q_claude = GR.generate_response_claude(self.prompt)
            self.model_response_for_each_q_cohere = GR.generate_response_Cohere(self.prompt)
            self.model_response_for_each_q_llama = GR.generate_response_Llama(self.prompt)

            self.original_response_list_for_each_q_chatgpt.append(self.model_response_for_each_q_chatgpt)
            self.original_response_list_for_each_q_meta_opt.append(self.model_response_for_each_q_meta_opt)
            self.original_response_list_for_each_q_bloom.append(self.model_response_for_each_q_bloom)
            self.original_response_list_for_each_q_gemini.append(self.model_response_for_each_q_gemini)
            self.original_response_list_for_each_q_claude.append(self.model_response_for_each_q_claude)
            self.original_response_list_for_each_q_cohere.append(self.model_response_for_each_q_cohere)
            self.original_response_list_for_each_q_llama.append(self.model_response_for_each_q_llama)

            # run the loop for the number of times specified by the user

            #This is likely a copy paste from process questions
            #This method (process_answers) is supposed to repeatedly generate answers for the same question.
            #These answers are then used in consistency analysis
            #No need to self valid twice. The regular prompt should be here, not the response + question
            for self.p in range(self.count):
                self.model_temp_response_chatgpt = GR.generate_response_chat(self.prompt)
                self.model_response_check_list_chatgpt.append(self.model_temp_response_chatgpt)

                self.model_temp_response_meta_opt = GR.generate_response_meta(self.prompt)
                self.model_response_check_list_meta_opt.append(self.model_temp_response_meta_opt)

                self.model_temp_response_bloom = GR.generate_response_bloom(self.prompt)
                self.model_response_check_list_bloom.append(self.model_temp_response_bloom)
                
                self.model_temp_response_gemini = GR.generate_response_gemini(self.prompt)
                self.model_response_check_list_gemini.append(self.model_temp_response_gemini)
                
                self.model_temp_response_claude = GR.generate_response_claude(self.prompt)
                self.model_response_check_list_claude.append(self.model_temp_response_claude)
                
                self.model_temp_response_cohere = GR.generate_response_Cohere(self.prompt)
                self.model_response_check_list_cohere.append(self.model_temp_response_cohere)
                
                self.model_temp_response_llama = GR.generate_response_Llama(self.prompt)
                self.model_response_check_list_llama.append(self.model_temp_response_llama)

            self.model_response_check_list_super_chatgpt.append(self.model_response_check_list_chatgpt)
            self.model_response_check_list_super_meta_opt.append(self.model_response_check_list_meta_opt)
            self.model_response_check_list_super_bloom.append(self.model_response_check_list_bloom)
            self.model_response_check_list_super_gemini.append(self.model_response_check_list_gemini)
            self.model_response_check_list_super_claude.append(self.model_response_check_list_claude)
            self.model_response_check_list_super_cohere.append(self.model_response_check_list_cohere)
            self.model_response_check_list_super_llama.append(self.model_response_check_list_llama)

        # return results
        return {
            'original_response_list_for_each_q_chatgpt': self.original_response_list_for_each_q_chatgpt,
            'model_response_check_list_super_chatgpt': self.model_response_check_list_super_chatgpt,
            'original_response_list_for_each_q_meta_opt': self.original_response_list_for_each_q_meta_opt,
            'model_response_check_list_super_meta_opt': self.model_response_check_list_super_meta_opt,
            'original_response_list_for_each_q_bloom': self.original_response_list_for_each_q_bloom,
            'model_response_check_list_super_bloom': self.model_response_check_list_super_bloom,
            'original_response_list_for_each_q_gemini': self.original_response_list_for_each_q_gemini,
            'model_response_check_list_super_gemini': self.model_response_check_list_super_gemini,
            'original_response_list_for_each_q_claude': self.original_response_list_for_each_q_claude,
            'model_response_check_list_super_claude': self.model_response_check_list_super_claude,
            'original_response_list_for_each_q_cohere': self.original_response_list_for_each_q_cohere,
            'model_response_check_list_super_cohere': self.model_response_check_list_super_cohere,
            'original_response_list_for_each_q_llama': self.original_response_list_for_each_q_llama,
            'model_response_check_list_super_llama': self.model_response_check_list_super_llama
        }

    # function for auto-generation of questions
    def auto_generate(self, topic, no_of_questions):
        
        self.topic = topic
        self.no_of_questions = no_of_questions
        
        self.question_response = GR.auto_generate(self.topic, self.no_of_questions)
        self.questions_list = self.question_response.split("? ")
        
        return {'questions_list': self.questions_list}