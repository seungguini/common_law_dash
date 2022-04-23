from plotly import graph_objects as go, express as px
from plotly.subplots import make_subplots

ANNOTATION_CATEGORIES = ['Appropriateness', 'Information content of outputs', 'Humanlikeness']
linechart_colors = [

    '#ff7f0e',  # safety orange
    '#1f77b4',  # muted blue
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
]
linechart_styles = {
    'Appropriateness': {'dash': 'solid', 'marker': 'circle'},
    'Information content of outputs': {'dash': 'solid', 'marker': 'square'},
    'Humanlikeness': {'dash': 'solid', 'marker': 'star'},
}


def create_linechart(df):
    fig = go.Figure()
    for group_no in range(1, 5):
        for category in ANNOTATION_CATEGORIES:
            fig.add_trace(go.Scatter(
                x=df[df['group'] == group_no][df['category'] == category]['round'],
                y=df[df['group'] == group_no][df['category'] == category]['kappa_score'],
                name=f"Group {group_no} - {category}",
                line=dict(
                    color=linechart_colors[group_no - 1],
                    width=2,
                    dash=linechart_styles[category]['dash'],
                ),
                mode='lines+markers',
                marker=dict(
                    symbol=linechart_styles[category]['marker'],
                    size=12

                )
            ))
            fig.update_xaxes(type='category')  # Make x axis discrete
            fig.update_layout(title="Cohen's Kappa per Round",
                              xaxis_title='Round',
                              yaxis_title="Cohen's Kappa")
    return fig


def create_histograms_differences(df, category):
    fig = px.histogram(
        df[df['category'] == category],
        x='round',
        y='value',
        color='difference',
        barmode='group',
        facet_row='group',
    )
    fig.update_xaxes(type='category')

    # === Update y-axis text ===

    # Remove all subplot y axes
    for axis in fig.layout:
        if type(fig.layout[axis]) == go.layout.YAxis:
            fig.layout[axis].title.text = ''

    fig.update_layout(
        # keep the original annotations and add a list of new annotations:
        annotations=list(fig.layout.annotations) + [
            go.layout.Annotation(
                x=-0.07,
                y=0.5,
                font=dict(
                    size=14
                ),
                showarrow=False,
                text="Count",
                textangle=-90,
                xref="paper",  # Positions labels independent of subplots
                yref="paper"
            )
        ]
    )

    return fig


def create_histograms_annotations(df, category):
    fig = px.histogram(
        df[df['category'] == category],
        x='round',
        y='annotation',
        color='annotation',
        barmode='group',
        facet_row='group',
    )
    fig.update_xaxes(type='category')

    # Remove all subplot y axes
    for axis in fig.layout:
        if type(fig.layout[axis]) == go.layout.YAxis:
            fig.layout[axis].title.text = ''

    fig.update_layout(
        # keep the original annotations and add a list of new annotations:
        annotations=list(fig.layout.annotations) + [
            go.layout.Annotation(
                x=-0.07,
                y=0.5,
                font=dict(
                    size=14
                ),
                showarrow=False,
                text="Count",
                textangle=-90,
                xref="paper",  # Positions labels independent of subplots
                yref="paper"
            )
        ]
    )
    return fig


def create_heatmap_kappa(data, category):
    fig = make_subplots(
        1,
        len(data.keys()),
        vertical_spacing=0.05,
        horizontal_spacing=0.05,
        shared_yaxes=True,
        subplot_titles=[f"Round {i}" for i in data.keys()]
    )

    # Patches to add emphasis on groups

    for idx, round in enumerate(data):
        round_data = data[round][category]

        xpatches = [i for i in range(len(round_data)) if i % 2 == 1]  # Odd idx get patches
        ypatches = [i for i in range(len(round_data)) if i % 2 == 0]  # Odd idx get patches

        fig.add_trace(
            go.Heatmap(
                x=[f"Rater {group_no + 1}" for group_no in range(len(round_data))],
                y=[f"Rater {group_no + 1}" for group_no in range(len(round_data))],
                z=round_data,
                type='heatmap',
                hoverongaps=False,
                coloraxis='coloraxis',
                text=round_data,
                texttemplate="%{text:.2f}",
                textfont={"size": 10}
            ), 1, idx + 1
        )

    fig.update_layout(
        coloraxis={'colorscale': 'viridis'},
    )

    return fig
