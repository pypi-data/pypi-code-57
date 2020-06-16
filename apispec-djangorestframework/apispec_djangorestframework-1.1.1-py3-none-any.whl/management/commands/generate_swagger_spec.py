# encoding: utf-8


import os

from django.core.management import BaseCommand

from apispec_drf.builder import APISpecDRF


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--output', nargs='?', default='api_docs_{version}.json')
        parser.add_argument('--preamble', nargs='?',
            help='Inject GitHub-flavored Markdown from this file into the auto-generated swagger spec'
        )
        parser.add_argument('--include-oauth2-security', default=False)
        parser.add_argument('--versions', nargs='*', default=['v1'])

    def handle(self, *args, **options):
        versions = options.get('versions')
        preamble_path = options.get('preamble')
        include_oauth2_security = options.get('include_oauth2_security')

        for version in versions:
            output_path = os.path.realpath(options['output'].format(version=version))

            dirname = os.path.dirname(output_path)
            if not os.path.exists(dirname):
                os.makedirs(output_path)
            preamble = None

            if preamble_path:
                with open(preamble_path.format(version=version)) as f:
                    preamble = f.read()

            with open(output_path, 'w') as spec_file:
                if options['verbosity'] > 0:
                    self.stdout.write("Generating '{}' spec in '{}'".format(version, output_path))
                spec = APISpecDRF(version=version, preamble=preamble, include_oauth2_security=include_oauth2_security)
                spec.write_to(spec_file)


