# -*- coding: utf-8 -*-

from eea.facetednavigation.browser.app.query import FacetedQueryHandler
from random import shuffle


class IdeaboxFacetedQueryHandler(FacetedQueryHandler):
    def query(self, *args, **kwargs):
        results = super(IdeaboxFacetedQueryHandler, self).query(*args, **kwargs)
        query = self.criteria()
        if "sort_on" in query and query["sort_on"] == "random_sort":
            results = [e for e in results]
            shuffle(results)
        return results
