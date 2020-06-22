import matplotlib
matplotlib.use('Agg')
import warnings
warnings.filterwarnings("ignore")
import sklearn.manifold as sm
from time import localtime, strftime

from .composers.first_page_composer import FirstPageComposer
from .composers.pie_page_composer import PiePageComposer
from .composers.mds_page_composer import MdsPageComposer

class Rendering:
    def multidimentionnal_scaling(self, matrix, seed):
        # return numpy.random.random((len(matrix), 2))
        return sm.MDS(dissimilarity='precomputed', n_jobs=-1, random_state=seed).fit_transform(matrix.get_matrix())

    def __init__(self, tool_name):
        self.time = strftime("%a, %d %b %Y %H:%M:%S %Z", localtime())
        self.tool_name = tool_name

    def render(self, annotation, title, seed, scatter_plot, ordered_group_names, rescale_heatmap=False):
        matrix = annotation.get_matrix()

        composers = [FirstPageComposer(annotation, title, ordered_group_names, rescale_heatmap)]

        for group_name in ordered_group_names:
            composers.append(PiePageComposer(annotation, title, group_name))

        if scatter_plot:
            p_matrix = self.multidimentionnal_scaling(matrix.to_distance(), seed)
            if len(p_matrix) != len(matrix.get_file_names()):
                raise Exception("Ops! Something is went wrong with the MDS.")

            for group_name in ordered_group_names:
                composers.append(MdsPageComposer(p_matrix, annotation, group_name, title))

        return [composers[i].run(self.make_left_lower_page(),
                                 self.make_rigth_lower_page(i + 1))
                for i in range(len(composers))]

    def make_left_lower_page(self):
        return self.time + '; ' + self.tool_name

    def make_rigth_lower_page(self, page_number):
        return 'Page ' + str(page_number)
