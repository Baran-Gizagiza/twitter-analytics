""" manage.py """

from views import Views
from get_data import Get_Data
from time_analytics import Time_Analytics
from preprocessing_data import PreProcessing
from static_analytics import Static_Analysis
from sns_graph import SNS_Graph
import streamlit as st
import pandas as pd

# 出力ファイルディレクトリとファイル名を指定してください
Outputfile = "../output/better_tweet.xlsx"
# Option: 分析したい文字列をリストで渡してください
string_list = []    # 例: string_list = ['ブログ', 'Python', 'Docker']
# 月ごとのフォロワー数を入力してください。新たに追加することもできます。
follower = {
        '2020-06':15,
        '2020-07':45,
        '2020-08':100,
        '2020-09':70,
        '2020-10':50,
        '2020-11':60,
        '2020-12':20,
        '2021-01':40,
        '2021-02':20,
        '2021-03':35,
        }

target = '+1 followers'

# Follower数の分析を行います
st.title('1. Twitter Analytics for {}'.format(target))
df = Get_Data().get_data()
df = Get_Data().time_select(df)
df = Get_Data().evaluation_string(df, string_list)
df = Time_Analytics().time_trend(df)
df["Impression"] = df["Impression"] / 1000  # Impressionは数字が大きくなりやすいので1000で割ります

# パラメータ呼び出し
st.sidebar.header("Parameter")
corr_rank = Views().corr_rank()
quan = Views().quan()
target_2 = Views().target_column(df)
level = Views().level()
percent = Views().percent()
hue_string = Views().hue_string(string_list)
fileoutput = Views().file_output_value()

# 月ごとのTweet解析
st.header("1-1. Mothly data")
df_reset = df.reset_index()
df_reset["Year-Month"] = df_reset["date"].dt.strftime("%Y-%m")
df_month = df_reset.groupby("Year-Month").sum()
df_month["Eng_Ratio"] = df_month["Engagement"] / df_month["Impression"]
df_month[target] = pd.DataFrame(follower.values(), index=df_month.index)
df_month = df_month.iloc[:, 6:]
st.subheader(target)
st.bar_chart(df_month[target])
month_detail = st.checkbox("Detail Month data")
if month_detail:
    st.dataframe(df_month)

# 単回帰分析
st.header('1-2. Single Regresion Analytics')
df_month_corr = df_month.corr()
related_month = df_month_corr[(abs(df_month_corr[target])>corr_rank) & (abs(df_month_corr[target]) < 1)].index
# 関連するカラムがない場合、corr_rankを下げることで関連カラムを取得できます。
if len(related_month) == 0:
    st.warning("There are related columns for {}. Decrease 'corr_rank' and try again!".format(target))
else:
    st.success("There are related columns for {}".format(target))
    reg_summary = Static_Analysis().single_reg(df_month, related_month, target)
    SNS_Graph().sns_scatter(df_month, target, related_month, reg_summary)
    single_detail = st.checkbox("Detail Single Regresion")
    if single_detail:
        st.dataframe(reg_summary)

    # 重回帰分析
    st.header('1-3. Multi Regresion Analytics')
    reg_summary_2 = Static_Analysis().multi_reg_scaled(df_month, related_month, target)
    reg_summary_3 = Static_Analysis().multi_reg(df_month, related_month, target)
    with st.beta_container():
        col1, col2 = st.beta_columns([1, 2])
    with col1:
        st.subheader("Scaled")
        st.dataframe(reg_summary_2)
    with col2:
        st.subheader("Normal")
        st.dataframe(reg_summary_3)

    # "Target column"で選択したカラムの分析を行います
    analyze = st.sidebar.button('Analyze',)
    if analyze:
        st.title('2. Twitter Analytics for {}'.format(target_2))

        st.header('2-1. Raw Data')
        # target_2の上位(quan)%以上を除外します。除外しない場合は100%を選択します。
        df_quan = PreProcessing().quantile(df_reset, target_2, quan).iloc[:, 6:]
        st.dataframe(df_quan)

        # カラムの件数、levelで表示レンジを変更可能
        st.header('2-2. Time Trend')
        df_graph = Time_Analytics().trend_by_level(df, level, "sum")
        st.bar_chart(df_graph[target_2])

        st.header('2-3. Histgram')
        PreProcessing().histgram_target(df_quan, target_2)
        df_corr = df_quan.corr()
        related = df_corr[(abs(df_corr[target_2])>corr_rank) & (abs(df_corr[target_2]) < 1)].index
        # 関連するカラムがない場合、corr_rankを下げることで関連カラムを取得できます。
        if len(related) == 0:
            st.warning("There are related columns for {}. Decrease 'corr_rank' and try again!".format(target_2))
        else:
            st.success("There are related columns for {}".format(target_2))
            PreProcessing().histgram_related(df_quan, related)

            st.header('2-4. Single Regresion Analytics')
            reg_summary_4 = Static_Analysis().single_reg(df_quan, related, target_2)
            SNS_Graph().sns_scatter(df_quan, target_2, related, reg_summary_4, hue=hue_string, N=3)

            st.header('2-5. Multi Regresion Analytics')
            reg_summary_5 = Static_Analysis().multi_reg_scaled(df_quan, related, target_2)
            reg_summary_6 = Static_Analysis().multi_reg(df_quan, related, target_2)
            with st.beta_container():
                col3, col4 = st.beta_columns([1, 2])
            with col3:
                st.subheader("Scaled")
                st.dataframe(reg_summary_5)
            with col4:
                st.subheader("Normal")
                st.dataframe(reg_summary_6)

            st.header('3. Good tweet for {}'.format(target_2))
            df_eval = df_reset.iloc[:, 6:].copy()
            for column in related:
                df_eval = Static_Analysis().evaluation_percent(df_eval, column, 'eval_{}'.format(column), percent)
                df_eval = df_eval[df_eval['eval_{}'.format(column)]==1]
            st.table(df_eval.iloc[:, :2])

            # ”Good Tweet”をexcelで出力するかどうかを選択できます。
            if fileoutput:
                df_eval.to_excel(Outputfile, encoding="utf-8", index=False)
