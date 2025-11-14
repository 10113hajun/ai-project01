# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Countries MBTI Viewer", layout="wide")

# --- 유틸: 색상 생성 (상위=빨강, 하위=파랑, 중간은 보라 계열을 거치는 그라데이션)
def rank_to_rgb_hex(rank_index, n_items):
    """
    rank_index: 0-based rank where 0 = highest (should be red), n_items-1 = lowest (should be blue)
    returns: "#rrggbb"
    """
    if n_items <= 1:
        t = 0.0
    else:
        t = rank_index / (n_items - 1)  # 0..1
    # linear interpolation between red (255,0,0) and blue (0,0,255)
    r = int(round(255 * (1 - t)))
    g = 0
    b = int(round(255 * t))
    return f"#{r:02x}{g:02x}{b:02x}"

# --- 데이터 로드
@st.cache_data
def load_data(path="countriesMBTI_16types.csv"):
    df = pd.read_csv(path)
    # 소소한 정리: Country 칼럼 존재 확인, MBTI 칼럼 리스트
    if "Country" not in df.columns:
        raise ValueError("CSV에 'Country' 컬럼이 없습니다.")
    # MBTI 컬럼들: Country 외 모든 컬럼
    mbti_cols = [c for c in df.columns if c != "Country"]
    return df, mbti_cols

try:
    df, mbti_cols = load_data()
except Exception as e:
    st.error(f"데이터 로드 실패: {e}")
    st.stop()

st.title("🌍 Countries MBTI Explorer")
st.markdown("국가를 선택하면 해당 국가의 16 MBTI 유형 비율을 인터랙티브한 Plotly 막대그래프로 보여줍니다.")

# 사이드바: 국가 선택
countries = df["Country"].tolist()
default_country = countries[0] if countries else None
selected = st.sidebar.selectbox("국가 선택", countries, index=countries.index(default_country) if default_country else 0)

# 선택 국가의 행 가져오기
row = df.loc[df["Country"] == selected]
if row.empty:
    st.warning("선택한 국가의 데이터가 없습니다.")
    st.stop()

# MBTI 비율 테이블 만들기
values = row[mbti_cols].iloc[0].astype(float)
mbti_df = pd.DataFrame({"MBTI": mbti_cols, "Value": values.values})
# 내림차순 정렬(그래프는 1등 빨강 → 아래로 파랑이 되도록)
mbti_df = mbti_df.sort_values("Value", ascending=False).reset_index(drop=True)

# 색상 생성: 인덱스(0=highest) → red, (n-1)=lowest → blue
n = len(mbti_df)
colors = [rank_to_rgb_hex(i, n) for i in range(n)]
mbti_df["color"] = colors

# Plotly 막대그래프 (인터랙티브)
fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=mbti_df["MBTI"],
        y=mbti_df["Value"],
        marker=dict(color=mbti_df["color"]),
        hovertemplate="<b>%{x}</b><br>비율: %{y:.2%}<extra></extra>"
    )
)

# 레이아웃 세부 조정
fig.update_layout(
    title=f"{selected} — MBTI 비율 (내림차순: 1등 빨강 → 아래로 파랑)",
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    yaxis_tickformat=".0%",
    template="plotly_white",
    margin=dict(t=80, l=40, r=40, b=40),
    height=520,
)

# 보조 정보: 1등 유형 강조
top_mbti = mbti_df.loc[0, "MBTI"]
top_val = mbti_df.loc[0, "Value"]

col1, col2 = st.columns((2, 3))
with col1:
    st.subheader(f"{selected}의 최상위 MBTI")
    st.metric(label=f"1위: {top_mbti}", value=f"{top_val:.2%}")
    st.write("MBTI 순위(내림차순):")
    st.dataframe(mbti_df[["MBTI", "Value"]].assign(Value=lambda d: d["Value"].map("{:.2%}".format)), use_container_width=True)

with col2:
    st.plotly_chart(fig, use_container_width=True)

# 데이터 다운로드 버튼 (선택적)
csv = row.to_csv(index=False).encode("utf-8")
st.download_button(
    label="선택 국가 데이터 CSV로 다운로드",
    data=csv,
    file_name=f"{selected}_MBTI.csv",
    mime="text/csv",
)

st.markdown("---")
st.markdown("⚙️ 사용 방법: 좌측 사이드바에서 국가를 선택하세요. 그래프는 해당 국가의 MBTI 유형 비율을 내림차순으로 표시하며, 색은 1위(빨강) → 최하위(파랑)로 그라데이션됩니다.")
