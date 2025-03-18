import numpy as np
import matplotlib.pyplot as plt
from math import pi

class Spider_Charts:
    def Spider_Charts(self, labels, N, spider_list_total, no_of_questions, name):
        
        # Initializations
        self.labels = labels
        self.N = N
        self.spider_list_total = spider_list_total
        self.no_of_questions = no_of_questions
        
        # What will be the angle of each axis in the plot
        self.angles = [n / float(self.N) * 2 * pi for n in range(self.N)]
        self.angles += self.angles[:1]

        # Initialize the spider plot
        self.fig, self.ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        #self.ax.set_label(name)

        # Draw one axe per variable and add labels
        plt.xticks(self.angles[:-1], self.labels)

        # Draw ylabels
        self.ax.set_rlabel_position(0)
        #plt.yticks([1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"], color="grey", size=7)
        plt.ylim(0, 100)
        
        # Define colors for each question
        colourmap = plt.cm.get_cmap('tab20', no_of_questions)  # 'tab20' can generate up to 20 distinct colors, used repetitively
        
        # Plot data for each question
        for i in range(0, self.no_of_questions):
            self.values = self.spider_list_total[i]
            self.values += self.values[:1]
            colour = colourmap(i % 20)
            print("ANGLES")
            print(self.angles)
            print("VALUES")
            print(self.values)
            self.ax.plot(self.angles, self.values, linewidth=2, linestyle='solid',
                    label=f'Question {i+1}', color=colour)
            #Damn British People
            self.ax.fill(self.angles, self.values, color=colour, alpha=0.2)

        # Add legend
        self.ax.set_title(name, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

        plt.show()
        
        #return None
        pass