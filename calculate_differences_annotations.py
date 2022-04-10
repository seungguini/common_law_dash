"""
1. Calculate number of differences for all groups, for each round
- 1 Array per group, 3 categories per group, 4 differences

"""



import numpy as np
import glob
import pandas as pd
import os

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
def calculate_differences():
    # For each group, calculate their cohen's kappa
    # for group_no in range(1, NUMBER_OF_GROUPS+1):

    master_df = pd.DataFrame(columns=['value', 'difference', 'category', 'round', 'group'])
    print('attempting to calculate differences')
    print(os.getcwd())
    for ROUND_NUMBER in range(1,ROUNDS):
        for GROUP_NO in range(1, 6):


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
                difference_count = [0, 0, 0, 0, 0] # Differences of 0, 1, 2, 3, 4

                for xlsx_annotator in xlsx_files:
                    annotator_df = pd.read_excel(xlsx_annotator, engine='openpyxl')

                    print(annotation_category)

                    # Convert each column (series) into lists
                    annotations = annotator_df[annotation_category]

                    raters.append(annotations)

                # Calculate differences in annotation values
                differences = np.absolute(raters[0] - raters[1])[:50].astype('int32')
                for difference in differences:
                    difference_count[difference] += 1

                # Add info to master_dataframe
                for idx, difference in enumerate(difference_count):

                    # master_df = pd.DataFrame(columns=['value', 'difference', 'category', 'round', 'group'])
                    row_dict = {'value': difference, 'difference': idx, 'category': annotation_category, 'round': ROUND_NUMBER, 'group': GROUP_NO}
                    master_df = master_df.append(row_dict, ignore_index=True, )

                
    return master_df

