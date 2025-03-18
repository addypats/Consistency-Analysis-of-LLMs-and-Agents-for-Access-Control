import matplotlib.pyplot as plt
import numpy as np

class Cross_List_Graph:
    def Cross_List_Graph(self, cross_list):
        
        self.cross_list = cross_list
        
        # Determine the number of sublists and categories
        num_sublists = len(self.cross_list[0])
        num_bars = len(self.cross_list[0])  # assuming all sublists have the same length

        # Define the bar width and positions
        bar_width = 0.8 / num_sublists  # Adjust width so bars fit within the space
        index = np.arange(num_bars)

        print("INDEX ARANGE")
        print(index)

        # Create the figure and axis
        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot each sublist as a set of bars
        print("BROKEN CROSS LIST?")
        print(self.cross_list)
        
        self.i = 0
        for sublist in self.cross_list[0][0]:
            bar_positions = self.i + self.i * bar_width
            print("TESTING BAR CHART")
            print(bar_positions)
            print(sublist)
            print(bar_width)
            print(self.cross_list[0])
            ax.bar(bar_positions, sublist, bar_width, label=f'Sublist {self.i + 1}')
            self.i+=1

        # Add labels, title, and legend
        ax.set_xlabel('Categories')
        ax.set_ylabel('Values')
        ax.set_title('Combined Bar Chart of Different Lists')
        ax.set_xticks(index + bar_width * (num_sublists - 1) / 2)
        ax.set_xticklabels([f'Category {i + 1}' for i in range(num_bars)])
        ax.legend()

        # Show the plot
        plt.tight_layout()
        plt.show()
        
        pass