#!/usr/bin/env python

import os, json
import numpy as np
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib as plt
import plotly.express as px

def file_path(rel_path, data_file):
    '''
    Form paths using os library and user inputs
    Dependencies - None
    '''
    # Create path to data files
    print("Generating data file path.")
    data_dir = os.path.abspath(rel_path)
    data_path = os.path.join(data_dir,data_file)
    print('File path generation completed.')
    return data_path

# Class attributes and methods
class tweet_analysis:

    # Seaborn configuration/design parameters     
    sns.set(rc={"figure.figsize":(15,15),
                "figure.facecolor":"ffffff",
                "text.color":"black"},
                style='darkgrid',
                font_scale=1.15)

    '''
    Analysis class for objects containing tweet data, statistics and charts
    '''
    def __init__(self,df):
        self.df = df
        self.sent_evol_df=self.sent_evol_data()
        self.series_entries_count=self.count_series_entries()
        self.series_entry_count = self.count_series_entries()
        self.neg_tweet_counts = self.df['negative_score']
        self.pos_tweet_counts = self.df['positive_score']
        self.neut_tweet_counts = self.df['neutral_score']
        self.net_sent_tweet_counts = self.series_entries_count['net_score']
        self.lang_counts = self.series_entries_count['tweet_language']
        self.lang_counts_grouped = self.group_low_count_data(self.series_entry_count['tweet_language'], 0.15)
        self.tweet_source_counts = self.series_entries_count['tweet_source']
        self.tweet_source_counts_grouped = self.group_low_count_data(self.series_entry_count['tweet_source'],1 )
        self.corr_data = df.corr()
        self.shape = df.shape
        self.size = df.size
        self.dtypes = df.dtypes
        self.colums = df.columns
        self.null_vaue_count = df.isnull().sum()
        self.prelim_stats = df.describe()

    def count_series_entries(self):
        '''
        Count the number of times each pattern occurs in each string column
        eg. Count number of times each language occurs in a collection of tweets
        Dependencies - None
        '''
        series_entry_count = {}
        df_series_lst = list(df.columns[df.dtypes == 'object'])
        exception_lst = ['tweet_id', 'tweet_text']
        for series in df_series_lst:
            if series not in exception_lst:
                series_entry_count[series] = self.df[series].value_counts()
        return series_entry_count

    def group_low_count_data(self, pd_series, cutoff_percent):
        '''
        To prevent overcrowding of pie charts:
        1. Filter and group data with low counts (i.e. categories with small area on pie chart)
        2. What is considered a 'small' area is defined by the user by specifying a threshold percentage (frctnl_lmt)
        3. Values below the threshold value are represented under the category 'Others'
        '''
        cutoff_fraction = cutoff_percent / 100
        pd_series_count = pd_series.sum()
        pd_series_proc = pd_series[pd_series > (cutoff_fraction*pd_series_count)]
        pd_series_proc['Others'] = pd_series[pd_series <= (cutoff_fraction*pd_series_count)].sum()
        pd_series_proc.sort_values(inplace=True)
        return pd_series_proc

    def sent_evol_data(self):
        '''
        Computes and returns a dataframe that contains the cumulative counts of positive and negative tweets as a function of time
        '''
        sent_evol_df = self.df[['tweet_time','net_score']]
        sent_evol_df = sent_evol_df.sort_values(by='tweet_time')
        count_positive=0
        pos_lst = []
        count_negative=0
        neg_lst = []
        for sent in sent_evol_df['net_score']:
            if sent.lower() == 'positive':
                count_positive += 1
                pos_lst.append(count_positive)
            else:
                pos_lst.append(count_positive)
            if sent.lower() == 'negative':
                count_negative += 1
                neg_lst.append(count_negative)
            else:
                neg_lst.append(count_negative)
        print('Positive list:')
        print(len(pos_lst))
        print(pos_lst[:10])
        print('Negative list:')
        print(len(neg_lst))
        print(neg_lst[:10])
        sent_evol_df['neg_tweet_count'] = neg_lst
        sent_evol_df['pos_tweet_count'] = pos_lst
        print(sent_evol_df.columns)
        return sent_evol_df


# matplotlib charts
    def draw_pie_chart(self,data,title=None):
        fig, axis = plt.pyplot.subplots()
        graph_params={'kind':'pie','figsize':(20,15),'autopct':'%.1f','title':title,'ax':axis}
        data.plot(**graph_params)

    def draw_barh_chart(self,data):
        fig, axis = plt.pyplot.subplots()
        graph_params={'kind':'barh','figsize':(15,15),'title':"Distribution of meow",'ax':axis}
        data.plot(**graph_params)

    def draw_hist_chart(self,data,bins,color):
        fig, axis = plt.pyplot.subplots(figsize=(15,15))
        graph_params={'x':data, 'bins':bins,'color':color,'alpha':0.5,'data':self.df,'ax':axis}
        sns.histplot(**graph_params)

    def draw_corr_chart(self,corr_data):
        fig, axis = plt.pyplot.subplots(figsize=(15,15))
        graph_params={'data':corr_data,'cmap' : 'RdBu_r','xticklabels':corr_data.columns,
        'yticklabels':corr_data.columns,'linewidth' : 0.5,'annot' : True, 'ax':axis}
        return sns.heatmap(**graph_params)

# plotly express charts
    

# test/debugging        
fname = 'test_with_sentiments.json'
df = pd.read_json(file_path("data/", fname))        
a1 = tweet_analysis(df)
print(a1.corr_data)
print(a1.corr_data.columns)
print(np.array(a1.corr_data))
