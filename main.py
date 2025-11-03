import streamlit as st
st.title('웹서비스제작')
name=st.text_input('이름을 입력하세요:')
st.selectbox('좋아하는 음식을 선택하세요:',['김치찌개,된장찌개'])
if st.button('인사말 생성'):
  st.info(name+'님 안녕하세요')
  st.warning('반가워요')
  st.error(천만해요')
  st.balloons()
