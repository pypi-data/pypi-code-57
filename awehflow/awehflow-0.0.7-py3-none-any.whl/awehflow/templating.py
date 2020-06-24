from datetime import timedelta

from jinja2 import Environment, BaseLoader


class TemplateRenderer:
    def __init__(self):
        self.env = Environment(autoescape=True, loader=BaseLoader())
        self.__load_custom_filters()

    def render(self, template_string, context):
        print('TemplateRenderer.render')
        print(self.env.filters)
        return self.env.from_string(template_string).render(context)

    def __load_custom_filters(self):
        self.env.filters['format_date'] = self.__format_date
        self.env.filters['day_delta'] = self.__day_delta

    @staticmethod
    def __format_date(datetime_obj, fmt):
        return datetime_obj.strftime(fmt)

    @staticmethod
    def __day_delta(datetime_obj, number_of_days):
        return datetime_obj + timedelta(number_of_days)
