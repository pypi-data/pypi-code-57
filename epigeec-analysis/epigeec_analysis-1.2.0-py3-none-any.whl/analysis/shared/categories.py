class Categories(dict):
    def __init__(self, categories_dict):
        super(Categories, self).__init__(categories_dict)

    def obtain_file_names_with_tag_name(self, tag_name):
        return set(file_name for ca in self.values() 
                   for file_name in ca.obtain_file_names_with_tag_name(tag_name))

    def obtain_size_of_tags_in_category(self, category_name):
        return self[category_name].obtain_size_of_tags()

    def obtain_size_of_tags_from_tag_names(self, category_name, tag_names, file_names):
        return self[category_name].obtain_size_of_tags_from_tag_names(tag_names, file_names)

    def obtain_file_names_tag_names(self, category_name):
        return self[category_name].obtain_file_names_tag_names()

    def obtain_sorted_tags(self, category_name):
        return self[category_name].obtain_sorted_tags()

    @staticmethod
    def make_categories(metadata, file_names, categories_names):
        return Categories({category_name: Category.make_category(metadata, file_names, category_name)
                           for category_name in categories_names})

class Category:
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags

    def get_name(self):
        return self.name

    def get_tags(self):
        return self.tags

    def obtain_file_names_with_tag_name(self, tag_name):
        return self.tags.get(tag_name, Tag(tag_name, [])).get_file_names()

    def obtain_size_of_tags(self):
        return self.tags.obtain_size_of_tags()

    def obtain_size_of_tags_from_tag_names(self, tag_names, file_names):
        return self.tags.obtain_size_of_tags_from_tag_names(tag_names, set(file_names))

    def obtain_file_names_tag_names(self):
        return self.tags.obtain_file_names_tag_names()

    def obtain_sorted_tags(self):
        return sorted(sorted(self.tags.values(), key=lambda t: t.get_name()), key=lambda t: len(t), reverse=True)

    def make_flat_clusters(self, matrix):
        fn_flc = {}
        for idx, tag in enumerate(self.tags.values()):
            for file_name in tag.get_file_names():
                fn_flc[file_name] = idx

        return [fn_flc[fn] for fn in matrix.get_file_names()]

    def __len__(self):
        return len(self.tags)

    @staticmethod
    def make_category(metadata, file_names, category_name):
        return Category(category_name, Tags.make_tags(metadata.extract_tag_names_file_names(file_names, category_name)))

class Tags(dict):
    def __init__(self, tags_dict):
        super(Tags, self).__init__(tags_dict)

    def obtain_size_of_tags(self):
        return [(k, len(tag)) for k, tag in self.items()]

    def obtain_size_of_tags_from_tag_names(self, tag_names, file_names):
        return sum([self[tag_name].obtain_size_of_intersection(file_names)
                    for tag_name in tag_names
                    if tag_name in self])

    def obtain_file_names_tag_names(self):
        return dict([file_names_tag_names for tag in self.values() for file_names_tag_names in tag.obtain_file_names_tag_names()])

    @staticmethod
    def make_tags(tags_file_names):
        return Tags({tag: Tag(tag, file_names) for tag, file_names in tags_file_names.items()})

class Tag:
    def __init__(self, name, file_names):
        self.name = name
        self.file_names = file_names

    def get_name(self):
        return self.name

    def get_file_names(self):
        return self.file_names

    def obtain_file_names_tag_names(self):
        return [(file_name, self.name) for file_name in self.file_names]

    def obtain_size_of_intersection(self, file_names):
        return len(file_names.intersection(self.file_names))

    def __len__(self):
        return len(self.file_names)