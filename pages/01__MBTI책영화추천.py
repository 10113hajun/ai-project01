import streamlit as st

# MBTI 추천기 (Streamlit용, 외부 라이브러리 불필요)
# 이 파일은 UTF-8로 저장되어야 합니다.

st.set_page_config(page_title="MBTI 추천기", page_icon=":sparkles:")

MBTI_LIST = [
    "ISTJ","ISFJ","INFJ","INTJ",
    "ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP",
    "ESTJ","ESFJ","ENFJ","ENTJ",
]

RECOMMENDATIONS = {
    "ISTJ": {
        "books": [
            ("성공하는 사람들의 7가지 습관", "Stephen R. Covey", "실용적이고 체계적인 습관을 다루어 안정적인 성취에 도움을 줘요. 📈"),
            ("미움받을 용기", "기시미 이치로·고가 후미타케", "자기 책임과 내적 원칙을 다시 생각하게 해주는 책이에요. 💡"),
        ],
        "movies": [
            ("인턴", "The Intern (2015)", "일과 책임을 성실히 해내는 모습이 공감돼요. 👔"),
            ("설국열차", "Snowpiercer (2013)", "질서와 시스템, 책임의 무게를 생각하게 하는 영화. 🚆"),
        ],
    },
    # (중략) 다른 MBTI 항목들은 동일한 형식으로 유지됩니다.
}

# --- UI 구성 ---
st.title("MBTI별 책·영화 추천기 🎯")
st.write("아래에서 당신의 MBTI를 골라보세요 — 간단한 추천과 이유를 보여드릴게요! 😊")

choice = st.selectbox("당신의 MBTI를 선택하세요", MBTI_LIST)

if st.button("추천 받기 🎁"):
    rec = RECOMMENDATIONS.get(choice)
    if not rec:
        st.info("아직 해당 MBTI에 대한 추천이 준비되지 않았어요. 😅")
    else:
        st.subheader("📚 책 추천 — {}".format(choice))
        for i, item in enumerate(rec.get("books", []), start=1):
            title, author, reason = item
            # 마크다운에 f-string을 직접 쓰지 않고 format을 사용합니다.
            st.markdown("**{}. {}** — _{}_  \n{}".format(i, title, author, reason))

        st.subheader("🎬 영화 추천 — {}".format(choice))
        for i, item in enumerate(rec.get("movies", []), start=1):
            title, info, reason = item
            st.markdown("**{}. {}** — _{}_  \n{}".format(i, title, info, reason))

        st.write("즐거운 감상 되세요! 필요하면 추천을 더 바꿔줄게요. 😄")

st.write("---")
st.caption("※ 추천 도서는 대한민국에서 판매되는 번역본/원서로 구할 수 있는 작품들을 중심으로 선정했습니다.")
