import streamlit as st
import requests
import time  # 画像の切り替えに使用
from datetime import datetime  # 日付取得用
import pandas as pd  # CSVファイルを読み込むため

# APIのURLと都市コード（東京固定）
city_code = "130010"  # 東京の都市コード
url = f"https://weather.tsukumijima.net/api/forecast/city/{city_code}"  # リクエストURL

# 天気情報を取得する関数
def get_weather(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.sidebar.error("天気情報を取得できませんでした。")
        return None

# CSVファイルから目的地データを読み込む関数
@st.cache_data
def load_destinations(csv_path):
    df = pd.read_csv(csv_path)
    return list(set(df["今の気持ち"].tolist()))

# Streamlitアプリ
st.title("練馬ワンダーランド")
st.sidebar.title("目的選択メニュー")

# 目的地選択
st.sidebar.subheader("目的を選択してください")
destination_csv = "./destinations.csv"  # CSVファイルのパス
try:
    destinations = load_destinations(destination_csv)
    selected_destination = st.sidebar.selectbox("目的地", sorted(destinations))
except FileNotFoundError:
    st.sidebar.error("目的地データ（CSVファイル）が見つかりません。")
    selected_destination = None

# 移動手段選択
st.sidebar.subheader("移動手段を選択してください")
transportation = st.sidebar.radio("移動手段", ("徒歩", "自転車", "タクシー"))

# 食事の有無
st.sidebar.subheader("食事の計画")
meal_plan = st.sidebar.radio("食事をしますか？", ("する", "しない"))

# 確定ボタン
if st.sidebar.button("確定"):

    # 「旅行プランの作成中...」メッセージをプレースホルダーに表示
    message_placeholder = st.empty()
    message_placeholder.write("旅行プランの作成中...")

    # 画像アニメーション用のプレースホルダー
    image_placeholder = st.empty()

    # 表示する画像のリスト
    image_paths = ["./0.png", "./1.png", "./2.png"]  # 画像ファイルを指定
    for image in image_paths:
        image_placeholder.image(image, use_container_width=True)  # 同じ位置に画像を更新
        time.sleep(1.5)  # 1.5秒ごとに画像を切り替え

    # アニメーション終了後、「旅行プランの作成中...」メッセージを削除
    message_placeholder.empty()

    # 最後に選択内容を表示
    image_placeholder.empty()  # 画像をクリア
    if selected_destination:
        st.write(f"**目的地**: {selected_destination}")
    st.write(f"**移動手段**: {transportation}")
    st.write(f"**食事**: {meal_plan}")

# サイドバーの下部に天気情報を表示
with st.sidebar:
    st.markdown("---")  # 水平線で区切りを追加

    # 現在の日付を取得してフォーマット
    today_date = datetime.now().strftime("%m/%d")  # mm/dd形式にフォーマット

    st.subheader(f"{today_date} 練馬の天気")  # 日付付きのタイトル

    # 天気情報を取得
    weather_json = get_weather(url)
    if weather_json:
        # 今日の天候情報とアイコンURLを取得
        today_weather = weather_json['forecasts'][0]['telop']  # 今日の天候（晴れ、曇り、雨など）
        today_icon_url = weather_json['forecasts'][0]['image']['url']  # アイコンURL

        # 天気情報をサイドバーの下部に表示
        st.image(today_icon_url, width=85)  # 天気アイコンを表示
        st.write(f"天気: {today_weather}")
