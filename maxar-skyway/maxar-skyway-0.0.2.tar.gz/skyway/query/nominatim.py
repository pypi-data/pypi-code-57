import typing
from collections import defaultdict
import collections.abc
import functools
import csv

from .filters import TagFilter, format_values
from .query import element_query_factory, reduce_union_or


def parse_feature_description(desc):
    tagmap = defaultdict(list)
    s = [_.strip().split("=") for _ in desc.split("OR")]
    for k, v in s:
        tagmap[k].append(v)
    return tagmap

def parse_feature_elements(elms, delim="_"):
    return [int(lev) for lev in elms.split(delim)]


def nominatim_from_csv(path):
    d = defaultdict(list)
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            d[row['FeatureName']].append(row['TagFilterDescription'])
            try:
                d[row['FeatureName']].append(row['Elements'])
            except KeyError:
                pass
    return d


class PrimaryFeature(typing.NamedTuple):
    name: str
    source_desc: str
    elements: collections.abc.Sequence = [1, 2, 3]

    @property
    def ElementQuery(self):
        return element_query_factory(parse_feature_elements(self.elements))

    @property
    def tag_profile(self):
        return dict(parse_feature_description(self.source_desc))

    def compile_QL(self, *args, **kwargs):
        wildkeys, tagkeys = [], []
        tagmap = self.tag_profile
        while tagmap:
            k, v = tagmap.popitem()
            if v == ['*']:
                wildkeys.append(k)
            else:
                tagkeys.append(TagFilter(k, vals=v))

        # format wildcard keys if exist
        tfs = []
        if wildkeys:
            if len(wildkeys) == 1:
                fargs = wildkeys.pop()
            else:
                fargs = format_values(wildkeys)
            tfs.append(TagFilter(fargs))
        tfs.extend(tagkeys)
        qs = [self.ElementQuery(filters=tf) for tf in tfs]
        return reduce_union_or(qs)


class Nominatim:
    def __init__(self, d):
        _nd = dict((k.replace(" ", "_"), PrimaryFeature(k, desc, elms)) for k, (desc, elms) in d.items())
        self._f = _nd.keys()
        self.__dict__.update(_nd)

    @property
    def feature_names(self):
        return self._f

    def __getitem__(self, fname):
        if fname not in self._f:
            raise KeyError("Feature {} not defined".format(fname))
        return getattr(self, fname)

    def desc(self):
        for n in self._f:
            pf = getattr(self, n)
            print(f'''{n}: {pf.compile_QL()}''')

    def _map_profiles_by_eqtype(self, *args):
        md = defaultdict(lambda: defaultdict(list))
        for fname in (args or self.feature_names):
            pf = self[fname]
            tpm = md[pf.ElementQuery]
            for tagkey, taglist in pf.tag_profile.items():
                tpm[tagkey].extend(taglist)
        return md

    def _consolidate_element_queries(self, *args):
        md = self._map_profiles_by_eqtype(*args)
        qlist = []
        for EQ, tpfs in md.items():
            tfs = [TagFilter(k, vals=vals) for k, vals in tpfs.items()]
            elmqs = [EQ(filters=tf) for tf in tfs]
            unioned = reduce_union_or(elmqs)
            qlist.append(unioned)
        return qlist

    def compress_feature_queries(self, *args):
        """
        Takes a number of feature names, groups their tag profiles by
        element query type and then by tag-key, then builds and unionizes the
        resulting queries element queries, potentially reducing the number of
        unions resulting from combining features with shared elements and tag-
        profile keys. This can result in more effcient queries than simply adding
        feature queries together, since it reduces IO by eliminating redundancy
        incurred via shared tag profiles and query types.

        If no arguments are passed, this function builds the compressed QL for the
        entire collection of the features defined on it.
        """

        qlist = self._consolidate_element_queries(*args)
        return reduce_union_or(qlist)

    @classmethod
    def from_csv(cls, path):
        d = nominatim_from_csv(path)
        return cls(d)

