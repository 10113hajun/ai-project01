import streamlit as st
st.title('웹서비스제작')
name=st.text_input('이름을 입력하세요:')
if st.button('인사말 생성'):
  st.write(name+'님 안녕하세요')
