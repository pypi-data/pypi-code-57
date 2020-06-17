# -*- coding: utf-8 -*-

from eea.facetednavigation.interfaces import ICriteria

import logging


logger = logging.getLogger('eea.facetednavigation')


def criteria(self, sort=False, **kwargs):
    """ Process catalog query
    """
    if self.request:
        kwargs.update(self.request.form)

    # jQuery >= 1.4 adds type to params keys
    # $.param({ a: [2,3,4] }) // "a[]=2&a[]=3&a[]=4"
    # Let's fix this
    kwargs = dict(
        (key.replace('[]', ''), val)
        for key, val in kwargs.items()
    )

    logger.debug('REQUEST: %r', kwargs)

    # Generate the catalog query
    criteria = ICriteria(self.context)
    query = {}
    for cid, criterion in criteria.items():
        widget = criteria.widget(cid=cid)
        widget = widget(self.context, self.request, criterion)

        widget_query = widget.query(kwargs)
        if getattr(widget, 'faceted_field', False):
            widget_index = widget.data.get('index', '')
            if ('facet.field' in query and widget_index not in query['facet.field']):
                query['facet.field'].append(widget_index)
            else:
                query['facet.field'] = [widget_index]
        query.update(widget_query)

    # Add default sorting criteria
    if sort and 'sort_on' not in query:
        query['sort_on'] = 'effective'
        query['sort_order'] = 'reverse'

    if 'Language' in query:
        query.pop('Language')
    logger.debug('QUERY: %s', query)
    return query
