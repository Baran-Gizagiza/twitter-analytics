""" sns_graph.py """

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(font='Yu Gothic') # sns.set(font='DejaVu Sans')

class SNS_Graph():
    def sns_scatter(self, df, target, related, reg_summary, hue=None, N=3):
        fdic = {
            #"family" : "Georgia",
            #"style" : "italic",
            "size" : 12,
            "color" : "Black",
            #"weight" : "heavy"
        }

        boxdic = {
            "facecolor" : "White",
            "edgecolor" : "Black",
            "boxstyle" : "Round",
            "linewidth" : 1
        }

        width = 15
        height = 6

        max_size = len(related)
        q, r = divmod(max_size, N)
        if q == 0 or (q == 1 and r == 0):
            fig, axes = plt.subplots(1, N, figsize=(width, height))
            for idx, column in enumerate(related):
                sns.set(font='Yu Gothic')
                sns.scatterplot(data=df,
                                x=column,
                                y=target,
                                alpha=0.5,
                                hue=hue,
                                ax=axes[idx],
                                legend="full"
                                )
                yhat = reg_summary["Coef"][idx] * df[column]
                axes[idx].plot(df[column], yhat, lw=3, c='red', label="Linear")
                axes[idx].set_xlabel(column)
                axes[idx].set_ylabel(target)
                axes[idx].set_title(column)
                axes[idx].text(1, -max(df[target])//10*1, "{0}: {1}".format(target, reg_summary[target][idx]), fontdict=fdic, bbox=boxdic)
                axes[idx].text(1, -max(df[target])//10*2.5, "R2: {}".format(reg_summary["R2"][idx]), fontdict=fdic, bbox=boxdic)
                axes[idx].set_xlim(0)
                axes[idx].set_ylim(-max(df[target])//10*3, max(df[target])*1.2)
                axes[idx].legend(title="Hue: {}".format(hue), loc='lower right')
        else:
            if q >= 2 and r == 0:
                fig, axes = plt.subplots(q, N, figsize=(width, height*q))
            else:
                fig, axes = plt.subplots(q+1, N, figsize=(width, height*(q+1)))
            for idx, column in enumerate(related):
                x = idx // N
                y = idx % N
                sns.set(font='Yu Gothic')
                sns.scatterplot(data=df,
                                x=column,
                                y=target,
                                alpha=0.5,
                                hue=hue,
                                ax=axes[x, y],
                                legend="full"
                                )
                yhat = reg_summary["Coef"][idx] * df[column]
                axes[x, y].plot(df[column], yhat, lw=3, c='red', label="Linear")
                axes[x, y].set_xlabel(column)
                axes[x, y].set_ylabel(target)
                axes[x, y].set_title(column)
                axes[x, y].text(1, -max(df[target])//10*1, "{0}: {1}".format(target, reg_summary[target][idx]), fontdict=fdic, bbox=boxdic)
                axes[x, y].text(1, -max(df[target])//10*2.5, "R2: {}".format(reg_summary["R2"][idx]), fontdict=fdic, bbox=boxdic)
                axes[x, y].set_xlim(0)
                axes[x, y].set_ylim(-max(df[target])//10*3, max(df[target])*1.2)
                axes[x, y].legend(title="Hue: {}".format(hue), loc='lower right')
        st.pyplot(fig)
