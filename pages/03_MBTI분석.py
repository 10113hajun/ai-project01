# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Countries MBTI Viewer", layout="wide")

# --- 색상: 내림차순 빨강 → 파랑 그라데이션 ---
def rank_to_rgb_hex(rank_index, n_items):
    if n_items <= 1:
        t = 0.0
    else:
        t = rank_index / (n_items - 1)
    r = int(round(255 * (1 - t)))
    g = 0
    b = int(round(255 * t))
    return f"#{r:02x}{g:02x}{b:02x}"

# --- 데이터 로드 ---
@st.cache_data
def load_data(path="countriesMBTI_16types.csv"):
    df = pd.read_csv(path)
    mbti_cols = [c for c in df.columns if c != "Country"]
    return df, mbti_cols

df, mbti_cols = load_data()

st.title("🌍 Countries MBTI Explorer")

# ============================
#        🔵 탭 구성
# ============================
tab1, tab2 = st.tabs(["국가별 MBTI 보기", "MBTI 유형별 국가 순위"])

# ==========================================================
#                     🟦 TAB 1 — 국가별 MBTI 그래프
# ==========================================================
with tab1:

    st.subheader("국가를 선택하면 MBTI 유형 비율을 확인할 수 있습니다.")

    countries = df["Country"].tolist()
    selected = st.sidebar.selectbox("국가 선택", countries, index=0)

    row = df[df["Country"] == selected].iloc[0]
    values = row[mbti_cols].astype(float)

    mbti_df = (
        pd.DataFrame({"MBTI": mbti_cols, "Value": values.values})
        .sort_values("Value", ascending=False)
        .reset_index(drop=True)
    )

    n = len(mbti_df)
    mbti_df["Color"] = [rank_to_rgb_hex(i, n) for i in range(n)]

    # Plotly 그래프
    fig1 = go.Figure()
    fig1.add_trace(
        go.Bar(
            x=mbti_df["MBTI"],
            y=mbti_df["Value"],
            marker=dict(color=mbti_df["Color"]),
            hovertemplate="<b>%{x}</b><br>비율: %{y:.2%}<extra></extra>",
        )
    )

    fig1.update_layout(
        title=f"{selected} — MBTI 비율 (내림차순)",
        xaxis_title="MBTI 유형",
        yaxis_title="비율",
        yaxis_tickformat=".0%",
        template="plotly_white",
        height=520,
        margin=dict(t=60, l=30, r=30, b=40),
    )

    st.plotly_chart(fig1, use_container_width=True)

# ==========================================================
#                🟥 TAB 2 — MBTI 유형별 Top 국가
# ==========================================================
with tab2:

    st.subheader("MBTI 유형을 선택하면 해당 유형 비율이 높은 국가 TOP10을 보여줍니다.")

    mbti_selected = st.selectbox("MBTI 유형 선택", mbti_cols, index=0)

    # 선택된 MBTI에 대해 국가 정렬
    rank_df = (
        df[["Country", mbti_selected]]
        .rename(columns={mbti_selected: "Value"})
        .sort_values("Value", ascending=False)
        .reset_index(drop=True)
    )

    # Top 10 추출
    top10 = rank_df.head(10).copy()

    # 한국 포함 여부 확인
    korea_row = rank_df[rank_df["Country"] == "South Korea"]
    korea_included = not korea_row.empty and korea_row.index[0] < 10

    # 한국이 Top10에 없으면 추가
    if not korea_included and not korea_row.empty:
        korea_data = korea_row.copy()
        top10 = pd.concat([top10, korea_data], ignore_index=True)

    # 색상
    colors = []
    for i, row in top10.iterrows():
        if row["Country"] == "South Korea":
            colors.append("#ff0000")  # 한국은 무조건 빨간색
        else:
            colors.append(rank_to_rgb_hex(i, len(top10)))

    top10["Color"] = colors

    # Plotly 그래프 (가로 막대)
    fig2 = go.Figure()
    fig2.add_trace(
        go.Bar(
            x=top10["Value"],
            y=top10["Country"],
            orientation="h",
            marker=dict(color=top10["Color"]),
            hovertemplate="<b>%{y}</b><br>비율: %{x:.2%}<extra></extra>",
        )
    )

    fig2.update_layout(
        title=f"{mbti_selected} 유형 비율 — 상위 국가",
        xaxis_title="비율",
        yaxis_title="국가",
        xaxis_tickformat=".0%",
        template="plotly_white",
        height=600,
        margin=dict(t=60, l=100, r=40, b=40),
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.write("※ 한국이 Top10 안에 없으면 자동으로 추가하여 빨간색으로 표시합니다.")
