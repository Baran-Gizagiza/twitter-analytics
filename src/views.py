""" views.py """

import streamlit as st

class Views():
    def corr_rank(self):
        corr_rank = st.sidebar.number_input(
            'Select "corr_rank" (0.1 ~ 1.0)',
            min_value=0.1,
            max_value=1.0,
            value=0.7
        )
        return corr_rank


    def target_column(self, df):
        target_column = st.sidebar.selectbox(
            'Select "Target column" for analytics',
            df.columns[1:]
        )
        return target_column


    def quan(self):
        quan = st.sidebar.number_input(
            'Select "quantile" number (0.01 ~ 1.00)',
            min_value=0.01,
            max_value=1.00,
            value=0.99
        )
        return quan


    def hue_string(self, string_list):
        hue_string = st.sidebar.selectbox(
            'Select "Hue column"',
            string_list
        )
        return hue_string


    def level(self):
        level = st.sidebar.selectbox(
            'Select "Graph time trend level"',
            ['month', 'year', 'quarter', 'week', 'weekday', 'day']
        )
        return level

    def percent(self):
        percent = st.sidebar.number_input(
            'Select "percent" for Good tweet (1 ~ 100)',
            min_value=1,
            max_value=100,
            value=20
        )
        return percent


    def file_output_value(self):
        file_output = st.sidebar.radio(
            'Output the good tweet with excel file?"',
            ['No', 'Yes']
            )
        return file_output
