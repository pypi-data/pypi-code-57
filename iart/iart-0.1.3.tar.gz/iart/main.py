import configparser
import time
from operator import itemgetter

import dateparser
import pandas as pd
import requests
import typer
import xlsxwriter
from PyInquirer import prompt
from dateparser.search import search_dates
from tqdm import tqdm
from xlsxwriter.utility import xl_col_to_name

from modules import safetypy
from modules.RowCreator import RowCreator, TemplateCreator, ConfigSetup

app = typer.Typer()

IGNORED_TYPES = ['smartfield', 'primeelement', 'section', 'category', 'element']
COMMON_DATA = ['AuditID', 'Name', 'DateStarted', 'Percentage Score', 'Score', 'Site', 'Area', 'Region',
               'Template Name']
DELIMITER = chr(255)
# values = []
FAILED_DELIMITER = ' [F]'


def create_excel_document(df, template_id, workbook):
    template_id = template_id[:30]
    worksheet = workbook.add_worksheet(template_id)
    label_col = 0

    template_as_list = df.values.tolist()
    columns_as_list = df.columns.values.tolist()
    response_col = len(columns_as_list) - 1

    # worksheet = workbook.add_worksheet(ft.sanitised_template_name)

    wrap_format = workbook.add_format({'text_wrap': 1})
    header_format = workbook.add_format({'text_wrap': 1, 'rotation': 30})
    failed_item_format = workbook.add_format({'bg_color': '#FFC7CE',
                                              'font_color': '#9C0006'})
    worksheet.set_row(0, 140)

    label_col_letter = xl_col_to_name(label_col)
    response_col_letter = xl_col_to_name(response_col)
    left_border = workbook.add_format()
    left_border.set_left()
    worksheet.set_column(f'{label_col_letter}:{response_col_letter}', 24, wrap_format)

    reformatted_columns = []
    for column in columns_as_list:
        current_row = {'header': column, 'header_format': header_format}
        reformatted_columns.append(current_row)

    table_length = len(template_as_list) + 1
    worksheet.add_table(f'{label_col_letter}1:{response_col_letter}{table_length}', {'name': template_id,
                                                                                     'data': template_as_list,
                                                                                     'columns': reformatted_columns,
                                                                                     'banded_rows': 0,
                                                                                     'banded_columns': 1
                                                                                     })

    worksheet.conditional_format(f'{label_col_letter}1:{response_col_letter}{table_length}',
                                 {'type': 'text',
                                  'criteria': 'containing',
                                  'value': FAILED_DELIMITER,
                                  'format': failed_item_format})


def look_up_col_name(template, column, duplicate_col_check):
    check = template.dict_label_map.get(column)
    if check:
        check_label = check['label'].strip()
        category = check['category'].strip()[:40]
        check_label = " ".join(check_label.split()).strip()
        col_label = (check_label[:200] + '..') if len(check_label) > 200 else check_label
        if category:
            col_label = f'{col_label} ({category})'
        if col_label not in duplicate_col_check:
            duplicate_col_check[col_label] = 1
        else:
            duplicate_col_check[col_label] += 1
            col_label = f"{col_label} ({duplicate_col_check[col_label]})"
        return col_label
    else:
        return column


def rename_cols(df, template, duplicate_col_check):
    for column in tqdm(df.columns):
        rename_to = look_up_col_name(template, column, duplicate_col_check)
        if rename_to != column:
            df.rename(columns={column: rename_to}, inplace=True)

    return df


def convert_to_dict(csv_as_list):
    csv_as_dict = {}

    print('Restructuring Output...')
    for row in tqdm(csv_as_list):
        key = list(row.keys())[0]
        row_values = list(row.values())[0]
        csv_as_dict[key] = row_values

    return csv_as_dict


def process_exports(date_modified, date_before, config):
    sp = config.sp
    list_of_templates = config.templates
    pretty_file_name = time.strftime("%Y-%m-%d at %H%M")
    if list_of_templates:
        if config.file_format == 'Excel':
            workbook = xlsxwriter.Workbook(f'{pretty_file_name}.xlsx')
        for template_id in list_of_templates:
            template_name = [t for t in config.template_lookup if t['value'] == template_id]
            if template_name:
                template_name = template_name[0]['name'].strip()
            else:
                template_name = template_id.strip()
            template_id = template_id.strip()
            styled_template_id = typer.style(template_name, fg=typer.colors.GREEN, bold=True)
            print(f'Beginning processing of {styled_template_id}')
            check_for_inspections = sp.discover_audits(template_id=[template_id], modified_after=date_modified,
                                                       modified_before=date_before, limit=1)
            if check_for_inspections['count'] != 0:
                template = TemplateCreator(template_id, sp, date_modified, date_before)
                inspection_count = len(template.inspection_list['audits'])
                if inspection_count > 0:
                    for inspection in template.full_combined:
                        RowCreator(inspection, sp, template)
                    # for inspection in template.inspection_list['audits']:
                    #     RowCreator(inspection, sp, template)
                    csv_as_dict = convert_to_dict(template.csv_as_list)
                    df = pd.DataFrame(csv_as_dict)
                    print('Renaming Columns...')
                    duplicate_col_check = {}
                    df = rename_cols(df, template, duplicate_col_check)
                    if config.file_format == 'Excel':
                        print('Creating Excel Document...')
                        create_excel_document(df, template_id, workbook)
                    elif config.file_format == 'CSV':
                        df.to_csv(f'{template_name}.csv')
                    print(f'Processing of {styled_template_id} completed.')
                else:
                    print(f'Nothing to export for {styled_template_id}')
                    continue
            else:
                print(f'Nothing to export for {styled_template_id}')
                continue
        if config.file_format == 'Excel':
            workbook.close()
    else:
        typer.echo('No templates specified, you must specify at least one.')
        interactive_setup()


def ask_for_date():
    date_choice = [
        {
            'type': 'list',
            'name': 'date_modified',
            'message': 'Select the date range to export each time the script runs. All times are relative to the '
                       'current date.',
            'choices': [
                '1 Week',
                '2 Weeks',
                '3 Weeks',
                '1 Month',
                'Custom'
            ]
        }
    ]
    answers = prompt(date_choice)

    custom_date_choice = [
        {
            'type': 'input',
            'name': 'custom_date',
            'message': 'What date range to use?'
        }
    ]
    if answers['date_modified'] == 'Custom':
        date_choice = prompt(custom_date_choice)
        date_input = date_choice['custom_date']
        # parsed_date = dateparser.parse(date_input)
        string_searches = date_choice['custom_date']
    else:
        date_input = answers['date_modified']
        # parsed_date = dateparser.parse(date_input)
        string_searches = answers['date_modified']
    parsed_date = date_parser(date_input)
    return parsed_date, string_searches


def set_typer_colour(str_to_format, colour=typer.colors.GREEN, bold=True):
    if type(str_to_format) is str:
        formatted_string = typer.style(str_to_format, fg=colour, bold=bold)
        return formatted_string
    return str_to_format


def date_parser(date):
    parsed_date = dateparser.parse(date)
    if not parsed_date:
        date = search_dates(date)
    else:
        date = parsed_date
    if not date:
        print('The date provided cannot be parsed. Please try again.')
        ask_for_date()
    return date


def get_formatted_list_of_templates(token):
    sp = safetypy.SafetyCulture(token)
    all_templates = sp.discover_templates()
    if all_templates['count'] > 0:
        all_templates = sorted(all_templates['templates'], key=itemgetter('modified_at'), reverse=True)
        template_list = []
        if all_templates:
            for template in all_templates:
                if len(template_list) > 25:
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
    else:
        return ['No Templates Found.']


def interactive_login():
    login_questions = [
        {
            'type': 'input',
            'name': 'username',
            'message': 'Your iAuditor username (should be your email address.)'
        },
        {
            'type': 'password',
            'name': 'password',
            'message': 'Your iAuditor Password'
        }
    ]
    login = prompt(login_questions)
    username = login['username']
    password = login['password']
    generate_token_url = "https://api.safetyculture.io/auth"
    payload = {
        "username": username,
        "password": password,
        "grant_type": "password"
    }
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
    }
    response = requests.request("POST", generate_token_url, data=payload, headers=headers)
    if response.status_code == requests.codes.ok:
        typer.echo('Token successfully obtained, continuing to export.')
        return response.json()['access_token']
    else:
        print('An error occurred calling ' + generate_token_url + ': ' + str(response.json()))
        interactive_login()


@app.command()
def interactive_setup():

    iauditor_reporting_tool = set_typer_colour('iAuditor Reporting tool', colour=typer.colors.BRIGHT_MAGENTA,
                                               bold=True)
    api_token_str = set_typer_colour('API token', colour=typer.colors.BRIGHT_MAGENTA, bold=True)
    username_str = set_typer_colour('username', colour=typer.colors.BRIGHT_MAGENTA, bold=True)
    password_str = set_typer_colour('password', colour=typer.colors.BRIGHT_MAGENTA, bold=True)

    welcome = f'Welcome to the {iauditor_reporting_tool}. To get started, we need to generate an {api_token_str}.' \
              f' Please enter your {username_str} and {password_str}:'
    typer.echo(welcome)
    config = ConfigSetup()
    if not config.sp:
        token = interactive_login()
    else:
        overwrite_token = [
        {
            'type': 'confirm',
            'name': 'existing_token',
            'message': 'You already have an API token saved. Do you need to regenerate it?'
        }
        ]
        ask_to_overwrite_token = prompt(overwrite_token)
        if ask_to_overwrite_token['existing_token'] is True:
            token = interactive_login()
        else:
            token = config.token
    templates = get_formatted_list_of_templates(token)
    questions = [
        {
            'type': 'list',
            'name': 'export_format',
            'message': 'Which file format would you like to export?',
            'choices': [
                'Excel',
                'CSV'
            ]
        },
        {
            'type': 'checkbox',
            'name': 'templates',
            'message': 'Which templates to export?',
            'choices': templates
        }
    ]
    answers = prompt(questions)
    date_to_search, string_searches = ask_for_date()
    answers['to_search'] = string_searches
    answers['token'] = token
    answers['templates'] = ','.join(answers['templates'])
    new_config = configparser.ConfigParser()
    new_config['options'] = answers
    with open('config.ini', 'w') as configfile:
        new_config.write(configfile)
    config = ConfigSetup()
    process_exports(str(config.after), str(config.before), config)


@app.command()
def export():
    config = ConfigSetup()
    if config.config:
        typer.echo('Exporting using the same settings as last time.')
        process_exports(str(config.after), str(config.before), config)
    else:
        interactive_setup()


if __name__ == "__main__":
    app()
