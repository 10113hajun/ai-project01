import streamlit as st
import pandas as pd

st.title("알코올 질환 사망자 분석")

uploaded = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded is None:
    st.warning("CSV 파일을 업로드 해주세요.")
    st.stop()

# CSV 로드
encodings = ["utf-8", "cp949", "euc-kr", "latin1"]
df = None

for enc in encodings:
    try:
        df = pd.read_csv(uploaded, encoding=enc)
        break
    except Exception:
        uploaded.seek(0)  # 업로드 파일은 읽고 나면 포인터를 처음으로 되돌려야 함

# 그래도 안되면 utf-8로 불러보기
if df is None:
    uploaded.seek(0)
    df = pd.read_csv(uploaded, encoding="utf-8")

st.subheader("원본 데이터")
st.dataframe(df.head())

# 데이터 분리
df_rate = df[df["구분"] == "사망률"].sort_values("연도")
df_count = df[df["구분"] == "사망자수"].sort_values("연도")

# 사망률 그래프
st.header("📊 사망률 그래프 (오래된 연도 → 최근 연도)")
st.bar_chart(df_rate.set_index("연도")["총계"])

# 사망자수 그래프
st.header("📊 사망자수 그래프 (오래된 연도 → 최근 연도)")
st.bar_chart(df_count.set_index("연도")["총계"])
