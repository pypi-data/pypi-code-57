from __future__ import generators
from six import string_types
import sys, os, tempfile
from itertools import cycle
import matplotlib
import matplotlib.patches as mpatches
import numpy
from collections import Counter
import string

OTHERS = 'Others'
USER = 'User'

class Composer:
    def run(self, filename, left_lower_page, right_lower_page):
        raise NotImplementedError('Composer.run() is an abstract method')

    def tmp_name(self):
        fd, temp_path = tempfile.mkstemp()
        os.close(fd)
        os.remove(temp_path)
        return temp_path


class LegendMaker:
    KELLY_COLORS = [(1.0, 0.7019607843137254, 0.0),
                    (0.5019607843137255, 0.24313725490196078, 0.4588235294117647),
                    (1.0, 0.40784313725490196, 0.0),
                    (0.6509803921568628, 0.7411764705882353, 0.8431372549019608),
                    (0.7568627450980392, 0.0, 0.12549019607843137),
                    (0.807843137254902, 0.6352941176470588, 0.3843137254901961),
                    (0.5058823529411764, 0.4392156862745098, 0.4),
                    (0.0, 0.49019607843137253, 0.20392156862745098),
                    (0.9647058823529412, 0.4627450980392157, 0.5568627450980392),
                    (0.0, 0.3254901960784314, 0.5411764705882353),
                    (1.0, 0.47843137254901963, 0.3607843137254902),
                    (0.3254901960784314, 0.21568627450980393, 0.47843137254901963),
                    (1.0, 0.5568627450980392, 0.0),
                    (0.7019607843137254, 0.1568627450980392, 0.3176470588235294),
                    (0.9568627450980393, 0.7843137254901961, 0.0),
                    (0.4980392156862745, 0.09411764705882353, 0.050980392156862744),
                    (0.5764705882352941, 0.6666666666666666, 0.0),
                    (0.34901960784313724, 0.2, 0.08235294117647059),
                    (0.9450980392156862, 0.22745098039215686, 0.07450980392156863),
                    (0.13725490196078433, 0.17254901960784313, 0.08627450980392157)]
    USER_COLOR = (0., 0.85, 0.85)

    @staticmethod
    def create_colors_dict(labels):
        rri = cycle(LegendMaker.KELLY_COLORS)
        colors = []

        for lbl in labels:
            if lbl == USER:
                colors.append((lbl, matplotlib.colors.rgb2hex(LegendMaker.USER_COLOR)))
            else:
                colors.append((lbl, matplotlib.colors.rgb2hex(next(rri))))

        return dict(colors)

    @staticmethod
    def create_patches(labels, colors_dict, formatted_labels):
        patches = []

        if USER in labels:
            patches.append(mpatches.Patch(color=colors_dict[USER], label=formatted_labels[USER]))

        patches += [mpatches.Patch(color=colors_dict[lbl], label=formatted_labels[lbl])
                   for lbl in labels
                   if lbl != USER]

        return patches

    @staticmethod
    def limit_chars(string, max_chars):
        if len(string) > max_chars:
            return string[:max_chars - 1] +  u'\0x2026'
        else:
            return string

    @staticmethod
    def make_composed_tags(tag_names, max_nb_tags):
        firsts = tag_names[:max_nb_tags - 1]
        lasts = tag_names[max_nb_tags - 1:]

        if USER in lasts:
            lasts.remove(USER)
            lasts.insert(0, firsts.pop())
            firsts.insert(0, USER)

        composed_tags = [(f, [f]) for f in firsts]

        if len(lasts) > 1:
            composed_tags += [('Others', lasts)]
        else:
            composed_tags += [(l, [l]) for l in lasts]

        return composed_tags

class ScatterPlot:
    def __init__(self, title, p_matrix, colors, handles):
        self.title = title
        self.handles = handles
        self.p_matrix = p_matrix
        self.colors = colors

    def get_title(self):
        return self.title

    def get_handles(self):
        return self.handles

    def get_p_matrix(self):
        return self.p_matrix

    def get_colors(self):
        return self.colors

    @staticmethod
    def make_tags_sp(category_name, p_matrix, annotation, max_nb_tags):
        tag_names_with_len = annotation.obtain_size_of_tags_in_category(category_name)
        tag_names_with_len.sort(key=lambda x: x[1], reverse=True)

        tag_names = [t for (t, _) in tag_names_with_len]

        composed_tags = LegendMaker.make_composed_tags(tag_names, max_nb_tags)
        labels = [c[0] for c in composed_tags]

        formatted_labels = {lbl:LegendMaker.limit_chars(lbl, 20) for lbl in labels}
        colors_dict = LegendMaker.create_colors_dict(labels)

        handles = LegendMaker.create_patches(labels, colors_dict, formatted_labels)

        composed_tags_dict = {tag:ct[0] for ct in composed_tags for tag in ct[1]}
        ordered_tag_names = annotation.obtain_ordered_tag_names(category_name)

        colors = [colors_dict[composed_tags_dict[tag_name]] for tag_name in ordered_tag_names]


        non_user_ids = [index
                        for index, tag_name in enumerate(ordered_tag_names)
                        if composed_tags_dict[tag_name] != USER]
        user_ids = [index
                    for index, tag_name in enumerate(ordered_tag_names)
                    if composed_tags_dict[tag_name] == USER]

        reordered_p_matrix = numpy.concatenate((p_matrix[non_user_ids], p_matrix[user_ids]))
        reordered_colors = [colors[idx] for idx in non_user_ids + user_ids]

        return ScatterPlot('Groups', reordered_p_matrix, reordered_colors, handles)

    @staticmethod
    def make_clusters_sp(p_matrix, annotation):
        cluster_ids = range(1, annotation.get_nb_clusters() + 1)

        formatted_labels = {cluster_id:annotation.obtain_cluster_name(cluster_id)
                            for cluster_id in cluster_ids}
        colors_dict = LegendMaker.create_colors_dict(cluster_ids)
        handles = LegendMaker.create_patches(cluster_ids, colors_dict, formatted_labels)

        colors = [colors_dict[cluster_id]
                  for cluster_id in annotation.make_flat_clusters()]

        return ScatterPlot('Clusters', p_matrix, colors, handles)

class PieChartsBuilder:
    def __init__(self):
        self.annotation = None
        self.category_name = None
        self.max_nb_tags = 0x7FFFFFFFFFFFFFFF # int64 max
        self.show_nb_tags = False
        self.max_chars = -1

    def build(self):
        if self.annotation is None or self.category_name is None:
            raise Exception('No annotation or no category_name passed')

        tag_names_with_len = self.annotation.obtain_size_of_tags_in_category(self.category_name)
        tag_names_with_len.sort(key=lambda x: x[1], reverse=True)

        tag_names = [t for (t, _) in tag_names_with_len]

        composed_tags = LegendMaker.make_composed_tags(tag_names, self.max_nb_tags)
        sizes = self._list_size_for_composed_tags(composed_tags, tag_names_with_len)
        formatted_labels = self._make_labels_for_tags(composed_tags, sizes)

        return PieCharts.make_piecharts(self.annotation, self.category_name, composed_tags, formatted_labels)

    def _make_labels_for_tags(self, composed_tags, sizes):
        if self.show_nb_tags:
            labels = map(lambda x, y: '(' + str(x) + ') ' + y[0], sizes, composed_tags)
        else:
            labels = [ct[0] for ct in composed_tags]

        if self.max_chars > 0:
            labels = [LegendMaker.limit_chars(lbl, self.max_chars) for lbl in labels]

        return {ct[0]: lbl for ct, lbl in zip(composed_tags, labels)}

    def _list_size_for_composed_tags(self, composed_tags, tag_names_with_len):
        lenghts = {x:y for x, y in tag_names_with_len}
        return [sum([lenghts[lbl]
                     for lbl in ct[1]])
                for ct in composed_tags]

    def set_annotation(self, annotation):
        self.annotation = annotation

    def set_category_name(self, category_name):
        self.category_name = category_name

    def set_max_nb_tags(self, max_nb_tags):
        self.max_nb_tags = max_nb_tags

    def set_show_nb_tags(self, show_nb_tags):
        self.show_nb_tags = show_nb_tags

    def set_max_chars(self, max_chars):
        self.max_chars = max_chars

class PieCharts(dict):
    def __init__(self, category_name, piecharts, handles):
        super(PieCharts, self).__init__(piecharts)
        self.category_name = category_name
        self.handles = handles

    def get_percents_for_cluster(self, cluster_id):
        return self[cluster_id].get_percents()

    def get_colors_for_cluster(self, cluster_id):
        return self[cluster_id].get_colors()

    def get_category_name(self):
        return self.category_name

    def get_handles(self):
        return self.handles

    def get_title_for_cluster(self, cluster_id):
        return self[cluster_id].get_title()

    @staticmethod
    def make_piecharts(annotation, category_name, composed_tags, formatted_labels):
        # Make dict of translation
        # create patch and color dict
        labels = [c[0] for c in composed_tags]
        colors_dict = LegendMaker.create_colors_dict(labels)
        handles = LegendMaker.create_patches(labels, colors_dict, formatted_labels)

        return PieCharts(category_name,
                         {cluster_id: PieChart.make_piechart(annotation, cluster_id, category_name, composed_tags, colors_dict)
                          for cluster_id in range(annotation.get_nb_clusters() + 1)},
                         handles)

class PieChart:
    def __init__(self, name, slices):
        self.name = name
        self.slices = slices

    def get_percents(self):
        return self.slices.get_percents()

    def get_title(self):
        return self.name + '=' + str(self.slices.get_total())

    def get_colors(self):
        return self.slices.get_colors()

    @staticmethod
    def make_piechart(annotation, cluster_id, category_name, composed_tags, colors_dict):
        return PieChart(annotation.obtain_cluster_name(cluster_id),
                        Slices.make_slices(annotation, cluster_id, category_name, composed_tags, colors_dict))

class Slices(list):
    def __init__(self, *args):
        super(Slices, self).__init__(*args)

    def get_percents(self):
        counts = [float(x.get_count()) for x in self]
        total = float(sum(counts))
        return [count/total for count in counts]

    def get_total(self):
        return sum([x.get_count() for x in self])

    def get_colors(self):
        return [x.get_color() for x in self]

    @staticmethod
    def make_slices(annotation, cluster_id, category_name, composed_tags, colors_dict):
        return Slices([Slice.make_slice(annotation, cluster_id, category_name, ct, colors_dict)
                       for ct in composed_tags
                       if annotation.obtain_size_of_tags_from_tag_names(cluster_id,
                                                                        category_name,
                                                                        ct[1]) > 0])

class Slice:
    def __init__(self, name, count, color):
        self.name = name
        self.color = color
        self.count = count

    def get_name(self):
        return self.name

    def get_count(self):
        return self.count

    def get_color(self):
        return self.color

    @staticmethod
    def make_slice(annotation, cluster_id, category_name, composed_tag, colors_dict):
        return Slice(composed_tag[0],
                     annotation.obtain_size_of_tags_from_tag_names(cluster_id, category_name, composed_tag[1]),
                     colors_dict[composed_tag[0]])
