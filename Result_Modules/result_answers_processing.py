# import modules
from Processing_Modules.get_sim_list import Similarity_Lists
from Processing_Modules.get_score_n_graph import Score_and_Graph


SG = Score_and_Graph()
SL = Similarity_Lists()


class Result_Answers:
    
    def result_answers(self, orignal_response_list_for_each_q, model_response_check_list_super, questions_list, counter, no_of_questions, cross_valid_list):
        
        # initializations
        self.orignal_response_list_for_each_q = orignal_response_list_for_each_q
        self.model_response_check_list_super = model_response_check_list_super
        self.questions_list = questions_list
        self.cross_valid_list = cross_valid_list
        self.no_of_questions = int(no_of_questions)
        self.counter = int(counter)

        print("RESULT_ANSWERS")
        print(self.no_of_questions)
        print(self.counter)


        self.seq_score_list = []
        self.leven_score_list = []
        self.jaccard_score_list = []
        self.cosine_score_list = []
        self.avg_score_list = []
        self.seq_score_list_cross = []
        self.leven_score_list_cross = []
        self.jaccard_score_list_cross = []
        self.cosine_score_list_cross = []
        self.avg_score_list_cross = []
        self.avg_score_seq = []
        self.avg_score_leven = []
        self.avg_score_jaccard = []
        self.avg_score_cosine = []
        self.avg_score_indexes = []
        self.Sim_score_list = []
        self.Avg_Sim_score = []
        self.Min_Sim_Score = []
        self.Max_Sim_Score = []
        self.Median_Sim_Score = []
        self.Sim_Score_List_cross = []

        # SELF VALIDATION
        # Run the loop for the number of times the user wants
        for i in range(self.no_of_questions):

            #Scores and graphs
            self.scores = SG.get_scores_and_graphs_ChatGPT_modified_for_answers_Self_Valid(self.model_response_check_list_super[i])

            # param list
            self.seq_score_list.append(self.scores['seq_score_list'])
            self.leven_score_list.append(self.scores['leven_score_list'])
            self.jaccard_score_list.append(self.scores['jaccard_score_list'])
            self.cosine_score_list.append(self.scores['cosine_score_list'])
            self.avg_score_list.append(self.scores['avg_score_list'])

            # graph lists to be displayed
            self.avg_score_seq.append(self.scores['avg_score_seq'])
            self.avg_score_leven.append(self.scores['avg_score_leven'])
            self.avg_score_jaccard.append(self.scores['avg_score_jaccard'])
            self.avg_score_cosine.append(self.scores['avg_score_cosine'])
            self.avg_score_indexes.append(self.scores['avg_score_indexes'])

            #call and get similarity lists
            self.plots = SL.get_sim_score(self.seq_score_list[i], self.leven_score_list[i], self.jaccard_score_list[i], self.cosine_score_list[i], self.avg_score_list[i])
            print("SELF.PLOTS")
            print(self.plots)
            self.Sim_score_list.append(self.plots['Sim_Score_List'])
            self.Avg_Sim_score.append(self.plots['Sim_Score'])

        # get average score
        self.Avg_score = sum(self.Avg_Sim_score) / len(self.Avg_Sim_score)

        # get the min, max, median for the lists
        for i in range(self.no_of_questions):
            self.Min_Sim_Score_temp = min(self.Sim_score_list[i])
            self.Min_Sim_Score.append(self.Min_Sim_Score_temp)
            self.Max_Sim_Score_temp = max(self.Sim_score_list[i])
            self.Max_Sim_Score.append(self.Max_Sim_Score_temp)
            self.sorted_list = sorted(self.Sim_score_list[i])
            self.Median_Sim_Score_temp = self.sorted_list[len(self.sorted_list)//2] if len(self.sorted_list) % 2 == 1 else sum(self.sorted_list[len(self.sorted_list)//2-1:len(self.sorted_list)//2+1])/2.0
            self.Median_Sim_Score.append(self.Median_Sim_Score_temp)
            
        
        # CROSS VALIDATION
        #Scores and graphs
        if not self.cross_valid_list:
            self.seq_score_list_cross.append([])
            self.leven_score_list_cross.append([])
            self.jaccard_score_list_cross.append([])
            self.cosine_score_list_cross.append([])
            self.avg_score_list_cross.append([])
            
        else:
            self.scores = SG.get_scores_and_graphs_ChatGPT_modified_for_answers_Cross_Valid(self.orignal_response_list_for_each_q, self.cross_valid_list)

            # param list
            self.seq_score_list_cross.append(self.scores['seq_score_list_cross'])
            self.leven_score_list_cross.append(self.scores['leven_score_list_cross'])
            self.jaccard_score_list_cross.append(self.scores['jaccard_score_list_cross'])
            self.cosine_score_list_cross.append(self.scores['cosine_score_list_cross'])
            self.avg_score_list_cross.append(self.scores['avg_score_list_cross'])

        
        self.plots = SL.get_sim_score(self.seq_score_list_cross[0], self.leven_score_list_cross[0], self.jaccard_score_list_cross[0], self.cosine_score_list_cross[0], self.avg_score_list_cross[0])
        self.Sim_Score_List_cross.append(self.plots['Sim_Score_List'])
        
        # return lists
        return{
                'avg_score_seq': self.avg_score_seq,
                'avg_score_leven': self.avg_score_leven,
                'avg_score_jaccard': self.avg_score_jaccard,
                'avg_score_cosine': self.avg_score_cosine,
                'avg_score_indexes': self.avg_score_indexes,
                'Avg_Sim_score': self.Avg_Sim_score,
                'Min_Sim_Score': self.Min_Sim_Score,
                'Max_Sim_Score': self.Max_Sim_Score,
                'Median_Sim_Score': self.Median_Sim_Score,
                'Avg_score': self.Avg_score,
                'Sim_Score_List_cross': self.Sim_Score_List_cross
        }