class Sim_Score:

    def get_similarity_score(self, avg_score_seq, avg_score_Levenshtein, avg_score_Jaccard, avg_score_Cosine):

        # initializations
        self.avg_score_seq = avg_score_seq
        self.avg_score_Levenshtein = avg_score_Levenshtein
        self.avg_score_Jaccard = avg_score_Jaccard
        self.avg_score_Cosine = avg_score_Cosine
        
        print("A LIST?")
        print(self.avg_score_seq)

        # assign weights
        self.weights = {                    
            'seq_matcher': 0.2,              
            'lev_distance': 0.2,             
            'jaccard_similarity': 0.25,        
            'cosine_similarity': 0.35          
        }

        # calculate trust score
        self.trust_score = (self.weights['seq_matcher'] * float(self.avg_score_seq) +
                    self.weights['lev_distance'] * float(self.avg_score_Levenshtein) +
                    self.weights['jaccard_similarity'] * float(self.avg_score_Jaccard) +
                    self.weights['cosine_similarity'] * float(self.avg_score_Cosine))
        
        # return score
        return round(self.trust_score, 2)