# app.py
import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="외국인 인기 관광지 Top10 (Korea)", layout="wide")

st.title("🇰🇷 외국인이 좋아하는 한국 관광지 Top 10 — 지도 표시 (Folium + Streamlit)")
st.markdown("""
아래 마커를 클릭하면 장소 이름과 간단 설명을 볼 수 있습니다.
(데이터 출처: VisitKorea, TripAdvisor, Lonely Planet 등)  
""")

# 기본 지도 중심 (서울)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=7, tiles="OpenStreetMap")

# 관광지 리스트 (이름, 위도, 경도, 간단 설명)
spots = [
    {
        "name": "Gyeongbokgung Palace (경복궁)",
        "lat": 37.5796, "lon": 126.9770,
        "desc": "조선의 대표 궁궐. 한복 체험과 수문장 교대식으로 인기."
    },
    {
        "name": "Changdeokgung + Secret Garden (창덕궁 & 비원)",
        "lat": 37.5796, "lon": 126.9910,
        "desc": "유네스코 세계유산. 비원의 정원 경치가 유명."
    },
    {
        "name": "N Seoul Tower (N서울타워, 남산타워)",
        "lat": 37.5512, "lon": 126.9882,
        "desc": "서울 전경을 한눈에 볼 수 있는 전망 타워."
    },
    {
        "name": "Myeongdong (명동)",
        "lat": 37.5636, "lon": 126.9850,
        "desc": "쇼핑·길거리음식·뷰티로 외국인에게 인기 많은 상업지."
    },
    {
        "name": "Bukchon Hanok Village (북촌한옥마을)",
        "lat": 37.5825, "lon": 126.9857,
        "desc": "전통 한옥이 모여있는 역사적 마을, 사진 명소."
    },
    {
        "name": "Insadong (인사동)",
        "lat": 37.5744, "lon": 126.9850,
        "desc": "전통 공예품·찻집이 많은 전통문화 거리."
    },
    {
        "name": "Nami Island (남이섬)",
        "lat": 37.7914, "lon": 127.5250,
        "desc": "드라마 촬영지로 유명한 강가의 아름다운 섬."
    },
    {
        "name": "Seongsan Ilchulbong (성산 일출봉, 제주)",
        "lat": 33.4607, "lon": 126.9409,
        "desc": "제주 대표 자연 명소 — 일출과 주상절리."
    },
    {
        "name": "Gamcheon Culture Village (감천문화마을, 부산)",
        "lat": 35.0975, "lon": 129.0307,
        "desc": "형형색색 건물과 골목 아트로 유명한 부산 관광지."
    },
    {
        "name": "Haeundae Beach (해운대 해수욕장, 부산)",
        "lat": 35.1587, "lon": 129.1604,
        "desc": "부산의 대표 해변 — 연중 많은 관광객 방문."
    },
]

# 마커 추가
for s in spots:
    popup_html = f"""
    <b>{s['name']}</b><br>
    {s['desc']}<br>
    <i>위도: {s['lat']}, 경도: {s['lon']}</i>
    """
    folium.Marker(
        location=[s['lat'], s['lon']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=s['name'],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Folium 지도를 Streamlit에 렌더링
st_data = st_folium(m, width=1200, height=700)

# 오른쪽 사이드바: 선택된 마커 정보 표시 (있을 경우)
st.sidebar.header("선택 정보")
if st_data and "last_active_drawing" in st_data:
    st.sidebar.write(st_data["last_active_drawing"])
else:
    st.sidebar.write("마커를 클릭하면 상세 정보가 여기에 표시됩니다.")

st.markdown("---")
st.caption("데이터/추천 정보 출처: VisitKorea, TripAdvisor, Lonely Planet 등. (예시용 목록이며 필요하면 직접 순위·위치·설명을 조정하세요.)")
