from Processing_Modules.get_similarity_score import Sim_Score


Sim_Score = Sim_Score()

class Similarity_Lists:
    def get_sim_score(self, seq_score_list, leven_score_list, jaccard_score_list, cosine_score_list, avg_score_list):

        # initializations
        self.seq_score_list = seq_score_list
        self.leven_score_list = leven_score_list
        self.jaccard_score_list = jaccard_score_list
        self.cosine_score_list = cosine_score_list
        self.avg_score_list = avg_score_list
        self.n = len(seq_score_list)

        print("GET_SIM_SCORE")
        print(self.n)
        print("SHOULD BE EQUAL TO NUM REPETITIONS")
    
        self.similarity_score = 0
        self.x_axis = []
        self.similarity_score_list = []

        # Similarity scores stored in in the list
        for i in range(self.n):
            self.similarity_score = Sim_Score.get_similarity_score(self.seq_score_list[i], self.leven_score_list[i], self.jaccard_score_list[i], self.cosine_score_list[i])
            self.similarity_score_list.append(self.similarity_score)

        #print(self.similarity_score_list)
        self.avg_sim_score = round(sum(self.similarity_score_list) / len (self.similarity_score_list), 2)

        # return lists
        return{
                'Sim_Score_List': self.similarity_score_list,
                'Sim_Score': self.avg_sim_score,
    }