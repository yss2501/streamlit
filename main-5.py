import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

st.title('Streamlit Hello World') # タイトル

st.write('Interactive Widgets') # ウィジェットの表示

text = st.sidebar.text_input('あなたの趣味を教えてください。') # テキスト入力
'あなたの趣味は', text, 'です。' # テキスト表示

condition = st.sidebar.slider('あなたの今の調子は？', 0, 100, 50) # スライダー
'コンディション：', condition # テキスト表示