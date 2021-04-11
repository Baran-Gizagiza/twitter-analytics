""" preprocessing_data.py """

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


class PreProcessing():
    @st.cache
    # 1％の外れ値を取り除いた変数を作成
    def quantile(self, df, var, num):
        q = df[var].quantile(num)
        df_quan = df[df[var] <= q]
        return df_quan

    def histgram_target(self, df, target, bins=20):
        fig, axes = plt.subplots(figsize=(10,5))
        axes.hist(data=df,x=target, bins=bins)
        axes.set_xlabel(target)
        axes.set_ylabel("Count")
        axes.set_title(target)
        fig.tight_layout()
        st.pyplot(fig)

    def histgram_related(self, df, related, bins=20, N=3):
        width = 15
        height = 6
        max_size = len(related)
        q, r = divmod(max_size, N)
        if q == 0 or (q == 1 and r == 0):
            fig, axes = plt.subplots(1, N, figsize=(width, height))
            for idx, column in enumerate(related):
                axes[idx].hist(data=df,x=column, bins=bins)
                axes[idx].set_xlabel(column)
                axes[idx].set_ylabel("Count")
                axes[idx].set_title(column)

        else:
            if q >= 2 and r == 0:
                fig, axes = plt.subplots(q, N, figsize=(width, height*q))
            else:
                fig, axes = plt.subplots(q+1, N, figsize=(width, height*(q+1)))
            for idx, column in enumerate(related):
                x = idx // N
                y = idx % N
                axes[x, y].hist(data=df,x=column, bins=bins)
                axes[x, y].set_xlabel(column)
                axes[x, y].set_ylabel("Count")
                axes[x, y].set_title(column)
        st.pyplot(fig)
