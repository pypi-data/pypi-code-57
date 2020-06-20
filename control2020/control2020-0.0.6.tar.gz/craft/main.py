import dash
import dash_core_components as dcc
import dash_html_components as html
import control as ct
import control2020 as ct20
import sympy as sp
from dash.dependencies import Input, Output
from labo import BasicExperiment, BasicSystem

P = ct.TransferFunction([1], [1, 1, 1])
exp = BasicExperiment(BasicSystem(P))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# external_scripts = ['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML']

app = dash.Dash("Control Systems Observatory", external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Observatory'),
    html.Div(children="That is a proof of concept for a dynamic systems"),
    dcc.Input(id="sys", value="1/(s+3)"),
    dcc.Slider(id="k-range", value=1, min=1, max=10, step=0.01),
    html.Div(id="final-sys"),
    dcc.Graph(id='step-response'),
    html.Div(id="step-report"),
])


@app.callback(
    Output(component_id='final-sys', component_property='children'),
    [Input(component_id='sys', component_property='value')]
)
def update_plant(system):
    global P, K, H
    expr = sp.sympify(system)
    P = ct20.core.symbolic_transfer_function(expr)
    return str(ct.feedback(K*P, H))


@app.callback(
    [Output(component_id='step-response', component_property='figure'),
     Output(component_id='step-report', component_property='children')],
    [Input(component_id='sys', component_property='value'),
     Input(component_id='k-range', component_property='value')]
)
def update_step_response(system, new_k):
    global P, K, H
    expr = sp.sympify(system)
    P = ct20.core.symbolic_transfer_function(expr)
    K = ct.TransferFunction([new_k], [1])
    sys = ct.feedback(K * P, H)
    t, y = ct.step_response(sys)
    return {
        'data': [
            {'x': t, 'y': y, 'type': 'line', 'name': 'step'},
        ],
        'layout': {
            'title': 'System Step Response'
        }
    }, str(ct.step_info(sys))


if __name__ == '__main__':
    app.run_server(debug=True)