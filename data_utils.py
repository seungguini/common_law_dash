"""
1. Calculate number of differences for all groups, for each round
- 1 Array per group, 3 categories per group, 4 differences

"""

import numpy as np
import glob
import pandas as pd
import os
from sklearn.metrics import cohen_kappa_score
import itertools

# File path to annotations folder

BASE_PATH = './annotations/round'
ROUNDS = 5
# NUMBER_OF_GROUPS = 4

ANNOTATION_CATEGORIES = ['Appropriateness', 'Information content of outputs', 'Humanlikeness']
# Possible Cohen's Kappa Calculation Combos:
# 1. Same round, within group (in two's)
# 2. Same round, everyone
# 2. Different rounds, same person (see how much the agreement changes)
# 2. Same round, across groups (average groups - calculate kappa across groups)

"""
Calculates the differences in annotations for each group per round and returns it in a dataframe
"""


# Reads annotation data and returns a 3D matrix
# Round - Group - Category - annotations
def read_data():
    # For each group, calculate their cohen's kappa
    # for group_no in range(1, NUMBER_OF_GROUPS+1):

    rounds = {}
    print('attempting to calculate differences')
    print(os.getcwd())
    for ROUND_NUMBER in range(1, ROUNDS + 1):
        groups = {}
        for GROUP_NO in range(1, 6):
            categories = {}

            # Build final path to dataset
            FINAL_PATH = BASE_PATH + str(ROUND_NUMBER) + '/group' + str(GROUP_NO) + '/'

            # Use glob to grab all .xlsx files
            xlsx_files = glob.glob(FINAL_PATH + '*.xlsx')

            # Skip if files don't exist
            if len(xlsx_files) == 0:
                continue

            # For each annotation category, compile annotations
            for annotation_category in ANNOTATION_CATEGORIES:

                # Read xlsx files into two different Series
                raters = []
                difference_count = [0, 0, 0, 0, 0]  # Differences of 0, 1, 2, 3, 4

                for xlsx_annotator in xlsx_files:
                    annotator_df = pd.read_excel(xlsx_annotator, engine='openpyxl')[:50]

                    # Convert each column (series) into lists
                    annotations = annotator_df[annotation_category]

                    raters.append(annotations)

                # Set annotations for this category
                categories[annotation_category] = raters

            # Set category values for this group
            groups[GROUP_NO] = categories

        # Set group number for this round
        rounds[ROUND_NUMBER] = groups

    return rounds


def calculate_differences(data):
    # For each group, calculate their cohen's kappa
    differences_data = {
        'value': [],
        'difference': [],
        'category': [],
        'round': [],
        'group': []
    }

    print('attempting to calculate differences')
    print(os.getcwd())

    # Get number of rounds
    ROUNDS = data.keys()
    for ROUND_NUMBER in ROUNDS:
        # for ROUND_NUMBER in range(1,ROUNDS):
        round = data[ROUND_NUMBER]

        GROUPS = round.keys()
        for GROUP_NO in GROUPS:
            group = round[GROUP_NO]

            # For each annotation category, compile annotations
            for annotation_category in ANNOTATION_CATEGORIES:

                # Grab list of pd.Series, where each Series is a set of 50 annotations. Two Series per group
                two_annotations = group[annotation_category]

                raters = []
                for annotations in two_annotations:
                    raters.append(annotations)
                # Read xlsx files into two different Series

                difference_count = [0, 0, 0, 0, 0]  # Differences of 0, 1, 2, 3, 4

                # Calculate differences in annotation values
                differences = np.absolute(raters[0] - raters[1])[:50].astype('int32')
                for difference in differences:
                    difference_count[difference] += 1

                # Add info to master_dataframe
                for idx, difference in enumerate(difference_count):
                    # master_df = pd.DataFrame(columns=['value', 'difference', 'category', 'round', 'group'])
                    row_dict = {'value': difference, 'difference': idx, 'category': annotation_category,
                                'round': ROUND_NUMBER, 'group': GROUP_NO}

                    differences_data['value'].append(difference)
                    differences_data['difference'].append(idx)
                    differences_data['category'].append(annotation_category)
                    differences_data['round'].append(ROUND_NUMBER)
                    differences_data['group'].append(GROUP_NO)

    return pd.DataFrame(differences_data)


def calculate_cohen_kappa(data):
    kappa_data_list = {
        'kappa_score': [],
        'category': [],
        'round': [],
        'group': []
    }

    print('attempting to calculate differences')
    print(os.getcwd())

    labels = [1, 2, 3, 4, 5]

    # Get number of rounds
    ROUNDS = data.keys()
    for ROUND_NUMBER in ROUNDS:
        # for ROUND_NUMBER in range(1,ROUNDS):
        round = data[ROUND_NUMBER]

        GROUPS = round.keys()
        for GROUP_NO in GROUPS:
            group = round[GROUP_NO]

            # For each annotation category, compile annotations
            for annotation_category in ANNOTATION_CATEGORIES:

                # Grab list of pd.Series, where each Series is a set of 50 annotations. Two Series per group
                two_annotations = group[annotation_category]

                raters = []
                for annotations in two_annotations:
                    raters.append(annotations)
                # Read xlsx files into two different Series

                kappa_data = np.zeros((len(raters), len(raters)))

                # Calculate cohen_kappa_score for every combination of raters
                # Combinations are only calculated j -> k, but not k -> j, which are equal
                # So not all places in the matrix are filled.
                for j, k in list(itertools.combinations(range(len(raters)), r=2)):
                    kappa_data[j, k] = cohen_kappa_score(raters[j], raters[k], weights='linear', labels=labels)

                kappa_score = kappa_data[0][1]
                # Add kappa score to dataframe

                # master_df = pd.DataFrame(columns=['value', 'difference', 'category', 'round', 'group'])
                row_dict = {'kappa_score': kappa_score, 'category': annotation_category,
                            'round': ROUND_NUMBER, 'group': GROUP_NO}

                kappa_data_list['kappa_score'].append(kappa_score)
                kappa_data_list['category'].append(annotation_category)
                kappa_data_list['round'].append(ROUND_NUMBER)
                kappa_data_list['group'].append(GROUP_NO)

    return pd.DataFrame(kappa_data_list)


def calculate_group_kappa(data):
    print('attempting to calculate differences')
    print(os.getcwd())

    # all possible annotation labels
    labels = [1, 2, 3, 4, 5]
    # Get number of rounds
    ROUNDS = data.keys()

    # Master list of all rounds
    all_rounds = {}

    for ROUND_NUMBER in ROUNDS:
        all_rounds[ROUND_NUMBER] = {}  # To be filled with annotation specific kappa scores
        # for ROUND_NUMBER in range(1,ROUNDS):
        round = data[ROUND_NUMBER]

        # New set of raters per round
        raters = {
            'Appropriateness': [],
            'Information content of outputs': [],
            'Humanlikeness': []
        }

        # For each round, grab all raters
        GROUPS = round.keys()
        for GROUP_NO in GROUPS:
            group = round[GROUP_NO]

            # For each annotation category, compile annotations
            for annotation_category in ANNOTATION_CATEGORIES:

                # Grab list of pd.Series, where each Series is a set of 50 annotations. Two Series per group
                two_annotations = group[annotation_category]

                for annotations in two_annotations:
                    raters[annotation_category].append(annotations)
                # Read xlsx files into two different Series

        for annotation_category in ANNOTATION_CATEGORIES:
            kappa_rater = raters[annotation_category]  # List of all raters for the category, for this round
            kappa_data = np.zeros((len(kappa_rater), len(kappa_rater)))
            # Calculate cohen_kappa_score for every combination of raters
            # Combinations are only calculated j -> k, but not k -> j, which are equal
            # So not all places in the matrix are filled.
            for j, k in list(itertools.combinations(range(len(kappa_rater)), r=2)):
                kappa_data[j, k] = cohen_kappa_score(kappa_rater[j], kappa_rater[k], weights='linear', labels=labels)

            for j in range(len(kappa_rater)):
                for k in range(len(kappa_rater)):
                    if kappa_data[j, k] == float(0):
                        kappa_data[j, k] = None

            all_rounds[ROUND_NUMBER][annotation_category] = kappa_data

    return all_rounds


def calculate_count(data):
    annotation_data = {
        'annotation': [],
        'category': [],
        'round': [],
        'group': []
    }
    # annotation_df = pd.DataFrame(columns=['annotation', 'category', 'round', 'group'])
    print('attempting to calculate differences')
    print(os.getcwd())

    # Get number of rounds
    ROUNDS = data.keys()
    for ROUND_NUMBER in ROUNDS:
        # for ROUND_NUMBER in range(1,ROUNDS):
        round = data[ROUND_NUMBER]

        GROUPS = round.keys()
        for GROUP_NO in GROUPS:
            group = round[GROUP_NO]

            # For each annotation category, compile annotations
            for annotation_category in ANNOTATION_CATEGORIES:

                # Grab list of pd.Series, where each Series is a set of 50 annotations. Two Series per group
                two_annotations = group[annotation_category]

                raters = []
                for annotations in two_annotations:
                    raters.extend(annotations)
                # Read xlsx files into two different Series

                for annotation_score in raters:
                    # master_df = pd.DataFrame(columns=['value', 'difference', 'category', 'round', 'group'])

                    annotation_data['annotation'].append(annotation_score)
                    annotation_data['category'].append(annotation_category)
                    annotation_data['round'].append(ROUND_NUMBER)
                    annotation_data['group'].append(GROUP_NO)

    return pd.DataFrame(annotation_data)


def create_contingency_table(data):
    # Get number of rounds
    ROUNDS = data.keys()

    # Master list of all rounds
    all_rounds = {}

    for ROUND_NUMBER in ROUNDS:
        all_rounds[ROUND_NUMBER] = {}  # To be filled with annotation specific kappa scores
        # for ROUND_NUMBER in range(1,ROUNDS):
        round = data[ROUND_NUMBER]

        # For each round, grab all raters
        GROUPS = round.keys()
        for GROUP_NO in GROUPS:

            # 3 Contingency table per round for each group
            contingency_tables = {
                # Each category is a 5 x 5 matrix
                'Appropriateness': np.zeros((5, 5)),
                'Information content of outputs': np.zeros((5, 5)),
                'Humanlikeness': np.zeros((5, 5)),
            }

            group = round[GROUP_NO]

            # For each annotation category, compile annotations
            for annotation_category in ANNOTATION_CATEGORIES:

                # Grab list of pd.Series, where each Series is a set of 50 annotations. Two Series per group
                two_annotations = group[annotation_category]

                # Get each annotation1 - annotation2 pair for each prompt
                # Fill it inside the contingency table
                for idx in range(len(two_annotations[0])):
                    # Grab the annotation scores for both raters
                    first_score = two_annotations[0][idx]
                    second_score = two_annotations[1][idx]

                    # Add count to the annotation - annotation pairing
                    contingency_tables[annotation_category][int(first_score - 1)][int(second_score - 1)] += 1

            # Add contingency table for this group for this round
            all_rounds[ROUND_NUMBER][GROUP_NO] = contingency_tables

    return all_rounds


def get_dfs():
    print('get df ran again :(')
    # Grab data
    data = read_data()

    # Grab DFs
    difference_df = calculate_differences(data)
    kappa_df = calculate_cohen_kappa(data)
    annotation_df = calculate_count(data)
    group_kappa_data = calculate_group_kappa(data)
    contingency_table = create_contingency_table(data)

    return difference_df, kappa_df, annotation_df, group_kappa_data, contingency_table
