import datetime
from unittest import TestCase

from awehflow.templating import TemplateRenderer


class TestTemplateRenderer(TestCase):

    def test_render(self):
        template_renderer = TemplateRenderer()
        template = "Hello {{ target }}!"
        result = template_renderer.render(template, {'target': 'world'})
        self.assertEqual(result, "Hello world!")

    def test_load_custom_filters(self):
        template_renderer = TemplateRenderer()
        self.assertEqual(template_renderer.env.filters['format_date'], TemplateRenderer._TemplateRenderer__format_date)
        self.assertEqual(template_renderer.env.filters['day_delta'], TemplateRenderer._TemplateRenderer__day_delta)

    def test_format_date(self):
        reference_time = datetime.date(2019, 10, 22)
        self.assertEqual(TemplateRenderer._TemplateRenderer__format_date(reference_time, '%Y/%m/%d'), '2019/10/22')
        self.assertEqual(TemplateRenderer._TemplateRenderer__format_date(reference_time, '%Y-%m-%d'), '2019-10-22')

        reference_time = datetime.date(2017, 4, 3)
        self.assertEqual(TemplateRenderer._TemplateRenderer__format_date(reference_time, '%Y/%m/%d'), '2017/04/03')
        self.assertEqual(TemplateRenderer._TemplateRenderer__format_date(reference_time, '%Y-%m-%d'), '2017-04-03')

    def test_day_delta(self):
        reference_time = datetime.date(2019, 10, 22)

        self.assertEqual(TemplateRenderer._TemplateRenderer__day_delta(reference_time, 3), datetime.date(2019, 10, 25))
        self.assertEqual(TemplateRenderer._TemplateRenderer__day_delta(reference_time, -3), datetime.date(2019, 10, 19))

