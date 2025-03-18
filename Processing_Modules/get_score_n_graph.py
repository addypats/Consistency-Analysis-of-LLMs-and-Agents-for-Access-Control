from Processing_Modules.cal_score import Cal_Score

CS = Cal_Score()


class Score_and_Graph:

    def get_scores_and_graphs_ChatGPT_modified(self, model_response, model_response_list):

        # initializations
        self.model_response = model_response
        self.model_response_list = model_response_list

        self.score_seq = 0
        self.score_lev = 0
        self.score_jaccard = 0
        self.score_cosine = 0
        self.avg_score_indexes = 0

        self.seq_score_list = []
        self.leven_score_list = []
        self.jaccard_score_list = []
        self.cosine_score_list = []
        self.avg_score_list = []

        self.n = len(model_response_list)

        # print("\n\n------------------Processing check - 1 ------------------\n\n")

        # run loop for the number of elements in the model_response_list
        for self.i in range(self.n):

            # get the techniques scores
            self.curr_score_seq, self.curr_score_levenshtein, self.curr_score_jaccard, self.curr_score_cosine = CS.calculate_score(self.model_response, self.model_response_list[self.i])

            #calculate average score for the techniques
            self.avg_score_temp = (self.curr_score_seq + self.curr_score_levenshtein + self.curr_score_jaccard + self.curr_score_cosine) / 4

            # Enter scores in list for graphs
            self.seq_score_list.append(self.curr_score_seq)
            self.leven_score_list.append(self.curr_score_levenshtein)
            self.jaccard_score_list.append(self.curr_score_jaccard)
            self.cosine_score_list.append(self.curr_score_cosine)

            #calculate avg score of lists
            self.avg_score_list.append(self.avg_score_temp)
        
        # calculate the average score for each technique 
        print("PRINTING SELF.N FOLLOWED BY SCORE LISTS")
        print(self.n)
        print(self.seq_score_list)
        print(self.leven_score_list)
        print(self.jaccard_score_list)
        print(self.cosine_score_list)
        print(self.avg_score_list)
        self.score_seq = sum(self.seq_score_list)
        self.score_lev = sum(self.leven_score_list)
        self.score_jaccard = sum(self.jaccard_score_list)
        self.score_cosine = sum(self.cosine_score_list)
        self.avg_score_indexes_sum = sum(self.avg_score_list)
        
        self.avg_score_indexes = round(self.avg_score_indexes_sum / self.n, 2)
        self.avg_score_seq = round(self.score_seq / self.n, 2)
        self.avg_score_leven = round(self.score_lev / self.n, 2)
        self.avg_score_jaccard = round(self.score_jaccard / self.n, 2)
        self.avg_score_cosine = round(self.score_cosine / self.n, 2)
        
        # print("\n\n------------------Processing check - 2 ------------------\n\n")

        # print("\n\n------------------Processing check - 3 ------------------\n\n")

        # return results
        return{
                'seq_score_list': self.seq_score_list,
                'leven_score_list': self.leven_score_list,
                'jaccard_score_list': self.jaccard_score_list,
                'cosine_score_list': self.cosine_score_list,
                'avg_score_list': self.avg_score_list,
                'avg_score_seq': self.avg_score_seq,
                'avg_score_leven': self.avg_score_leven,
                'avg_score_jaccard': self.avg_score_jaccard,
                'avg_score_cosine': self.avg_score_cosine,
                'avg_score_indexes': self.avg_score_indexes
        }

    def get_scores_and_graphs_ChatGPT_modified_for_answers_Self_Valid(self, model_response_list):
        
        # initializations
        self.model_response_list = model_response_list

        self.score_seq = 0
        self.score_lev = 0
        self.score_jaccard = 0
        self.score_cosine = 0
        self.avg_score_indexes = 0

        self.seq_score_list = []
        self.leven_score_list = []
        self.jaccard_score_list = []
        self.cosine_score_list = []
        self.avg_score_list = []

        self.n = len(model_response_list)
        print("get_scores_and_graphs_ChatGPT_modified_for_answers_Self_Valid")
        print(self.n)
        print("THIS VALUE SHOULD BE THE NUMBER OF REPETITIONS")

        print("PRINTING MODEL_RESPONSE_LIST")
        print(model_response_list)

        # print("\n\n------------------Processing check - 4 ------------------\n\n")

        # run loop for one less number of elements in the model_response_list for pair to pair comparison
        f = open("smalllog.txt", "a")
        print(self.model_response_list, file=f)
        f.close()
        for self.i in range(self.n - 1):
            self.curr_score_seq, self.curr_score_levenshtein, self.curr_score_jaccard, self.curr_score_cosine = CS.calculate_score(self.model_response_list[self.i], self.model_response_list[self.i+1])

            self.avg_score_temp = (self.curr_score_seq + self.curr_score_levenshtein + self.curr_score_jaccard + self.curr_score_cosine) / 4

            # Enter scores in list for graphs
            self.seq_score_list.append(self.curr_score_seq)
            self.leven_score_list.append(self.curr_score_levenshtein)
            self.jaccard_score_list.append(self.curr_score_jaccard)
            self.cosine_score_list.append(self.curr_score_cosine)

            #calculate avg score of lists
            self.avg_score_list.append(self.avg_score_temp)
            
        # calculate the average score for each technique 
        print("PRINTING SELF.N FOLLOWED BY SCORE LISTS")
        print("SELF VALID")
        print(self.n)
        print(self.seq_score_list)
        print(self.leven_score_list)
        print(self.jaccard_score_list)
        print(self.cosine_score_list)
        print(self.avg_score_list)
        self.score_seq = sum(self.seq_score_list)
        self.score_lev = sum(self.leven_score_list)
        self.score_jaccard = sum(self.jaccard_score_list)
        self.score_cosine = sum(self.cosine_score_list)
        self.avg_score_indexes_sum = sum(self.avg_score_list)
            
        self.avg_score_indexes = round(self.avg_score_indexes_sum / (self.n - 1), 2)
        self.avg_score_seq = round(self.score_seq / (self.n - 1), 2)
        self.avg_score_leven = round(self.score_lev / (self.n - 1), 2)
        self.avg_score_jaccard = round(self.score_jaccard / (self.n - 1), 2)
        self.avg_score_cosine = round(self.score_cosine / (self.n - 1), 2)
        
        # print("\n\n------------------Processing check - 5 ------------------\n\n")

        # print("\n\n------------------Processing check - 6 ------------------\n\n")

        # return results    
        return{
                'seq_score_list': self.seq_score_list,
                'leven_score_list': self.leven_score_list,
                'jaccard_score_list': self.jaccard_score_list,
                'cosine_score_list': self.cosine_score_list,
                'avg_score_list': self.avg_score_list,
                'avg_score_seq': self.avg_score_seq,
                'avg_score_leven': self.avg_score_leven,
                'avg_score_jaccard': self.avg_score_jaccard,
                'avg_score_cosine': self.avg_score_cosine,
                'avg_score_indexes': self.avg_score_indexes
        }
        
    def get_scores_and_graphs_ChatGPT_modified_for_answers_Cross_Valid(self, model_response_list, cross_valid_list):
        # initializations
        self.model_response_list = model_response_list
        self.cross_valid_list = cross_valid_list

        self.score_seq = 0
        self.score_lev = 0
        self.score_jaccard = 0
        self.score_cosine = 0
        self.avg_score_indexes = 0

        self.seq_score_list_cross = []
        self.leven_score_list_cross = []
        self.jaccard_score_list_cross = []
        self.cosine_score_list_cross = []
        self.avg_score_list_cross = []


        # print("\n\n------------------Processing check - 7 ------------------\n\n")

        
        self.n = len(model_response_list)
        
        for self.i in range(0, self.n):
            
            for self.j in range(2 * self.i, (2 * self.i) + 1):
                self.curr_score_seq, self.curr_score_levenshtein, self.curr_score_jaccard, self.curr_score_cosine = CS.calculate_score(self.model_response_list[self.i], self.cross_valid_list[self.j])

                self.avg_score_temp = (self.curr_score_seq + self.curr_score_levenshtein + self.curr_score_jaccard + self.curr_score_cosine) / 4

                # Enter scores in list for graphs
                self.seq_score_list_cross.append(self.curr_score_seq)
                self.leven_score_list_cross.append(self.curr_score_levenshtein)
                self.jaccard_score_list_cross.append(self.curr_score_jaccard)
                self.cosine_score_list_cross.append(self.curr_score_cosine)

                #calculate avg score of lists
                self.avg_score_list_cross.append(self.avg_score_temp)
        print("PRINTING SELF.N FOLLOWED BY SCORE LISTS")
        print("CROSS VALID")
        print(self.n)
        print(self.seq_score_list_cross)
        print(self.leven_score_list_cross)
        print(self.jaccard_score_list_cross)
        print(self.cosine_score_list_cross)
        print(self.avg_score_list_cross)
        # Return lists
        return{
                'avg_score_list_cross': self.avg_score_list_cross,
                'seq_score_list_cross': self.seq_score_list_cross,
                'leven_score_list_cross': self.leven_score_list_cross,
                'jaccard_score_list_cross': self.jaccard_score_list_cross,
                'cosine_score_list_cross': self.cosine_score_list_cross
        }