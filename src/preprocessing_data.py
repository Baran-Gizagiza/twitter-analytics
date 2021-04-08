""" preprocessing_data.py """

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

@st.cache
class PreProcessing():
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

    def histgram_related(self, df, related, bins=20):
        fig, axes = plt.subplots(1, len(related), figsize=(10,5))
        for idx, column in enumerate(related):
            axes[idx].hist(data=df,x=column, bins=bins)
            axes[idx].set_xlabel(column)
            axes[idx].set_ylabel("Count")
            axes[idx].set_title(column)
        fig.tight_layout()
        st.pyplot(fig)
