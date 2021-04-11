""" time_analytics.py """

import streamlit as st
import datetime
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(font='Yu Gothic')


class Time_Analytics():
    def time_trend(self, df):
        df = df.set_index([df.index.year, df.index.quarter,\
                            df.index.month, df.index.isocalendar().week,\
                            df.index.weekday, df.index.day, df.index])
        df.index.names = ['year', 'quarter', 'month', 'week', 'weekday', 'day', 'date']
        return df

    @st.cache
    def trend_by_level(self, df, level_time='month', agg_iter='sum'):
        groupby_df = df.groupby(level=level_time).agg(agg_iter)
        groupby_df['Engagement'] / groupby_df['Impression']
        return groupby_df
