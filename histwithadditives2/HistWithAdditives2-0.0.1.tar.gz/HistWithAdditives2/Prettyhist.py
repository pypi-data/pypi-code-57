import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter, FormatStrFormatter
from matplotlib import rcParams


class HistPlot():
    
    """A class for creating a well-labelled histogram.
    
    Attributes:
                col - the column to plot
                title - the title to the histogram
                fig_size - the size of the figure
                x_lab - the xlabel
                y_lab - the ylabel
                font_size - the fontsize of the chart
                bins_range - the range of bins intended to be created
    """
    def __init__(self):
    
        self.title = ''
        self.fig_size = ''
        self.x_lab = ''
        self.y_lab = ''
        self.font_size = ''
        self.bins_hist = ''
        self.data = []
    
        
    def get_variables(self, col_name, title_chart, size_chart, x_label, y_label, font_sz, bins_chart):
        
        """Method that gets all the inputs of the data based on user preferences.
        
        Args: 
                col_name-the column to plot
                title - the title of the chart
                fig_size - the size of the chart
                x_lab - the x label
                y_lab - the y label
                fontize - the fontsize of the text
                
        Returns:
                None
        """
        self.data = col_name.astype(float).tolist()
        self.title = title_chart
        self.fig_size = size_chart
        self.x_lab = x_label
        self.y_lab = y_label
        self.font_size = font_sz
        self.bins_hist = bins_chart
        
    def plot_histogram(self):
        """Method to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """


        # set data and title

        data = self.data



        title = self.title



        #set plotsize and bins

        fig, ax = plt.subplots(figsize=self.fig_size)

        counts, bins, patches = ax.hist(data,

                                        bins = self.bins_hist,

                                        color = '#17618C',

                                        edgecolor='silver')



        # Set the ticks to be at the edges of the bins.

        ax.set_xticks(bins)



        # Set the xaxis's tick labels to be formatted with 1 decimal place...

        ax.xaxis.set_major_formatter(FormatStrFormatter('%0.0f'))



        # hide spines

        ax.set_title('bottom-left spines')



        # Hide the right and top spines

        ax.spines['right'].set_visible(False)

        ax.spines['top'].set_visible(False)



        ax.spines['bottom'].set_color('gray')

        ax.spines['left'].set_color('gray')

        #ax.set_facecolor("dimgray")

        #Commas on the thousands figure

        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))



        #set y limit

        #ax.set_ylim(0,)



        # Label the raw counts and the percentages below the x-axis...

        bin_centers = 0.5 * np.diff(bins) + bins[:-1]

        for count, x in zip(counts, bin_centers):



            # Label the percentages

            percent = '%0.0f%%' % (100 * float(count) / counts.sum())

            ax.annotate(percent, xy=(x, 0.01), xycoords=('data', 'axes fraction'),

                        xytext=(0, 10), textcoords='offset points',

                        va='top', ha='center', color = "white", fontsize=10)



        # set individual bar lables using above list

        for i in ax.patches:

            ymin, ymax = ax.get_ylim()

            xmin, xmax = ax.get_xlim()

            # get_x pulls left  right; get_height pushes up or down

            ax.text(i.get_x()+ (xmin*-.5), i.get_height() + (ymax*0.025), \

                    str('{:,}'.format(int(i.get_height()))), fontsize=10, color='dimgray', rotation=0)



        # Give ourselves some more room at the bottom of the plot

        plt.subplots_adjust(bottom=0.3)



        # label axes

        plt.title(title, fontsize = 12, color = 'black')

        plt.xlabel(self.x_lab, fontsize=self.font_size, color = 'dimgray')

        plt.xticks(fontsize=12, color = 'dimgray')

        plt.ylabel(self.y_lab, fontsize = self.font_size, color = 'dimgray')

        plt.yticks(fontsize=10, color = 'dimgray')

        plt.show()

                