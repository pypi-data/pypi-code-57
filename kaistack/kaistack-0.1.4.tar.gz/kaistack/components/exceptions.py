class MissingTemplateException(Exception):
    def __str__(self):
        return "There is no template"
