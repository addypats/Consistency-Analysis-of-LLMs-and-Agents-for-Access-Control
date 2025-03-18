from Result_Modules.result_processing import Result
from Result_Modules.result_answers_processing import Result_Answers

R = Result()
RA = Result_Answers()


class Llm_Model_Process:
    
    def Llm_Model_Process(self, data_dict_questions, data_dict_answers, questions_list, counter, model):
        # Initializations
        self.data_dict_questions = data_dict_questions
        self.data_dict_answers = data_dict_answers
        self.questions_list = questions_list
        self.counter = int(counter)
        self.model = model
        f = open("results.txt", 'a')
        print(model, file=f)
        f.write("\n\n")
        f.close()
        
        # Unpack data from the generate response api ChatGPT
        
        self.no_of_questions = len(self.questions_list)
        print("LLM_MODEL PROCESS")
        print("Model = " + self.model)
        print("NUMBER OF QUESTIONS")
        print(self.no_of_questions)
        print("COUNTER")
        print(counter)
        
        if self.model == "chatgpt":
        
        # Get data from the generate response api ChatGPT (checks for 'is this the answer for the question: ...')
            self.orignal_response_list_for_each_q_llm_q = self.data_dict_questions['original_response_list_for_each_q_chatgpt']
            self.model_response_check_list_super_llm_q = self.data_dict_questions['model_response_check_list_super_chatgpt']
            self.cross_valid_list = self.data_dict_questions['cross_valid_chat_list']
            
            # Get data from the generate response api ChatGPT (original answers to the questions)
            self.orignal_response_list_for_each_q = self.data_dict_answers['original_response_list_for_each_q_chatgpt']
            self.model_response_check_list_super = self.data_dict_answers['model_response_check_list_super_chatgpt']
            
            
        elif self.model == "metaopt":
        
        # Get data from the generate response api Meta OPT (checks for 'is this the answer for the question: ...')
            self.orignal_response_list_for_each_q_llm_q = self.data_dict_questions['original_response_list_for_each_q_meta_opt']
            self.model_response_check_list_super_llm_q = self.data_dict_questions['model_response_check_list_super_meta_opt']
            self.cross_valid_list = self.data_dict_questions['cross_valid_meta_list']

            # Get data from the generate response api Meta OPT (original answers to the questions)
            self.orignal_response_list_for_each_q = self.data_dict_answers['original_response_list_for_each_q_meta_opt']
            self.model_response_check_list_super = self.data_dict_answers['model_response_check_list_super_meta_opt']
            
            
        elif self.model == "bloom":
        
        # Get data from the generate response api Bloom (checks for 'is this the answer for the question: ...')
            self.orignal_response_list_for_each_q_llm_q = self.data_dict_questions['original_response_list_for_each_q_bloom']
            self.model_response_check_list_super_llm_q = self.data_dict_questions['model_response_check_list_super_bloom']
            self.cross_valid_list = self.data_dict_questions['cross_valid_bloom_list']

            # Get data from the generate response api Bloom (original answers to the questions)
            self.orignal_response_list_for_each_q = self.data_dict_answers['original_response_list_for_each_q_bloom']
            self.model_response_check_list_super = self.data_dict_answers['model_response_check_list_super_bloom']
            
        elif self.model == "gemini":
        
        # Get data from the generate response api Bloom (checks for 'is this the answer for the question: ...')
            self.orignal_response_list_for_each_q_llm_q = self.data_dict_questions['original_response_list_for_each_q_gemini']
            self.model_response_check_list_super_llm_q = self.data_dict_questions['model_response_check_list_super_gemini']
            self.cross_valid_list = self.data_dict_questions['cross_valid_gemini_list']

            # Get data from the generate response api Bloom (original answers to the questions)
            self.orignal_response_list_for_each_q = self.data_dict_answers['original_response_list_for_each_q_gemini']
            self.model_response_check_list_super = self.data_dict_answers['model_response_check_list_super_gemini']
            
        elif self.model == "claude":
        
        # Get data from the generate response api Bloom (checks for 'is this the answer for the question: ...')
            self.orignal_response_list_for_each_q_llm_q = self.data_dict_questions['original_response_list_for_each_q_claude']
            self.model_response_check_list_super_llm_q = self.data_dict_questions['model_response_check_list_super_claude']
            self.cross_valid_list = self.data_dict_questions['cross_valid_claude_list']

            # Get data from the generate response api Bloom (original answers to the questions)
            self.orignal_response_list_for_each_q = self.data_dict_answers['original_response_list_for_each_q_claude']
            self.model_response_check_list_super = self.data_dict_answers['model_response_check_list_super_claude']
            
        elif self.model == "cohere":
        
        # Get data from the generate response api Bloom (checks for 'is this the answer for the question: ...')
            self.orignal_response_list_for_each_q_llm_q = self.data_dict_questions['original_response_list_for_each_q_cohere']
            self.model_response_check_list_super_llm_q = self.data_dict_questions['model_response_check_list_super_cohere']
            self.cross_valid_list = self.data_dict_questions['cross_valid_cohere_list']

            # Get data from the generate response api Bloom (original answers to the questions)
            self.orignal_response_list_for_each_q = self.data_dict_answers['original_response_list_for_each_q_cohere']
            self.model_response_check_list_super = self.data_dict_answers['model_response_check_list_super_cohere']
            
        elif self.model == "llama":
        
        # Get data from the generate response api Bloom (checks for 'is this the answer for the question: ...')
            self.orignal_response_list_for_each_q_llm_q = self.data_dict_questions['original_response_list_for_each_q_llama']
            self.model_response_check_list_super_llm_q = self.data_dict_questions['model_response_check_list_super_llama']
            self.cross_valid_list = self.data_dict_questions['cross_valid_llama_list']

            # Get data from the generate response api Bloom (original answers to the questions)
            self.orignal_response_list_for_each_q = self.data_dict_answers['original_response_list_for_each_q_llama']
            self.model_response_check_list_super = self.data_dict_answers['model_response_check_list_super_llama']
            
        #This should be the actual data for real self valid (checking yourself, "is this answer correct")    
        #self.results_q = R.result_process(self.orignal_response_list_for_each_q_llm_q, self.model_response_check_list_super_llm_q, self.questions_list, self.counter, self.no_of_questions)

        self.self_valid = R.result_process(self.model_response_check_list_super_llm_q,  self.counter, self.no_of_questions)
        self.cross_valid = R.result_process(self.cross_valid_list,  6, self.no_of_questions)
        #The number of times the model itself believes it's correct. Cross Valid lists should be run through R, not RA
        #RA is doing a similarity analysis on the cross valid lists instead of doing a sentiment analysis
        #I've fixed the spider charts, but this is an even bigger issue

        #Not a pretty solution but I'll just ignore RA and send another call to R and change the model consistency bit at the bottom
        #The way the cross valid lists work I'll have to reorder them based on the LLM they're checking instead of the LLM doing the checking
        
        #self.cross_results_q = R.result_process(self.orignal_response_list_for_each_q_llm_q, self.model_response_check_list_super_llm_q, self.questions_list, self.counter, self.no_of_questions)

        #R is sent the self and cross valid stuff from process_questions (is this answer correct)
        #RA is sent the consistency stuff from process_answers (how similar are these responses)
        #Changed self.cross_valid_list to self.cross_valid_list[0], just so it doesn't throw an error. I'm not using those results anyway.
        self.results = RA.result_answers(self.orignal_response_list_for_each_q, self.model_response_check_list_super, self.questions_list, self.counter, self.no_of_questions, self.cross_valid_list[0])
        print("PRINTING MODEL")
        print(self.model)
        print("SELF.RESULTS")
        print(self.results)
        self.avg_score_seq = self.results['avg_score_seq']
        self.avg_score_leven = self.results['avg_score_leven']
        self.avg_score_jaccard = self.results['avg_score_jaccard']
        self.avg_score_cosine = self.results['avg_score_cosine']
        self.avg_score_indexes = self.results['avg_score_indexes']

        self.Avg_Sim_score = self.results['Avg_Sim_score']
        self.Min_Sim_score = self.results['Min_Sim_Score']
        self.Max_Sim_score = self.results['Max_Sim_Score']
        self.Median_Sim_score = self.results['Median_Sim_Score']
        self.Avg_score = self.results['Avg_score']
        
        self.Sim_Score_List_cross = self.results['Sim_Score_List_cross']

        # consistency_answers = 0
        # # results guaging
        # for i in range(len(self.Avg_Sim_score)):
        #     if self.Avg_Sim_score[i] > 80:
        #         consistency_answers =+ 1

        #if (consistency_answers / len(self.Avg_Sim_score)) > 0.8 and (self.self_valid / (int(self.counter) * self.no_of_questions)) > 0.8:
        if (self.cross_valid / (6 * self.no_of_questions)) > 0.8 and (self.self_valid / (int(self.counter) * self.no_of_questions)) > 0.8:
            self.consistency = 'Model is accurate'
        else:
            self.consistency = "Model is inaccurate"
        f = open("results.txt", 'a')
        print(self.consistency, file=f)
        f.write("Self Valid:")
        f.write(f"{self.self_valid} correct out of {int(self.counter) * self.no_of_questions} ({self.self_valid / (int(self.counter) * self.no_of_questions)})")
        f.write("Cross Valid:")
        f.write(f"{self.cross_valid} correct out of {6 * self.no_of_questions} ({self.cross_valid / (6 * self.no_of_questions)})")
        f.write("\n\n")
        f.close()
            
        return{
                'avg_score_seq': self.avg_score_seq,
                'avg_score_leven': self.avg_score_leven,
                'avg_score_jaccard': self.avg_score_jaccard,
                'avg_score_cosine': self.avg_score_cosine,
                'avg_score_indexes': self.avg_score_indexes,
                'Avg_Sim_score': self.Avg_Sim_score,
                'Min_Sim_score': self.Min_Sim_score,
                'Max_Sim_score': self.Max_Sim_score,
                'Median_Sim_score': self.Median_Sim_score,
                'Avg_score': self.Avg_score,
                'consistency': self.consistency,
                'Sim_Score_List_cross': self.Sim_Score_List_cross
        }