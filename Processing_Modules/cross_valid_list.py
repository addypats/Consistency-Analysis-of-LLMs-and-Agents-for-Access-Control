from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
from Processing_Modules.cross_list_split import Cross_List_Split
from Processing_Modules.cross_list_graphs import Cross_List_Graph

CLP = Cross_List_Split()
CLG = Cross_List_Graph()

class Cross_Valid_List:
    def Cross_Valid_List(self, Sim_Score_List_cross_chat, Sim_Score_List_cross_meta, Sim_Score_List_cross_bloom, Sim_Score_List_cross_gemini, Sim_Score_List_cross_claude, Sim_Score_List_cross_cohere, Sim_Score_List_cross_llama):
        
        
        self.Sim_Score_List_cross_chat = Sim_Score_List_cross_chat
        self.Sim_Score_List_cross_meta = Sim_Score_List_cross_meta
        self.Sim_Score_List_cross_bloom = Sim_Score_List_cross_bloom
        self.Sim_Score_List_cross_gemini = Sim_Score_List_cross_gemini
        self.Sim_Score_List_cross_claude = Sim_Score_List_cross_claude
        self.Sim_Score_List_cross_cohere = Sim_Score_List_cross_cohere
        self.Sim_Score_List_cross_llama = Sim_Score_List_cross_llama
        
        self.chat_super_list = CLP.Cross_List_Split(self.Sim_Score_List_cross_chat)
        CLG.Cross_List_Graph(self.chat_super_list)
        self.meta_super_list = CLP.Cross_List_Split(self.Sim_Score_List_cross_meta)
        CLG.Cross_List_Graph(self.meta_super_list)

        self.bloom_super_list = CLP.Cross_List_Split(self.Sim_Score_List_cross_bloom)
        CLG.Cross_List_Graph(self.bloom_super_list)
        
        self.gemini_super_list = CLP.Cross_List_Split(self.Sim_Score_List_cross_gemini)
        CLG.Cross_List_Graph(self.gemini_super_list)
        
        self.claude_super_list = CLP.Cross_List_Split(self.Sim_Score_List_cross_claude)
        CLG.Cross_List_Graph(self.claude_super_list)
        
        self.cohere_super_list = CLP.Cross_List_Split(self.Sim_Score_List_cross_cohere)
        CLG.Cross_List_Graph(self.cohere_super_list)
        
        self.llama_super_list = CLP.Cross_List_Split(self.Sim_Score_List_cross_llama)
        CLG.Cross_List_Graph(self.llama_super_list)
        
        
        pass