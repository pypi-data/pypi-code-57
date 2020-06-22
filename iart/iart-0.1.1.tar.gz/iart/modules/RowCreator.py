import configparser
import sys
from collections import OrderedDict
from datetime import datetime, timedelta
from operator import itemgetter

import dateparser
import typer
from dateparser.search import search_dates

from modules import csvExporter, safetypy
from tqdm import tqdm

IGNORED_TYPES = ['smartfield', 'primeelement',
                 'section', 'category',
                 'element', 'information',
                 'information - media', 'information - ']
COMMON_DATA = ['AuditID', 'Name',
               'DateStarted', 'Percentage Score',
               'Score', 'Site', 'Area', 'Region',
               'Template Name']
DELIMITER = chr(255)
values = []
FAILED_DELIMITER = ' [F]'


class TemplateCreator:
    def __init__(self, template_id, sp, date_modified, date_before):
        self.sp = sp
        self.template_id = template_id
        self.most_recent_inspection = self.get_most_recent_inspection()
        self.inspection_json = sp.get_audit(self.most_recent_inspection)
        self.current_table = csvExporter.CsvExporter(self.inspection_json)
        inspection_as_list = self.current_table.convert_audit_to_table()
        self.inspection_as_list = [item for item in inspection_as_list if item[1] not in IGNORED_TYPES]
        self.prime_elements = self.map_prime_elements()
        self.inspection_list = sp.discover_audits(template_id=[template_id], modified_after=date_modified,
                                                  modified_before=date_before)
        self.all_inspections, self.full_combined = self.combine_inspections()
        self.csv_as_list = [
            {'AuditID': []},
            {'Name': []},
            {'DateStarted': []},
            {'DateCompleted': []},
            {'Percentage Score': []},
            {'Score': []},
            {'Site': []},
            {'Area': []},
            {'Region': []},
            {'Template Name': []}
        ]
        self.item_label_map, self.dict_label_map = self.map_item_id_to_label()

    def get_most_recent_inspection(self):
        list_of_inspections = self.sp.discover_audits(template_id=[self.template_id], limit=1, order='desc')
        if list_of_inspections is not None:
            if list_of_inspections['count'] > 0:
                return list_of_inspections['audits'][0]['audit_id']
        else:
            return None

    def combine_inspections(self):
        all_inspections = []
        full_inspections = []
        if self.inspection_list:
            inspection_pbar = tqdm(self.inspection_list['audits'])
            for inspection in inspection_pbar:
                audit_id = inspection['audit_id']
                inspection_pbar.set_description(f"Downloading {audit_id}")
                inspection_json = self.sp.get_audit(audit_id)
                current_table = csvExporter.CsvExporter(inspection_json)
                inspection_as_list = current_table.convert_audit_to_table()
                full_inspections.append(inspection_as_list)
                inspection_as_list = [item for item in inspection_as_list if item[1] not in IGNORED_TYPES]
                all_inspections.append(inspection_as_list)
            return all_inspections, full_inspections
        return None

    def map_prime_elements(self):
        prime_elements = {}
        list_of_prime_elements = [item for item in self.inspection_as_list if item[35] == 'primeelement']
        for pe in list_of_prime_elements:
            prime_elements[pe[14]] = pe[2]
        if prime_elements:
            return prime_elements
        else:
            return None

    def map_item_id_to_label(self):
        checked_dynamicfields = []
        inspection_as_list = self.inspection_as_list
        item_label_map = []
        dict_label_map = OrderedDict()
        count = 0
        for item in inspection_as_list:
            item_id = item[14]
            label = item[2]
            item_type = item[1]
            repeating_section = item[35]
            if item_type == 'dynamicfield':
                if item_id not in checked_dynamicfields:
                    rs_map = self.create_rs_map(item_id)
                    checked_dynamicfields.append(item_id)
                    self.csv_as_list.extend(rs_map)
                    continue
            elif repeating_section in ['']:
                count += 1
                rs_check = False
                new_row = {item_id: []}
                self.csv_as_list.append(new_row)
                item_label_map.append({item_id: {'order': count, 'label': label, 'rs': rs_check}})
                dict_label_map[item_id] = {'order': count, 'label': label, 'rs': rs_check, 'category': item[34]}
            else:
                pass

        return item_label_map, dict_label_map

    def create_rs_map(self, item_id):
        columns = []
        for inspection in self.all_inspections:
            this_inspections_prime_elements = [item for item in inspection if item[35] == 'primeelement'
                                               and item[1] not in IGNORED_TYPES]
            this_inspections_pe_dict = {}
            for pe in this_inspections_prime_elements:
                this_inspections_pe_dict[pe[2]] = pe[14]
            for row in inspection:
                if row[35] not in ['primeelement', '']:
                    parent_id = list(row[35])[0]
                    if parent_id == item_id:
                        # section_title = list(row[35])[1]
                        section_number = list(row[35])[2]
                        category = row[34]
                        category = (category[:50] + '..') if len(category) > 50 else category
                        question = row[2]
                        question = (question[:150] + '..') if len(question) > 150 else question
                        pm_item_id = this_inspections_pe_dict.get(question)
                        new_label = self.prime_elements.get(pm_item_id)
                        if new_label != question:
                            question = new_label
                        new_row_title = f'{category} {section_number} / {question}'
                        new_row = {new_row_title: []}
                        if new_row not in columns:
                            columns.append(new_row)
        return columns


class RowCreator:
    def __init__(self, inspection, sp, template):
        # self.audit_id = inspection['audit_id']
        # self.inspection_json = sp.get_audit(self.audit_id)
        # self.current_table = csvExporter.CsvExporter(self.inspection_json)
        # inspection_as_list = self.current_table.convert_audit_to_table()
        full_combined_inspection = inspection
        self.inspection_as_list = [item for item in full_combined_inspection if item[1] not in IGNORED_TYPES]
        self.list_of_prime_elements = [item for item in full_combined_inspection if item[35] == 'primeelement']
        self.template_prime_elements = template.prime_elements
        self.csv_as_list = template.csv_as_list
        self.mapped_to_list = self.col_to_value()

    def col_to_value(self):
        list_of_prime_elements = self.list_of_prime_elements
        for row in self.csv_as_list:
            response_found = False
            item_id = list(row.keys())[0]
            if item_id in COMMON_DATA:
                item_values = self.inspection_as_list[0]
                common_data_dict = {'AuditID': item_values[29],
                                    'Name': item_values[21],
                                    'DateStarted': item_values[26],
                                    'DateCompleted': item_values[28],
                                    'Percentage Score': item_values[25],
                                    'Score': item_values[22],
                                    'Site': item_values[42],
                                    'Area': item_values[43],
                                    'Region': item_values[44],
                                    'Template Name': item_values[31]
                                    }
                common_response = common_data_dict.get(item_id)
                row[item_id].append(common_response)
                response_found = True
            else:
                search_inspection = [item for item in self.inspection_as_list if item[14] == item_id]
                if search_inspection:
                    response = search_inspection[0][3]
                    failed_status = search_inspection[0][12]
                    if failed_status is True:
                        response += FAILED_DELIMITER
                    row[item_id].append(response)
                    response_found = True
                else:
                    for item in self.inspection_as_list:
                        if item[35] not in ['primeelement', '']:
                            parent_id = list(item[35])[0]
                            section_title = list(item[35])[1]
                            section_number = list(item[35])[2]
                            category = item[34]
                            category = (category[:50] + '..') if len(category) > 50 else category
                            question = item[2]
                            question = (question[:150] + '..') if len(question) > 150 else question
                            response = item[3]
                            for primeelement in list_of_prime_elements:
                                if primeelement[2] == question:
                                    if question != self.template_prime_elements.get(primeelement[14]):
                                        question = self.template_prime_elements.get(primeelement[14])
                            new_row_title = f'{category} {section_number} / {question}'
                            if new_row_title == item_id and response_found is False:
                                row[item_id].append(response)
                                response_found = True
            if response_found is False:
                row[item_id].append('')
        return self.csv_as_list


class ConfigSetup:
    def __init__(self):
        self.config = self.get_config()
        self.sp = self.register_token()
        if self.sp:
            self.token = self.config['options']['token']
            self.templates = self.get_templates()
            self.file_format = self.config['options']['export_format']
            self.to_search = self.config['options']['to_search']
            self.parsed_date = self.date_parser()
            self.before, self.after = self.get_dates_to_search()
            self.template_lookup = self.get_formatted_list_of_templates()

    def get_templates(self):
        if self.config['options']['templates'] is None:
            return []
        if ',' in str(self.config['options']['templates']):
            templates = self.config['options']['templates'].split(',')
        else:
            templates = [self.config['options']['templates']]
        return templates

    @staticmethod
    def get_config():
        config = configparser.ConfigParser()
        config.read('config.ini')
        if config.sections():
            return config
        else:
            return None

    def register_token(self):
        config = self.config
        if self.config:
            if 'options' in config:
                if 'token' in config['options']:
                    sp = safetypy.SafetyCulture(config['options']['token'])
                    return sp
        else:
            print('No API Token found. Run interactive set up first.')
            return None

    def get_list_of_templates(self):
        list_of_templates = self.sp.discover_templates()
        if list_of_templates is not None:
            list_of_templates = list_of_templates['templates']
            return list_of_templates
        else:
            return None

    def get_formatted_list_of_templates(self):
        all_templates = self.get_list_of_templates()
        all_templates = sorted(all_templates, key=itemgetter('modified_at'), reverse=True)
        template_list = [{'value': 'all', 'name': 'Export All', 'checked': True}]
        if all_templates:
            for template in all_templates:
                if len(template_list) > 20:
                    break
                else:
                    if template['name'] == '':
                        name = 'Untitled template'
                    else:
                        name = template['name'].strip()
                    template_id = template['template_id']
                    joined_name = f'{name} ({template_id})'
                    template_dict = {'value': template_id, 'name': joined_name, }
                    template_list.append(template_dict)
        else:
            template_list = None
        return template_list

    def date_parser(self):
        parsed_date = dateparser.parse(self.to_search)
        if not parsed_date:
            date = search_dates(self.to_search)
        else:
            date = parsed_date
        if not date:
            print('Unable to parse the data in your config file. Defaulting to 1 week ago.')
            date = datetime.now() - timedelta(weeks=1)
        return date

    def get_dates_to_search(self):
        before = datetime.now()
        after = before - timedelta(weeks=1)
        if self.parsed_date:
            if type(self.parsed_date) is list:
                for i, date_to_search in enumerate(self.parsed_date):
                    if i == 0:
                        after = date_to_search[1]
                    if i == 1:
                        before = date_to_search[1]
                    if i > 1:
                        print('More than 2 dates provided, only taking the first two.')
            else:
                after = self.parsed_date

            pretty_after_date = after.strftime(f"%A %d %B %Y at %X")
            pretty_after_date = typer.style(pretty_after_date, fg=typer.colors.GREEN, bold=True)
            pretty_before_date = before.strftime(f"%A %d %B %Y at %X")
            pretty_before_date = typer.style(pretty_before_date, fg=typer.colors.GREEN, bold=True)
            search_from_alert = f'Searching for inspections completed after ' \
                                f'{pretty_after_date} until {pretty_before_date} '
            typer.echo(search_from_alert)
        else:
            print('Either unable to parse date or no date provided. Defaulting to 1 week ago.')
        return before, after
