""" get_data.py """

from pathlib import Path
import pandas as pd
import datetime
import streamlit as st

# @st.cache
class Get_Data():
    file_path = '../data'
    file_name = '*ja.csv'
    Encode = 'CP932'

    def get_data(self):
        #読み込むcsvファイルパスを取得して、DataFrameにする
        files = Path(self.file_path).glob(self.file_name)
        lists = [pd.read_csv(file, encoding=self.Encode) for file in files]
        df = pd.concat(lists)
        df = df[["ツイート本文", "時間", "インプレッション", "エンゲージメント", "エンゲージメント率", "リツイート", \
                "返信", "いいね", "ユーザープロフィールクリック", "URLクリック数", "ハッシュタグクリック", "詳細クリック"]]
        df.columns = ["Tweet", "Datetime", "Impression", "Engagement", "Eng_Ratio", "RT", "Return", "Good", \
                    "User_Click", "URL_Click", "Hash_Click", "Detail_Click"]
        df['Datetime'] = pd.to_datetime(df['Datetime'].apply(lambda x: x[:-5]))         #"Time"末尾の"+0000"を消しておく
        df = df.set_index('Datetime').sort_index()          #indexを"Time"に変更し、時間でソートする(降順)
        return df

    def time_select(self, df):
        start_time = (datetime.datetime.now() - datetime.timedelta(days=365))
        end_time = datetime.datetime.now()
        df = df[(df.index >= start_time) & (df.index <= end_time)]
        return df


    def evaluation_string(self, df, string_list):
        for string in string_list:
            df['{}'.format(string)] = df['Tweet'].apply(lambda x: 1 if '{}'.format(string) in x else 0)
        return df
