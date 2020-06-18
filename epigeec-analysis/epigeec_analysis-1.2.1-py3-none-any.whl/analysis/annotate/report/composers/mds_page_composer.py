from .composer import Composer, ScatterPlot
import warnings
warnings.filterwarnings("ignore")
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab

class MdsPageComposer(Composer):
    def __init__(self, p_matrix, annotation, group, title):
        self.p_matrix = p_matrix
        self.annotation = annotation
        self.group = group
        self.title = title

    def run(self, left_lower_page, right_lower_page):
        y_size = 1080*2
        x_size = (14 * y_size) / 8.5

        fig = pylab.figure(figsize=(x_size/100., y_size/100.), dpi=100.)

        axtitle = fig.add_axes([0.1, 0.9, 0.8, 0.01])
        axtitle.axis('off')
        pylab.title(self.title, fontsize=56, loc='left')
        axtitle.set_xticks([])
        axtitle.set_yticks([])

        axtitle = fig.add_axes([0.1, 0.870, 0.8, 0.01])
        axtitle.axis('off')
        pylab.title(self.group, fontsize=32, loc='left')
        axtitle.set_xticks([])
        axtitle.set_yticks([])

        self._group_scatter_plot(fig)
        self._cluster_scatter_plot(fig)

        #time and page
        axid = fig.add_axes([0., 0., 1., 0.015])
        axid.axis('off')
        axid.text(0.005, 0.25, left_lower_page)
        axid.text(0.995, 0.25, right_lower_page, ha='right')
        axid.set_xticks([])
        axid.set_yticks([])

        filename = self.tmp_name()
        plt.savefig(filename, format='png')
        return filename

    def _draw_scatter_plot(self, fig, axes, column, scatter_plot):
        p_matrix = scatter_plot.get_p_matrix()
        ax = fig.add_axes(axes)
        ax.scatter(p_matrix[:, 0],
                   p_matrix[:, 1],
                   s=100,
                   data=p_matrix,
                   cmap='rgb',
                   c=scatter_plot.get_colors())
        pylab.title(scatter_plot.get_title(),
                    fontsize='xx-large')
        plt.legend(handles=scatter_plot.get_handles(),
                   bbox_to_anchor=(0., -0.03),
                   loc=2,
                   ncol=column)

    def _group_scatter_plot(self, fig):
        self._draw_scatter_plot(fig,
                                [0.08, 0.15, .4, .6588235294],
                                3,
                                ScatterPlot.make_tags_sp(self.group,
                                                                  self.p_matrix,
                                                                  self.annotation,
                                                                  15))

    def _cluster_scatter_plot(self, fig):
        self._draw_scatter_plot(fig,
                                [0.52, 0.15, .4, .6588235294],
                                11,
                                ScatterPlot.make_clusters_sp(self.p_matrix,
                                                                      self.annotation))
