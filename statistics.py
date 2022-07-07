"""
Script to calculate statistics
"""
import pandas as pd
import numpy as np
from pandas import CategoricalDtype
from data_utils import read_data, calculate_group_kappa
import math
ANNOTATION_CATEGORIES = ['Appropriateness', 'Information content of outputs', 'Humanlikeness']

initial_data = read_data()
data = calculate_group_kappa(initial_data)

category_list = []
round_list = []
within_list = []
between_list = []

for category in ANNOTATION_CATEGORIES:

    
    print('category:', category)
    for idx, round in enumerate(data.keys()):

        within_group_scores = []
        between_group_scores = []
        # if round > 3:
        #     break
        round_data = data[round][category]

        for i in range(len(round_data)):
            for j in range(len(round_data)):
                score = round_data[i][j]
                
                if math.isnan(score):
                    continue
                # Find within group agreement
                if (i % 2 == 0) and (i + 1 == j):
                    within_group_scores.append(score)
                else:
                    between_group_scores.append(score)
        print('----------')
        print(f'round {str(round)}')
        print('within group:', sum(within_group_scores)/len(within_group_scores))
        print('between group:', sum(between_group_scores)/len(between_group_scores))
        
        category_list.append(category)
        round_list.append(round)
        within_list.append(sum(within_group_scores)/len(within_group_scores))
        between_list.append(sum(between_group_scores)/len(between_group_scores))

df = pd.DataFrame({
    'category': category_list,
    'round': round_list,
    'within': within_list,
    'between': between_list
})

df.to_excel('iaa_stats.xlsx', engine='openpyxl')


    # fig.add_trace(
    #     go.Heatmap(
    #         x=[f"Rater {group_no + 1}" for group_no in range(len(round_data))],
    #         y=[f"Rater {group_no + 1}" for group_no in range(len(round_data))],
    #         z=round_data,
    #         type='heatmap',
    #         hoverongaps=False,
    #         coloraxis='coloraxis',
    #         text=round_data,
    #         texttemplate="%{text:.2f}",
    #         textfont={"size": 10}
    #     ), 1, idx + 1
    # )



def create_heatmap_kappa(data, category):
    fig = make_subplots(
        1,
        6,
        # len(data.keys()),
        vertical_spacing=0.05,
        horizontal_spacing=0.05,
        # shared_yaxes=True,
        # subplot_titles=[f"Round {i}" for i in data.keys()]
        subplot_titles=[f"Round 1", "Round 2", "Round 3", "Round 4", "Round 5", "Round 6"]
    )

    # Patches to add emphasis on groups

    for idx, round in enumerate(data.keys()):
        # if round > 3:
        #     break
        round_data = data[round][category]

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
        coloraxis={'colorscale': 'PuBu'},
    )

    return fig