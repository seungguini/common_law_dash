import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

from utils import calculate_differences

"""
Create a grouped bar chart of annotation differences per each round
"""
NUM_GROUPS = 4

def create_chart(df, group_nos, category):
    figs = [
        go.Figure(
            data=[
                go.Bar(
                    name="Difference: " + str(difference),  # Dropdown category
                    x=df[df['group'] == group_no][df['difference'] == difference][df['category'] == category]['round'],
                    y=df[df['group'] == group_no][df['difference'] == difference][df['category'] == category]['value'],
                    offsetgroup=idx
                ) for idx, difference in enumerate(range(0, 5))
            ]
        ) for group_no in group_nos
    ]

    for fig in figs:
        fig.update_xaxes(title_text='Round')
        fig.update_yaxes(title_text='Count')

    return figs


# ===== BUILD BASE CHART =====

master_df = calculate_differences()
ANNOTATION_CATEGORIES = ['Appropriateness', 'Information content of outputs', 'Humanlikeness']

graphs = create_chart(master_df, range(1, NUM_GROUPS+1), 'Appropriateness')

# Filler for non-selected graphs
graphs += (NUM_GROUPS - len(graphs)) * [{}]  # or can use `[no_update]` here\

# ===== UPDATE AXES =====
#
# fig.update_xaxes(title_text='Round')
# fig.update_yaxes(title_text='Count')

print(master_df.size)
app = Dash(__name__)

server = app.server

app.layout = html.Div(children=[
    html.H1(children='Differences in Annotations per Round'),

    html.Div(children='''
        An interactive chart for Common Law Annotations
    '''),

    # Dropdown for group
    dcc.Dropdown(
        id='group-no-dropdown',
        options=[
            {
                'value': group_no,
                'label': 'Group ' + str(group_no)
            } for group_no in range(1, NUM_GROUPS+1)
        ],
        value=[1,2,3,4],  # Default value
        multi=True
    ),

    # Dropdown for category
    dcc.Dropdown(
        id='category-dropdown',
        options=ANNOTATION_CATEGORIES,
        value=ANNOTATION_CATEGORIES[0],  # Default value
        multi=True
    ),

    # Differences graphs
    dcc.Graph(id='differences-graph-1',figure=graphs[0]),
    dcc.Graph(id='differences-graph-2',figure=graphs[1]),
    dcc.Graph(id='differences-graph-3',figure=graphs[2]),
    dcc.Graph(id='differences-graph-4',figure=graphs[3]),


    # Store dropdown selection on local browser session
    dcc.Store(id='filter-store')

])


# ===== CALLBACKS FOR DROPDOWNS =====

# Store dropdown values to local session storage
@app.callback(
    Output('filter-store', 'data'),
    Input('group-no-dropdown', 'value'),
    Input('category-dropdown', 'value')
)
def update_dropdown_values(group_no, category):
    return {
        'group_no': group_no,
        'category': category
    }


@app.callback(
    Output('differences-graph-1', 'figure'),
    Output('differences-graph-2', 'figure'),
    Output('differences-graph-3', 'figure'),
    Output('differences-graph-4', 'figure'),

    Input('filter-store', 'data')
)
def update_category_chart(filter_json):
    graphs = create_chart(master_df, filter_json['group_no'], filter_json['category'])

    # Filler for non-selected graphs
    graphs += (NUM_GROUPS - len(graphs)) * [{}] # or can use `[no_update]` here\

    g1, g2, g3, g4 = graphs

    return g1, g2, g3, g4

if __name__ == '__main__':
    app.run_server(debug=True)
