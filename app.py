from dash import Dash, dcc, html, Input, Output

from dash_utils import ANNOTATION_CATEGORIES, create_linechart, create_histograms_differences, \
    create_histograms_annotations, create_heatmap_kappa
from data_utils import get_dfs

"""
Create a grouped bar chart of annotation differences per each round
"""

# Create line chart for kappa scores


# ===== DATA =====
# Grab dataframes
differences_df, kappa_df, annotation_df, kappa_data = get_dfs()

# ===== BUILD BASE CHART =====

histogram_fig = create_histograms_differences(differences_df, 'Appropriateness')
linechart_fig = create_linechart(kappa_df)
annotation_fig = create_histograms_annotations(annotation_df, 'Appropriateness')  # For counting annotations
heatmap_fig = create_heatmap_kappa(kappa_data, 'Appropriateness')
# ===== UPDATE AXES =====

# fig.update_xaxes(title_text='Round')
# fig.update_yaxes(title_text='Count')

print(differences_df.size)
app = Dash(__name__)

server = app.server

app.layout = html.Div(children=[
    html.H1(children='Common Law Annotations'),

    html.Div(children='''
        An interactive chart for Common Law Annotations
    '''),

    html.H2(children="Inter-group Inter-annotator Agreement per Round"),
    dcc.Graph(
        id='linechart-graph',
        figure=linechart_fig,
        style={'width': '90vw', 'height': '60vh'}  # Set graph size
    ),

    html.H2(children="Intra-group Inter-Annotator Agreement per Round"),
    dcc.Graph(
        id='heatmap-graph',
        figure=heatmap_fig,
        style={'width': '90vw', 'height': '60vh'}  # Set graph size
    ),

    html.H2(children='Differences in Annotations per Round'),

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
        figure=histogram_fig
    ),

    dcc.Graph(
        id='annotations-graph',
        figure=annotation_fig
    ),

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
    Output('differences-graph', 'figure'),
    Output('annotations-graph', 'figure'),
    Output('heatmap-graph', 'figure'),
    Input('filter-store', 'data'),
)
def update_category_chart(filter_json):
    return (
        create_histograms_differences(differences_df, filter_json['category']),
        create_histograms_annotations(annotation_df, filter_json['category']),
        create_heatmap_kappa(kappa_data, filter_json['category'])
    )


if __name__ == '__main__':
    app.run_server(debug=True)
