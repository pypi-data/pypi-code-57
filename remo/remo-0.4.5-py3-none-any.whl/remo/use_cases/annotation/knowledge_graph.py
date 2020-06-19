import requests

from django.conf import settings

from .open_images_categories import OPEN_IMAGES_CATEGORIES


def parse_open_images_categories(categories):
    result = {}
    for line in categories.splitlines():
        if not line:
            continue
        id, category = line.split(',')
        result[id] = category
        result[category] = id
    return result


class KnowledgeGraph:
    url = 'https://kgsearch.googleapis.com/v1/entities:search'
    default_params = {
        'limit': 1,
        'key': settings.KNOWLEDGE_GRAPH_API_KEY,
    }
    cache = parse_open_images_categories(OPEN_IMAGES_CATEGORIES)

    @staticmethod
    def search_category_id(category):
        category = str(category)
        category_id = KnowledgeGraph.cache.get(category)
        if category_id:
            return category_id

        if not settings.USE_KNOWLEDGE_GRAPH_API:
            return None

        result = KnowledgeGraph.search({'query': category})
        item = result.get('itemListElement')
        if item and len(item) > 0:
            category_id = str(item[0]['result']['@id']).replace('kg:', '')
            KnowledgeGraph.cache[category] = category_id
        return category_id

    @staticmethod
    def search(params):
        r = requests.get(KnowledgeGraph.url, params={**KnowledgeGraph.default_params, **params})
        return r.json()

    @staticmethod
    def search_category(category_id):
        category_id = str(category_id)
        category = KnowledgeGraph.cache.get(category_id)
        if category:
            return category

        if not settings.USE_KNOWLEDGE_GRAPH_API:
            return None

        result = KnowledgeGraph.search({'ids': category_id})
        item = result.get('itemListElement')
        if item and len(item) > 0:
            category = item[0]['result']['name']
            KnowledgeGraph.cache[category_id] = category

        return category
