import environ

package_dir = environ.Path(__file__) - 1


def parse_categories():
    data = str(package_dir.path('imagenet_metadata.txt'))
    # Source:
    # https://raw.githubusercontent.com/tensorflow/models/master/research/inception/inception/data/imagenet_metadata.txt

    with open(data, 'r') as f:
        lines = f.readlines()

    result = {}
    for s in lines:
        tokens = s.strip().split('\t')
        id, categories = tokens[0], tokens[1].split(',')
        result[id] = categories
    return result


class ImagenetMetadata():
    categories = parse_categories()

    @staticmethod
    def search_category(category_id):
        return ImagenetMetadata.categories.get(str(category_id), [])
