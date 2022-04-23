from dash import Dash, dcc, html, Input, Output

from dash_utils import ANNOTATION_CATEGORIES, create_linechart, create_histograms_differences, \
    create_histograms_annotations, create_heatmap_kappa
from data_utils import get_dfs
from flask_caching import Cache

"""
Create a grouped bar chart of annotation differences per each round
"""

# Create line chart for kappa scores


# ===== UPDATE AXES =====

app = Dash(__name__)
cache = Cache(app.server, config={
    'CACHE_TYPE': 'simple',
})
app.config.suppress_callback_exceptions = True

server = app.server

TIMEOUT = 60


@cache.memoize(timeout=TIMEOUT)  # Memoize to avoid re-loading data
def query_data():
    print('querying data')
    return get_dfs()


app.layout = html.Div(children=[
    html.H1(children='Common Law Annotations'),

    html.Div(children='''
        An interactive chart for Common Law Annotations
    '''),

    html.H2(children="Inter-group Inter-annotator Agreement per Round"),
    dcc.Graph(
        id='linechart-graph',
        figure=create_linechart(query_data()[1]),
        style={'width': '90vw', 'height': '60vh'}  # Set graph size
    ),

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

    html.H2(children="Intra-group Inter-Annotator Agreement per Round"),
    dcc.Graph(
        id='heatmap-graph',
        figure=create_heatmap_kappa(query_data()[3], 'Appropriateness'),
        style={'width': '90vw', 'height': '60vh'}  # Set graph size
    ),

    html.H2(children='Differences in Annotations per Round'),

    dcc.Graph(
        id='differences-graph',
        figure=create_histograms_differences(query_data()[0], 'Appropriateness')
    ),

    dcc.Graph(
        id='annotations-graph',
        figure=create_histograms_annotations(query_data()[2], 'Appropriateness')
    ),

    # Store dropdown selection on local browser session
    dcc.Store(id='filter-store')

])


# ==== LOAD DATA ====

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
    Output('differences-graph', 'figure'),
    Output('annotations-graph', 'figure'),
    Output('heatmap-graph', 'figure'),
    Input('filter-store', 'data'),
)
def update_category_chart(filter_json):
    return (
        create_histograms_differences(query_data()[0], filter_json['category']),
        # skips kappa linechart - no categorical selections
        create_histograms_annotations(query_data()[2], filter_json['category']),
        create_heatmap_kappa(query_data()[3], filter_json['category'])
    )


if __name__ == '__main__':
    app.run_server(debug=True)
