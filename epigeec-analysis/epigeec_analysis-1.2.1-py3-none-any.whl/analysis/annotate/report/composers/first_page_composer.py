import matplotlib
matplotlib.use('Agg')
import warnings
warnings.filterwarnings("ignore")
import numpy
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
import pylab
from textwrap import TextWrapper
from analysis.annotate.report.composers.composer import Composer, USER, LegendMaker, PieChartsBuilder
from analysis.shared.clustering.scipypatch import ScipyPatch
from analysis.shared.util.labels import letter_label_to_int_label, int_label_to_letter_label

class FirstPageComposer(Composer):
    def __init__(self, annotation, title, ordered_group_names, rescale_heatmap):
        self.annotation = annotation
        self.title = title
        self.ordered_group_names = ordered_group_names
        self.rescale_heatmap = rescale_heatmap

    def run(self, left_lower_page, right_lower_page):
        ordered_matrix = self.annotation.get_matrix()

        if len(self.annotation) < 1785:
            scaling = 1785/float(len(self.annotation))
        else:
            scaling = 1

        matplotlib.rcParams['font.size'] = 14 * scaling * len(self.annotation)/1785
        m = len(self.annotation) * scaling
        n = (14 * m) / 8.5

        x_size = int(n * 5/4.)
        y_size = int(m * 5/4.)

        fig = pylab.figure(figsize=(x_size/100., y_size/100.), dpi=100.)
        axdendro = fig.add_axes([0.0,0.1,0.1,0.8])
        axdendro.axis('off')

        ScipyPatch.make_dendrogram(self.annotation.obtain_clusters(), self.annotation.get_matrix())
        axdendro.set_xticks([])
        axdendro.set_yticks([])

        # Plot distance matrix.
        axmatrix = fig.add_axes([0.11,0.1,0.4857142857,0.8])
        axmatrix.axis('off')

        if self.rescale_heatmap:
            vmin, vmax = None, None
        else:
            vmin, vmax = -1, 1

        im = axmatrix.matshow(ordered_matrix.get_matrix(), interpolation='nearest', cmap='RdBu_r', origin='upper', vmin=vmin, vmax=vmax)
        axmatrix.set_xticks([])
        axmatrix.set_yticks([])

        # User matrix line
        users_headers = self.annotation.obtain_file_names_with_tag_name(USER)
        users_line_pos = [-i for i, h in enumerate(ordered_matrix.get_file_names()) if h in users_headers]
        axuserline = fig.add_axes([0.5965, 0.1, 0.005, 0.8])
        axuserline.axis('off')
        # plt.eventplot(users_line_pos, orientation='vertical', colors=[self.user_color])
        plt.plot([1 for _ in range(len(users_line_pos))], users_line_pos, 'ro', markersize=matplotlib.rcParams['font.size']/2., color=LegendMaker.USER_COLOR)
        pylab.xlim([0.5, 1.5])
        pylab.ylim([-len(ordered_matrix)+1, 0])
        axuserline.set_xticks([])
        axuserline.set_yticks([])

        # Plot colorbar.
        axcolor = fig.add_axes([0.11,0.905,0.4857142857,0.025])
        pylab.colorbar(im, cax=axcolor, orientation='horizontal')
        axcolor.xaxis.set_ticks_position('top')
        pylab.title(self.title, fontsize=(matplotlib.rcParams['font.size'] * 4.2), y=2, loc='left')

        # Pie charts
        self._draw_aligned_piecharts(fig)

        # cluster id
        axcluster = fig.add_axes([0.102,0.1,0.005,0.8])
        axcluster.axis('off')
        self._align_cluster_labels(axcluster, scaling)
        axcluster.set_xticks([])
        axcluster.set_yticks([])

        # description
        self._draw_description(fig)

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

    def _draw_description(self, fig):
        formatted_description = '\n'.join(
            TextWrapper(
                width=140
            ).wrap(
                self.annotation.description))
        axdescription = fig.add_axes([0.11,0.015,0.4857142857,0.075])
        axdescription.text(0, 1, formatted_description, va='top', ha='left', clip_on=True, fontsize='large')
        axdescription.axis('off')
        axdescription.set_xticks([])
        axdescription.set_yticks([])

    def _compute_color_threshold(self, linkage_matrix, threshold):
        return linkage_matrix[-(threshold-1),2]

    def _draw_aligned_piecharts(self, fig):
        for column, group in enumerate(self.ordered_group_names[:3]):
            piecharts_builder = PieChartsBuilder()
            piecharts_builder.set_annotation(self.annotation)
            piecharts_builder.set_category_name(group)
            piecharts_builder.set_max_nb_tags(12)
            piecharts_builder.set_max_chars(30)

            piecharts = piecharts_builder.build()
        
            self._draw_piecharts_lines(fig, piecharts, column)
            self._draw_legend(fig, piecharts, column)

    def _draw_legend(self, fig, piecharts, col_pos):
        if len(piecharts) <= 20:
            axlegend = fig.add_axes([0.60 + (col_pos * 0.1), 0.0  , 0.1, 0.21])
            axlegend.axis('off')
            axlegend.set_xticks([])
            axlegend.set_yticks([])
            legend = plt.legend(handles=piecharts.get_handles(),
                                loc=2,
                                borderaxespad=0.,
                                title=piecharts.get_category_name())
            plt.setp(legend.get_title(), fontsize='xx-large')

    def _draw_piecharts_lines(self, fig, piecharts, column):
        nb_piecharts = len(piecharts)

        if nb_piecharts <= 10:
            line_a = reversed(range(nb_piecharts))
            line_b = range(0)
            stretch = 10 / float(nb_piecharts)
        elif nb_piecharts <= 20:
            side = nb_piecharts % 2 # 0 or 1
            line_a = reversed(range(1 - side, nb_piecharts, 2))
            line_b = reversed(range(0 + side, nb_piecharts, 2))
            stretch = 20 / float(nb_piecharts)

        if nb_piecharts <= 20:
            distance_between_charts = 0.07 * stretch
            first_axes = [0.60 + (column * 0.1), 0.215, 0.034, 0.056]
            second_axes = [0.64 + (column * 0.1), 0.235 + 0.020 * stretch, 0.034, 0.056]

            self._draw_piecharts_line(fig, piecharts, line_a, first_axes, distance_between_charts)
            self._draw_piecharts_line(fig, piecharts, line_b, second_axes, distance_between_charts)

    def _draw_piecharts_line(self, fig, piecharts, cluster_ids, axes, pos_inc):
        for pos, cluster_id in enumerate(cluster_ids):
            fig.add_axes([axes[0], axes[1] + (pos * pos_inc), axes[2], axes[3]])
            pylab.pie(piecharts.get_percents_for_cluster(cluster_id),
                      colors=piecharts.get_colors_for_cluster(cluster_id),
                      shadow=True)
            pylab.title(piecharts.get_title_for_cluster(cluster_id), y=0.95)

    def _align_cluster_labels(self, ax, scaling):
        total = len(self.annotation)
        clusters = self.annotation.obtain_clusters()

        total_px = total * scaling

        # caculate pixels position for text and repositionning
        px_pos = self._compute_text_pos(clusters, total_px, scaling)

        # compile text
        for cluster_id in range(1, len(clusters) + 1):
            ax.text(0.0, px_pos[cluster_id] / float(total_px), clusters[cluster_id].get_name(), fontsize='medium', family='monospace')

    def _compute_text_pos(self, clusters, total_px, scaling):
        before = total_px
        pos_before = total_px
        px_pos = {}
        for cluster_id in range(1, len(clusters) + 1):
            px_pos[cluster_id] = before - (len(clusters[cluster_id]) * scaling / 2)
            diff = (pos_before) - (px_pos[cluster_id] + matplotlib.rcParams['font.size'] + 2)
            if (diff < 0):
                px_pos[cluster_id] += diff
            pos_before = px_pos[cluster_id]
            before -= len(clusters[cluster_id]) * scaling

        return px_pos
