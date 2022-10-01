import numpy as np
import pandas as pd
import sys

csv = sys.argv[1]
#csv = '/Users/kathleenkanaley/Desktop/grapes_in_space/data_orig/data_scout_2021/2021_08_10_FieldScouting_PM_DM.csv'
def get_avg_severity(csv):
    '''
    This function takes downy mildew (DM) severity ratings for top and bottom leaf surfaces
    of 20 leaves and calculates an average severity rating.

    input: (str) path to a csv file containing DM severity ratings

    note: this function was written for csvs containing 20 ratings
    and specific metadata. It can be modified to accomodate different csv formats.

    '''

    data = pd.read_csv(csv) # read in data
    data = data.dropna(axis=1, how='all') # drop empty columns
    data = data.dropna(axis=0, how='all') # drop empty rows
    data = data.fillna(0) #fill any remaining nan values

    # Get the DM Top and DM Bot values only for each panel

    dm_only = data[data['Disease'].isin(['DM Top', 'DM Bot'])]
    leaves = dm_only.iloc[:,5:25] # get leaf-level sev. values
    leaves = leaves.apply(pd.to_numeric, errors='coerce') # make sure all leaf sev. values are of type int

    mean_sev = leaves.mean(axis=1) # get mean severity per disease label (top/bot)

    pd.options.mode.chained_assignment = None #prevent throwing a SettingWithCopy warning
    dm_only['mean_sev'] = mean_sev # add mean_sev column to the dataframe

    # If the treatment, row, and panel match for a pair of DM ratings, average the two ratings.

    pairs = dm_only.groupby(dm_only.index // 2) #floor division of indices give consecutive rows the same index

    pair_means = pairs['mean_sev'].mean()
    pair_means_new = pair_means.reset_index(drop=True)

    meta = dm_only.iloc[:,:5] # just the metadata - row, panel, treatment, date, disease
    meta = meta.drop_duplicates(subset=['Treatment', 'Row ', 'Panel ']) # get one line of data per panel
    meta['Disease'] = 'DM_avg'  # change disease label
    meta_new = meta.reset_index(drop=True)

    meta_new['mean_sev_top_bot'] = pair_means_new # add the avg. top and bottom severity to the metadata for each panel

    #return meta_new

    meta_new.to_csv(csv[:-4]+'_avgsev.csv')

get_avg_severity(csv)
