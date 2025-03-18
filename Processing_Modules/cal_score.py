import difflib
import numpy as np
import Levenshtein

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


class Cal_Score:
    def calculate_score(self, model_response, response_to_be_checked):

        # initializations
        self.response_to_be_checked = response_to_be_checked.strip()
        self.model_response = model_response.strip()
        print("CAL_SCORE")
        print("PRINTING MODEL RESPONSE")
        print(self.model_response)
        print("PRINTING RESPONSE TO BE CHECKED")
        print(self.response_to_be_checked)
        
        if not self.response_to_be_checked and not self.model_response:
            self.score_seq_matcher = 0
            self.scaled_score_levenshtein = 0
            self.jaccard_similarity_score = 0
            self.cosine_score = 0
            
        else:
            # Calculate scores for the techniques

            # 100 - identical, 0 - different (scale)

            #Sequence Matcher
            self.seq = difflib.SequenceMatcher(None, self.response_to_be_checked, self.model_response)
            self.score_seq_matcher = round(self.seq.ratio() * 100, 2)
            print("\nCurrent Sequence Matcher response score: ")
            print(self.score_seq_matcher)

            #Levenshtein Distance
            self.Leven_distance = Levenshtein.distance(self.response_to_be_checked, self.model_response)
            self.score_levenshtein = 1 - (self.Leven_distance / np.max([len(self.response_to_be_checked), len(self.model_response)]))
            self.scaled_score_levenshtein = round(self.score_levenshtein * 100, 2)
            print("\nCurrent Levenshtein Index: ")
            print(self.scaled_score_levenshtein)


            #Jaccard Index
            self.set_response_to_be_checked = set(self.response_to_be_checked)
            self.set_model_response = set(self.model_response)
            self.intersection = len(self.set_response_to_be_checked.intersection(self.set_model_response))
            self.union = len(self.set_response_to_be_checked.union(self.set_model_response))
            self.jaccard_index = self.intersection / self.union
            self.jaccard_similarity_score = round(self.jaccard_index * 100, 2)
            print("\nCurrent Jaccard Index: ")
            print(self.jaccard_similarity_score)

            #Cosine Similiarity
            self.vectorizer = CountVectorizer().fit_transform([self.response_to_be_checked, self.model_response])
            self.vectors = self.vectorizer.toarray()
            self.cosine_sim = cosine_similarity([self.vectors[0]], [self.vectors[1]])[0][0]
            self.cosine_score = round(self.cosine_sim * 100, 2)
            print("\nCurrent Cosine Similiarity score: ")
            print(self.cosine_score)

        # return results
        print("SIMILARITY SCORES")
        print(self.score_seq_matcher)
        print(self.scaled_score_levenshtein)
        print(self.jaccard_similarity_score)
        print(self.cosine_score)
        return self.score_seq_matcher, self.scaled_score_levenshtein, self.jaccard_similarity_score, self.cosine_score