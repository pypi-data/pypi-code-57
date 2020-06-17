from __future__ import division
import matplotlib
matplotlib.use('Agg')
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import pylab
import math
from analysis.shared.util.labels import letter_label_to_int_label, int_label_to_letter_label
from analysis.annotate.report.composers.composer import Composer, PieChartsBuilder

class PiePageComposer(Composer):
    def __init__(self, annotation, title, group_name):
        self.group_name = group_name
        self.title = title
        self.annotation = annotation

    def run(self, left_lower_page, right_lower_page):
        matplotlib.rcParams['font.size'] = 14
        y_size = 1080*2
        x_size = (14 * y_size) / 8.5

        fig = pylab.figure(figsize=(x_size/100., y_size/100.), dpi=100.)

        # title
        axtitle = fig.add_axes([0.1, 0.9, 0.8, 0.01])
        axtitle.axis('off')
        pylab.title(self.title, fontsize=56, loc='left')
        axtitle.set_xticks([])
        axtitle.set_yticks([])

        self._make_piecharts_grid(fig)

        #time and page
        axid = fig.add_axes([0., 0., 1., 0.015])
        axid.axis('off')
        axid.text(0.005, 0.25, left_lower_page)
        axid.text(0.995, 0.25, right_lower_page, ha='right')
        axid.set_xticks([])
        axid.set_yticks([])

        # Display and save figure.
        filename = self.tmp_name()
        fig.savefig(filename, format='png')
        return filename

    def _make_piecharts_grid(self, fig):
        piecharts_builder = PieChartsBuilder()
        piecharts_builder.set_annotation(self.annotation)
        piecharts_builder.set_category_name(self.group_name)
        piecharts_builder.set_max_nb_tags(20)
        piecharts_builder.set_max_chars(30)
        piecharts_builder.set_show_nb_tags(True)

        piecharts = piecharts_builder.build()

        self._draw_piecharts(fig, piecharts)

        self._draw_legend(fig, piecharts)

    def _draw_piecharts(self, fig, piecharts):
        lenght = len(piecharts)

        # when's only two piecharts (All and A),
        # the piecharts are too high
        # inside the frame of the page
        if lenght == 2:
            start_at = 1
        else:
            start_at = 0

        dim = int(math.ceil(math.sqrt(lenght - start_at)))
        i_dim = dim
        j_dim = dim
        for cluster_id in range(start_at, lenght):
            i = (cluster_id - start_at) % i_dim
            j = (cluster_id - start_at) // i_dim
            axpie = fig.add_axes([0.1 + (i * (0.60/float(i_dim))),
                                  0.9 - ((j + 1) * (0.8/float(j_dim))),
                                  0.9 * (0.4845/float(i_dim)),
                                  0.9 * (0.798/float(j_dim))])
            patches, texts, autotexts = pylab.pie(piecharts.get_percents_for_cluster(cluster_id),
                                                  colors=piecharts.get_colors_for_cluster(cluster_id),
                                                  shadow=True,
                                                  autopct='%1.0f%%',
                                                  pctdistance=1.15)

            for autotext in autotexts:
                autotext.set_fontsize('small')

            pylab.title(piecharts.get_title_for_cluster(cluster_id), fontsize='large')

    def _draw_legend(self, fig, piecharts):
        axlegend = fig.add_axes([0.7, 0.1, 0.25, 0.8])
        axlegend.axis('off')
        legend = plt.legend(handles=piecharts.get_handles(), loc=9, title=self.group_name)
        plt.setp(legend.get_title(), fontsize='xx-large')
        axlegend.set_xticks([])
        axlegend.set_yticks([])
