import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="DRI 분석", layout="wide")

st.title("DRI 사망자/사망률 데이터 분석")

# CSV 로드
@st.cache_data
def load_data():
    path = "/mnt/data/dri.csv"   # Streamlit Cloud 사용 시 사용자가 업로드하도록 수정 가능
    encodings = ["utf-8", "cp949", "euc-kr", "latin1"]
    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc)
            return df
        except:
            pass
    return pd.read_csv(path, encoding="utf-8", errors="replace")

df = load_data()

st.subheader("원본 데이터 미리보기")
st.dataframe(df.head(20))

# -----------------------------
# 데이터 분리
# -----------------------------
df_rate = df[df["구분"] == "사망률"].sort_values("연도")
df_count = df[df["구분"] == "사망자수"].sort_values("연도")

# -----------------------------
# 분석 내용 출력
# -----------------------------
st.subheader("데이터 기본 정보")
st.write(f"총 행 수: {df.shape[0]}")
st.write(f"총 열 수: {df.shape[1]}")
st.write(f"연도 범위: {df['연도'].min()} ~ {df['연도'].max()}")

st.subheader("요약 통계")
st.dataframe(df.describe(include='all'))

# -----------------------------
# 그래프 1: 사망률 막대 그래프
# -----------------------------
st.header("📊 사망률 (오래된 연도부터 오름차순)")

fig1, ax1 = plt.subplots(figsize=(12,5))
ax1.bar(df_rate["연도"], df_rate["총계"])
ax1.set_title("연도별 사망률 (총계 기준)")
ax1.set_xlabel("연도")
ax1.set_ylabel("사망률")
st.pyplot(fig1)

# -----------------------------
# 그래프 2: 사망자수 막대 그래프
# -----------------------------
st.header("📊 사망자수 (오래된 연도부터 오름차순)")

fig2, ax2 = plt.subplots(figsize=(12,5))
ax2.bar(df_count["연도"], df_count["총계"])
ax2.set_title("연도별 사망자수 (총계 기준)")
ax2.set_xlabel("연도")
ax2.set_ylabel("사망자수")
st.pyplot(fig2)

st.write("---")
st.write("※ 모든 기능은 pandas + matplotlib + streamlit 기본 라이브러리만 사용했습니다.")
