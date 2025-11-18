import streamlit as st
import pandas as pd
import os

st.title("알코올 질환 사망자 분석")

# ------- CSV 로드 함수 -------
def load_default_csv():
    """같은 폴더에 있는 dri.csv 로드"""
    encodings = ["utf-8", "cp949", "euc-kr", "latin1"]
    for enc in encodings:
        try:
            return pd.read_csv("dri.csv", encoding=enc)
        except:
            pass
    return None


uploaded = st.file_uploader("CSV 파일을 업로드하세요 (선택)", type=["csv"])

# 업로드 파일 우선, 없으면 기본파일 로드
df = None

if uploaded is not None:
    encodings = ["utf-8", "cp949", "euc-kr", "latin1"]
    for enc in encodings:
        try:
            df = pd.read_csv(uploaded, encoding=enc)
            break
        except:
            uploaded.seek(0)  # 다시 읽기 위해 포인터 초기화
else:
    # 기본 제공 CSV 자동 로드
    if os.path.exists("dri.csv"):
        df = load_default_csv()
    else:
        st.error("dri.csv 파일이 프로젝트 폴더에 없습니다.")
        st.stop()

# ----------- 데이터 표시 -----------
st.subheader("데이터 미리보기")
st.dataframe(df.head())

# 데이터 분리
df_rate = df[df["구분"] == "사망률"].sort_values("연도")
df_count = df[df["구분"] == "사망자수"].sort_values("연도")

# ----------- 그래프 출력 -----------
st.header("📊 사망률 그래프 (오래된 연도 → 최근 연도)")
st.bar_chart(df_rate.set_index("연도")["총계"])

st.header("📊 사망자수 그래프 (오래된 연도 → 최근 연도)")
st.bar_chart(df_count.set_index("연도")["총계"])
