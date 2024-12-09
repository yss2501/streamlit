import streamlit as st
from PIL import Image
import os
import pandas as pd

# 一つ目タイトル
st.title("Webアプリデプロイ初挑戦")

# 二つ目マークダウン項目
multi = '''Streamlitの機能
:blue[20個]お試しできるかな:rosette:'''
st.markdown(multi)

# セッションステートを初期化（選択肢のカウント）
if "selection_counts" not in st.session_state:
    st.session_state.selection_counts = {
        "秩父のジビエ": 0,
        "絶品卵かけごはん": 0,
        "ハワイのパンケーキ!?": 0,
        "秘密のばしょ": 0,
    }

# 三つ目選択リスト
option = st.selectbox(
    "埼玉県の魅力から気になるものを選んでください！",
    list(st.session_state.selection_counts.keys()),
)

# 選択肢ごとの処理
if st.button("決定", type="primary"):
    st.write(f"あなたは『{option}』を選択しました！")

    # カウントの更新
    st.session_state.selection_counts[option] += 1

    # 初期化
    image_paths = []
    caption = ""
    description = ""
    shop_data = None
    map_data = None

    if option == "秩父のジビエ":
        image_paths = ["images/01.jpg"]
        caption = "秩父の美味しいジビエ料理"
        description = "秩父地域で捕れる新鮮なジビエをぜひご賞味ください！"
        shop_data = pd.DataFrame({
            "店舗名": ["秩父ジビエレストラン"],
            "住所": ["埼玉県秩父市荒川小野原１７８"],
            "営業時間": ["11:00〜20:00"],
            "定休日": ["水曜日"],
            "電話番号": ["0494-XX-XXXX"]
        })
        map_data = {"lat": 36.0037435, "lon": 139.0081564}

    elif option == "絶品卵かけごはん":
        image_paths = ["images/09.jpg", "images/10.jpg"]
        caption = "酪農家直送！新鮮卵の卵かけごはん"
        description = "埼玉県の酪農家から届く新鮮な卵を使用した究極の卵かけごはんです。"
        shop_data = pd.DataFrame({
            "店舗名": ["埼玉酪農ファーム直営店"],
            "住所": ["埼玉県坂戸市多和目１３９−１"],
            "営業時間": ["10:00〜18:00"],
            "定休日": ["火曜日"],
            "電話番号": ["048-XX-XXXX"]
        })
        map_data = {"lat": 35.9244805, "lon": 139.3407268}

    elif option == "ハワイのパンケーキ!?":
        image_paths = ["images/02.jpg", "images/03.jpg", "images/04.jpg"]
        caption = "郊外のハワイアンカフェ"
        description = "海なし県でも、ハワイのパンケーキ食べれます"
        shop_data = pd.DataFrame({
            "店舗名": ["ハワイアンパンケーキカフェ"],
            "住所": ["埼玉県さいたま市緑区大間木１８５−１"],
            "営業時間": ["9:00〜17:00"],
            "定休日": ["日曜日"],
            "電話番号": ["048-874-8571"]
        })
        map_data = {"lat": 35.8186009, "lon": 138.8399372}

    elif option == "秘密のばしょ":
        image_paths = ["images/07.jpg", "images/08.jpg"]
        caption = "埼玉県の秘密のスポット"
        description = "知る人ぞ知る埼玉の隠れた名所。詳しくは訪れてからのお楽しみ！"
        shop_data = pd.DataFrame({
            "ヒント": ["静かな森の中にある観光スポット"],
            "詳細": ["詳しくは現地でお楽しみください"]
        })
        map_data = {"lat": 35.8149995, "lon": 138.8399238}

    # 画像の表示
    for path in image_paths:
        if os.path.exists(path):
            image = Image.open(path)
            st.image(image, caption=caption, use_container_width=True)
        else:
            st.error(f"画像が見つかりません: {path}")

    # 説明文の表示
    st.write(description)

    # お店情報の動的表示
    if shop_data is not None:
        st.markdown("### お店情報")
        st.table(shop_data)

    # 地図情報の表示
    if map_data:
        st.map(data={"lat": [map_data["lat"]], "lon": [map_data["lon"]]})

# グラフ表示（カスタム項目名を指定）
st.markdown("### 選択肢の人気グラフ")
counts_df = pd.DataFrame.from_dict(
    st.session_state.selection_counts, 
    orient="index", 
    columns=["人気度"]
)
counts_df.index.name = "選択肢"
st.bar_chart(counts_df)
