class Cross_List_Split:
    def Cross_List_Split(self, Sim_Score_List_Cross):
        
        self.Sim_Score_List_Cross = Sim_Score_List_Cross
        print(self.Sim_Score_List_Cross)
        print("DOES THE LIST EXIST")
        
        # Change according to the number of LLMs
        self.size = 2
        
        return [self.Sim_Score_List_Cross[i:i + self.size] for i in range(0, len(self.Sim_Score_List_Cross), self.size)]