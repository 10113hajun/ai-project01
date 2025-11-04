import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천기", page_icon="🌟")

st.title("🌟 MBTI 진로 추천기")
st.write("안녕! 😀 아래에서 너의 MBTI를 고르면 어울릴 만한 진로를 추천해줄게!")

mbti_jobs = {
    "ISTJ": ["📊 회계사", "🏛 공무원"],
    "ISFJ": ["👶 보육교사", "🏥 간호사"],
    "INFJ": ["🧠 상담가", "🎨 예술가"],
    "INTJ": ["🧪 연구원", "💻 데이터 분석가"],
    "ISTP": ["🔧 기술 엔지니어", "🚓 경찰관"],
    "ISFP": ["🎨 디자이너", "🐾 동물관리사"],
    "INFP": ["✍️ 작가", "🎼 음악가"],
    "INTP": ["🔬 과학자", "🧩 시스템 설계자"],
    "ESTP": ["🏅 스포츠 코치", "💼 영업 담당자"],
    "ESFP": ["🎤 연예인", "🎉 이벤트 플래너"],
    "ENFP": ["🎙 크리에이터", "💡 기획자"],
    "ENTP": ["🚀 스타트업 창업가", "🧠 전략 컨설턴트"],
    "ESTJ": ["🏢 관리자", "⚖️ 법무 관련 직무"],
    "ESFJ": ["🧑‍🏫 교사", "🤝 인사 담당자"],
    "ENFJ": ["💬 심리 상담가", "🧑‍🏫 교육 전문가"],
    "ENTJ": ["📈 경영 컨설턴트", "🏗 프로젝트 매니저"]
}

selected_mbti = st.selectbox("👉 너의 MBTI를 선택해줘!", list(mbti_jobs.keys()))

if selected_mbti:
    st.subheader(f"🌈 {selected_mbti} 유형에게 어울리는 진로 추천!")
    jobs = mbti_jobs[selected_mbti]
    st.write(f"1) {jobs[0]}")
    st.write(f"2) {jobs[1]}")
    st.write("\n화이팅! 너의 길을 응원할게 🥰")
