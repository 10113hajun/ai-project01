# app.py
# Streamlit app to visualize subway boarding+alighting sums by station for a chosen date and line
# - Works on Streamlit Cloud
# - Uses Plotly for an interactive bar chart
# - Highlights the top station in red; other stations are blue with progressively lower opacity

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title='지하철 이용량 히트바', layout='wide')
st.title('지하철 역별 이용량 (승차+하차) — Plotly + Streamlit')

# --- Helpers -------------------------------------------------

KOREAN_COLUMNS = {
    'date': ['사용일자', '일자', 'date'],
    'line': ['노선명', '노선', 'line'],
    'station': ['역명', '역', 'station'],
    'ons': ['승차총승객수', '승차', 'on', '승차총'],
    'offs': ['하차총승객수', '하차', 'off', '하차총']
}


def find_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None


def parse_dates(df, col):
    # Accept formats like YYYYMMDD (int or str), YYYY-MM-DD, etc.
    ser = df[col].astype(str).str.strip()
    # Try common patterns
    def try_parse(s):
        for fmt in ('%Y%m%d', '%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d'):
            try:
                return datetime.strptime(s, fmt).date()
            except Exception:
                continue
        # fallback: try pandas to_datetime
        try:
            return pd.to_datetime(s, errors='coerce').date()
        except Exception:
            return None

    return ser.apply(lambda x: try_parse(x))


# --- Load data ------------------------------------------------
st.markdown('**데이터 업로드**: CSV 파일을 업로드하거나 상위 폴더에 `subway.csv` 파일을 두세요.')
uploaded = st.file_uploader('CSV 파일 업로드', type=['csv'])

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded, encoding='utf-8')
    except Exception:
        try:
            df = pd.read_csv(uploaded, encoding='cp949')
        except Exception:
            st.error('CSV 파일을 읽는 중 오류가 발생했습니다. 인코딩 문제일 수 있습니다.')
            st.stop()
else:
    # fallback: try to read subway.csv from working dir (useful for Streamlit Cloud repo)
    try:
        df = pd.read_csv('../subway.csv', encoding='cp949')
        st.info('로컬 파일 `subway.csv`에서 로드했습니다.')
    except FileNotFoundError:
        st.warning('업로드된 파일이 없습니다. 먼저 CSV를 업로드하거나 repo에 `subway.csv`를 추가해주세요.')
        st.stop()
    except Exception:
        try:
            df = pd.read_csv('../subway.csv', encoding='utf-8')
            st.info('로컬 파일 `subway.csv`에서 로드했습니다 (utf-8).')
        except Exception:
            st.error('로컬 파일을 읽는 중 오류가 발생했습니다.')
            st.stop()

# find important columns
col_date = find_col(df, KOREAN_COLUMNS['date'])
col_line = find_col(df, KOREAN_COLUMNS['line'])
col_station = find_col(df, KOREAN_COLUMNS['station'])
col_on = find_col(df, KOREAN_COLUMNS['ons'])
col_off = find_col(df, KOREAN_COLUMNS['offs'])

required = {"사용일자": col_date, "노선명": col_line, "역명": col_station, "승차총승객수": col_on, "하차총승객수": col_off}
missing = [k for k,v in required.items() if v is None]
if missing:
    st.error(f'다음 필수 컬럼을 찾을 수 없습니다: {missing}. CSV 컬럼명을 확인해 주세요.')
    st.write('현재 컬럼:', list(df.columns))
    st.stop()

# parse dates
df['_date_parsed'] = parse_dates(df, col_date)
if df['_date_parsed'].isna().all():
    st.error('사용일자 컬럼을 날짜로 파싱할 수 없습니다. 형식을 확인해주세요 (예: YYYYMMDD 또는 YYYY-MM-DD).')
    st.stop()

# restrict date picker to 2025
min_date = datetime(2025,1,1).date()
max_date = datetime(2025,12,31).date()

# unique lines in data
lines = sorted(df[col_line].dropna().unique().tolist())

with st.sidebar:
    st.header('필터')
    sel_date = st.date_input('날짜 선택 (2025년)', value=min_date, min_value=min_date, max_value=max_date)
    sel_line = st.selectbox('호선 선택', options=lines)
    top_n = st.slider('표시할 역 개수 (상위 N)', min_value=5, max_value=100, value=20)

# filter
mask = (df['_date_parsed'] == sel_date) & (df[col_line] == sel_line)
filtered = df.loc[mask].copy()
if filtered.empty:
    st.warning('선택한 날짜와 호선에 해당하는 데이터가 없습니다. 다른 날짜/호선을 선택해 주세요.')
    st.stop()

# ensure numeric
filtered[col_on] = pd.to_numeric(filtered[col_on], errors='coerce').fillna(0)
filtered[col_off] = pd.to_numeric(filtered[col_off], errors='coerce').fillna(0)

filtered['total'] = filtered[col_on] + filtered[col_off]

# aggregate by station
agg = filtered.groupby(col_station).agg({col_on: 'sum', col_off: 'sum', 'total': 'sum'}).reset_index()
agg = agg.sort_values('total', ascending=False).reset_index(drop=True)

# limit to top_n
agg_top = agg.head(top_n).copy()

# prepare colors: 1st = red, others blue with decreasing opacity
colors = []
if len(agg_top) > 0:
    colors.append('rgba(255,0,0,1)')  # red for first
    if len(agg_top) > 1:
        # alphas decreasing from 0.95 down to 0.2
        import numpy as np
        alphas = np.linspace(0.95, 0.2, max(1, len(agg_top)-1))
        for a in alphas:
            colors.append(f'rgba(0,0,255,{a:.2f})')

# build interactive bar chart with Plotly
fig = go.Figure()
fig.add_trace(go.Bar(
    x=agg_top['total'][::-1],
    y=agg_top[col_station][::-1],
    orientation='h',
    marker=dict(color=colors[::-1]),  # reverse because we reversed order
    hovertemplate=(
        '<b>%{y}</b><br>'
        '총합: %{x}<br>'
        '승차 합: %{customdata[0]}<br>'
        '하차 합: %{customdata[1]}<extra></extra>'
    ),
    customdata=agg_top[[col_on, col_off]][::-1].values
))

fig.update_layout(
    title=f'{sel_date} — {sel_line} 호선 역별 이용량 (상위 {len(agg_top)})',
    xaxis_title='승차+하차 합계',
    yaxis_title='역명',
    margin=dict(l=180, r=40, t=80, b=40),
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.markdown('---')
with st.expander('원본 데이터 미리보기'):
    st.dataframe(filtered.head(200))

st.caption('앱: Streamlit + Plotly로 제작 — 상단의 파일 업로드 또는 repo의 subway.csv 사용')

