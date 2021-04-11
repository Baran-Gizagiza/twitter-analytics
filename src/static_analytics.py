""" static_analytics.py """

import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import f_regression
from sklearn.preprocessing import StandardScaler


class Static_Analysis():
    @st.cache
    def single_reg(self, df, related, target):
        d = {}
        for column in related:
            X, y = df[[column]], df[target]
            reg = LinearRegression(fit_intercept=False)
            results = reg.fit(X, y)
            r2 = reg.score(X,y).round(3)
            a = reg.coef_[0].round(6)
            inv_a = (1/a).round(3)
            d[column] = [a, inv_a, r2]
        reg_sum = pd.DataFrame.from_dict(d, orient='index').reset_index()\
                    .rename(columns={"index":"Feature", 0:'Coef', 1:target, 2: "R2"})
        return reg_sum

    @st.cache
    def multi_reg_scaled(self, df, related, target):
        X, y = df[related], df[target]
        X_scaled = StandardScaler().fit_transform(X)
        reg = LinearRegression(fit_intercept=False)
        reg.fit(X_scaled, y)
        a = reg.coef_.round(6)
        p_values = f_regression(X_scaled, y)[1].round(3)
        reg_sum = pd.DataFrame(data = X.columns.values, columns=['Features'])
        reg_sum['Coef'] = a
        reg_sum['p-values'] = p_values
        return reg_sum

    @st.cache
    def multi_reg(self, df, related, target):
        X, y = df[related], df[target]
        reg = LinearRegression(fit_intercept=False)
        reg.fit(X, y)
        a = reg.coef_.round(6)
        r2 = reg.score(X, y).round(3)
        p_values = f_regression(X, y)[1].round(3)
        reg_sum = pd.DataFrame(data = X.columns.values, columns=['Features'])
        reg_sum['Coef'] = a
        reg_sum[target] = (1/a).round(3)
        reg_sum['R2'] = r2
        return reg_sum

    @st.cache
    def evaluation_percent(self, df, column, evaluation, percent=20):
        per = df[column].quantile(q=[(100-percent)/100]).iloc[0]
        df[evaluation] = df[column].apply(lambda x: 1 if x >= per else 0)
        return df
