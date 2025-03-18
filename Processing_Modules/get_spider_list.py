
class Spider_List:
    
    def Spider_List(self, avg_score_indexes, avg_score_seq, avg_score_leven, avg_score_jaccard, avg_score_cosine, no_of_questions):
        
        self.avg_score_indexes = avg_score_indexes
        self.avg_score_seq = avg_score_seq
        self.avg_score_leven = avg_score_leven
        self.avg_score_jaccard = avg_score_jaccard
        self.avg_score_cosine = avg_score_cosine
        self.no_of_questions = no_of_questions
        
        self.spider_list_total = []
                
        for self.i in range(self.no_of_questions):
            
            self.spider_list = []
            
            self.spider_list.append(avg_score_indexes[self.i])
            self.spider_list.append(avg_score_seq[self.i])
            self.spider_list.append(avg_score_leven[self.i])
            self.spider_list.append(avg_score_jaccard[self.i])
            self.spider_list.append(avg_score_cosine[self.i])
            
            self.spider_list_total.append(self.spider_list)
            
        print("SPIDER LIST")
        print(self.spider_list_total)
        
        return self.spider_list_total