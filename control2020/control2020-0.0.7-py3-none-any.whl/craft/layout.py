import dash_core_components as dcc
import dash_html_components as html


def feather_icon(name: str):
    return html.I(**{"data-feather": name})


functions = "mx-1 my-2 p-2 flex justify-between"
input_class = "px-2 py-1 ml-2 bg-indigo-100 rounded-md"

layout = html.Div(className="flex container justify-between mx-6 my-4 max-h-screen", children=[
    html.Div(children=[
        html.H1(className="text-3xl", children="System Observer"),
        html.H2(className="text-xl mt-3", children="System"),
        html.Div(children=[
            html.Div(className=functions, children=[
                html.Span(className="text-md", children="Plant"),
                dcc.Input(id="plant_raw", className=input_class, value="1/(s+3)"),
            ])
        ]),
        html.Div(children=[
            html.Div(className=functions, children=[
                html.Span(className="text-md", children="Controller"),
                dcc.Input(id="controller_raw", className=input_class, value="1"),
            ])
        ]),
        html.Div(children=[
            html.Div(className=functions, children=[
                html.Span(className="text-md", children="Feedback"),
                dcc.Input(id="feedback_raw", className=input_class, value="1"),
            ])
        ])
    ]),
    html.Div(className="relative max-h-full", children=[
        # html.Div(className="absolute h-3 w-3 bg-red-500"),
        html.Button(id="compute-btn", className="z-10", children=feather_icon("play")),
    ]),
    html.Div(className="max-h-full px-0", children=[
        dcc.Graph(id="time-plot"),
        dcc.Graph(id="freq-plot")
    ]),
])