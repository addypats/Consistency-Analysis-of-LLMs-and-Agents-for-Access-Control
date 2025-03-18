from Processing_Modules.get_sim_list import Similarity_Lists
from Processing_Modules.get_score_n_graph import Score_and_Graph


SG = Score_and_Graph()
SL = Similarity_Lists()

class Result:
    def result_process(self, check_list, counter, no_of_questions):
        self.check_list = check_list
        self.counter = int(counter)
        self.no_of_questions = no_of_questions
        self.correctnum = 0
        for self.i in range(self.no_of_questions):
            for self.j in range(self.counter):
                if ("yes" in check_list[self.i][self.j].lower()):
                    self.correctnum += 1
        return self.correctnum