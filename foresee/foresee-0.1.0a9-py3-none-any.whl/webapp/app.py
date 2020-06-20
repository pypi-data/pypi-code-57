"""
UI built using dash to perform basic tasks like uploading user data and setting proper parameters.
"""


import base64
import datetime
import io
import os
import sys
import pandas as pd

import flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from foresee.scripts import main

server = flask.Flask(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
					__name__,
					external_stylesheets=external_stylesheets,
					server=server,
					routes_pathname_prefix='/dash/'
				)


app.layout = html.Div([

	### prompt user to provide endog column name ###

	dcc.Markdown('''
	**Provide time series values column name. Default is "y".**
	'''),
	dcc.Input(id="endog-column", type="text", placeholder="time series column", value='y'),
	html.Br(),   

	### prompt user to provide id column name ###

	dcc.Markdown('''
	**If uploading more than one time series, provide an id column name. Default is "id".**
	'''),
	dcc.Input(id="id-column", type="text", placeholder="time series id column", value='id'),
	html.Br(),   

	### prompt user to provide date_stamp column name ###

	dcc.Markdown('''
	**Provide date stamp column name if available. Default is "date_stamp".**
	'''),
	dcc.Input(id="ds-column", type="text", placeholder="Date-Time column", value='date_stamp'),
	html.Br(),   

	### prompt user to provide time series frequency ###

	dcc.Markdown('''
	**Provide time series frequency. Default is 1.**
	'''),
	dcc.Input(id="ts-freq", type="number", placeholder='time series frequency', value=1),
	html.Br(),   

	### prompt user to provide forecast length ###

	dcc.Markdown('''
	**Provide forecast length. Default is 10.**
	'''),
	dcc.Input(id="fcst-length", type="number", placeholder='forecast horizon', value=10),
	html.Br(),   

	### prompt user to provide holdout length ###

	dcc.Markdown('''
	**If comparing model results, provide holdout length for out of sample
	forecast accuracy estimation. Default is 5.**
	'''),
	dcc.Input(id="holdout-length", type="number", placeholder='out of sample holdout len', value=5),
	html.Br(),   

	### display available output formats ###

	dcc.Markdown('''
	**Select result output format.**
	'''),
	dcc.RadioItems(
		id='result-format',
		options=[
			{'label': 'Best Model', 'value': 'best_model'},
			{'label': 'All Models', 'value': 'all_models'},
			{'label': 'All & Best', 'value': 'all_best'}
		],
		value='all_models',
		labelStyle={'display': 'inline-block'}
	),
	html.Br(),

	### display fit-forecast processing method (parallel/sequential) ###

	dcc.Markdown('''
	**Select fit-forecast processing method. Parallel execution with "dask" library.**
	'''),
	dcc.RadioItems(
		id='fit-execution-method',
		options=[
			{'label': 'Parallel', 'value': 'parallel'},
			{'label': 'Sequential', 'value': 'non_parallel'}
		],
		value='non_parallel',
		labelStyle={'display': 'inline-block'}
	),
	html.Br(),

	# display model list

	html.H5('Select or Remove Models'),

	dcc.Checklist(
		id='model-options',
		options=[
			{'label': 'EWM', 'value': 'ewm_model'},
			{'label': 'FFT', 'value': 'fft'},
			{'label': 'Holt Winters', 'value': 'holt_winters'},
			{'label': 'Prophet', 'value': 'prophet'},
			{'label': 'Sarimax', 'value': 'sarimax'}
		],
		value=['ewm_model', 'fft', 'holt_winters', 'prophet', 'sarimax'],
		labelStyle={'display': 'inline-block'}
	),

	html.Hr(),

	### upload file box ###

	dcc.Upload(
		id='upload-data',
		children=html.Div([
			html.H6('Column name (header) is required!!!'),
			'Drag and Drop or ',
			html.A('Select Files'),
		]),
		style={
			'width': '50%',
			'height': '100px',
			'lineHeight': '60px',
			'borderWidth': '1px',
			'borderStyle': 'dashed',
			'borderRadius': '5px',
			'textAlign': 'center',
			'margin': '10px'
		},
		multiple=True
	),

	### display a sample of input data ###

	html.Div(id='output-sample-data', style={'width': '50%'}),
	html.Br(),   

	### display final result dataframe ###

	html.Div(
		id='output-result',
		style={'width': '50%'}
	),
	html.Hr(),

])

### read user input
def read_contents(contents, ds_colname, filename):

	try:
		content_type, content_string = contents.split(',')
		decoded = base64.b64decode(content_string)

		if 'csv' in filename:
			# Assume that the user uploaded a CSV file
			df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

			if ds_colname in df.columns:
				df[ds_colname] = pd.to_datetime(df[ds_colname])

			return df

		elif 'xls' in filename:
			# Assume that the user uploaded an excel file
			df = pd.read_excel(io.BytesIO(decoded))

			if ds_colname in df.columns:
				df[ds_colname] = pd.to_datetime(df[ds_colname])

			return df

		else:
			# TODO: update this to read txt file
			# Assume that the user uploaded a txt file
			df = pd.read_csv(
				io.StringIO(decoded.decode('utf-8'))
			)
			if ds_colname in df.columns:
				df[ds_colname] = pd.to_datetime(df[ds_colname])

			return df

	except Exception as e:
		return str(e)

### display user input
def parse_contents(contents, ds_colname, filename):

	content = read_contents(contents, ds_colname, filename)

	if type(content) == type(pd.DataFrame()):
		try:
			df_info = [col + ': ' + str(content[col].dtype) for col in content.columns]
			df_info = [x + ' *** ' for x in df_info]
			df_info = '\n'.join([s for s in df_info])

			return html.Div([
				#TODO: fix linebreak
				dcc.Markdown(df_info),

				html.H6('Input data: ' + filename),
				dash_table.DataTable(

					data=content.to_dict('records'),
					columns=[{'name': i, 'id': i} for i in content.columns],
					page_action='none',
					style_table={'height': '200px', 'overflowY': 'auto'},

				),
				html.Hr(),
			])

		except Exception as e:
			return html.H6('Failed to display input data: ' + str(e))


	else:
		return html.H6('Failed to read input data: ' + content)




### display dataframe
def display_dataframe(df, name):

	if type(df) == type(pd.DataFrame()):
		return html.Div([
			html.H5(name),
			dash_table.DataTable(
				data=df.to_dict('records'),
				columns=[{'name': i, 'id': i} for i in df.columns],
				page_action='none',
				style_table={'height': '300px', 'overflowY': 'auto'},              
				export_columns = 'all',
				export_format = 'csv',
#                 filter_action='native',
			),
			html.Hr(),
		])

	else:
		return html.Div(['run failed with error : ' + str(df)])



### read input file, display a sample
@app.callback(Output('output-sample-data', 'children'),
			  [
				  Input('upload-data', 'contents'),
				  Input('ds-column', 'value'),
			  ],
			  [
				  State('upload-data', 'filename'),
			  ])

def update_output(content_list, ds_colname, filename_list):

	if content_list is not None:
		return parse_contents(content_list[0], ds_colname, filename_list[0])        


### read input file and parameters, display forecast results
@app.callback(Output('output-result', 'children'),
			  [
				  Input('endog-column', 'value'),
				  Input('id-column', 'value'),
				  Input('ds-column', 'value'),
				  Input('ts-freq', 'value'),
				  Input('fcst-length', 'value'),
				  Input('result-format', 'value'),
				  Input('holdout-length', 'value'),
				  Input('model-options', 'value'),
				  Input('upload-data', 'contents'),
				  Input('fit-execution-method', 'value')
			  ],
			  [State('upload-data', 'filename')])

def parse_result(
					endog_colname,
					gbkey,
					ds_colname,
					freq,
					fcst_length,
					run_type,
					holdout_length,
					model_list,
					content_list,
					processing_method,
					filename_list,
				):
	if content_list is not None:
		try:
			raw_fact = read_contents(content_list[0], ds_colname, filename_list[0])

			raw_fact_cols = raw_fact.columns

			#TODO: add flag for endog column

			if gbkey not in raw_fact_cols:
				gbkey = 'id'
			if ds_colname not in raw_fact_cols:
				ds_colname = 'date_stamp'
			if freq == '':
				freq = 1
			if fcst_length == '':
				fcst_length = 10
			if holdout_length == '':
				holdout_length = 5

			result, fit_result_list = main.collect_result(
																 raw_fact,
																 endog_colname,
																 gbkey,
																 ds_colname, 
																 freq, 
																 fcst_length, 
																 run_type, 
																 holdout_length,
																 model_list,
																 processing_method,
														)

			return display_dataframe(result, 'forecast result')

		except Exception as e:
			return display_dataframe(str(e), None)

# if __name__ == '__main__':
	# app.run_server(debug=True)
	