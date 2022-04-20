import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

from utils import calculate_differences

"""
Create a grouped bar chart of annotation differences per each round
"""

NUMBER_OF_GROUPS = 4

def create_chart(df, category):
    fig = make_subplots(
        rows=4,  # Group per row
        cols=1,  # Differences, distribution
        subplot_titles=(
            "Group 1: Differences in Annotations",# "Group 1: Distribution of Annotations (Total)",
            "Group 2: Differences in Annotations",# "Group 1: Distribution of Annotations (Total)",
            "Group 3: Differences in Annotations",# "Group 1: Distribution of Annotations (Total)",
            "Group 4: Differences in Annotations",# "Group 1: Distribution of Annotations (Total)",
        )
    )
    for idx, group_no in enumerate(range(NUMBER_OF_GROUPS)):

        graphs = [
                go.Bar(
                    name="Difference: " + str(difference),  # Dropdown category
                    x=df[df['group'] == group_no][df['difference'] == difference][df['category'] == category]['round'],
                    y=df[df['group'] == group_no][df['difference'] == difference][df['category'] == category]['value'],
                    offsetgroup=idx
                ) for idx, difference in enumerate(range(0, 5))
            ]

        # for graph in graphs:
        #     graph.
        #     # graph.update_xaxes(title_text='Round')
        #     # graph.update_yaxes(title_text='Count')

        fig.append_trace(graphs[0], row=idx+1, col=1)

    return fig


# ===== BUILD BASE CHART =====

master_df = calculate_differences()
ANNOTATION_CATEGORIES = ['Appropriateness', 'Information content of outputs', 'Humanlikeness']

fig = create_chart(master_df, 'Appropriateness')

# ===== UPDATE AXES =====

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
            } for group_no in range(1, 6)
        ],
        value=1  # Default value
    ),

    # Dropdown for category
    dcc.Dropdown(
        id='category-dropdown',
        options=ANNOTATION_CATEGORIES,
        value=ANNOTATION_CATEGORIES[0]  # Default value
    ),

    dcc.Graph(
        id='differences-graph',
        figure=fig
    ),

    # Store dropdown selection on local browser session
    dcc.Store(id='filter-store')

])


# ===== CALLBACKS FOR DROPDOWNS =====
"""

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
    Output('differences-graph', 'figure'),
    Input('filter-store', 'data')
)
def update_category_chart(filter_json):
    return create_chart(master_df, filter_json['group_no'], filter_json['category'])

"""
if __name__ == '__main__':
    app.run_server(debug=True)
