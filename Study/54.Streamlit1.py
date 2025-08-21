import streamlit as st

st.title('Title')
st.header('header')
st.subheader('subheader')

st.write('write 문장입니다.')
st.text('text 문장입니다')
st.markdown(
    '''
    This is main text.
    :red[빨강,] :blue[파랑,] :green[초록.]\n
    This is **Bold** and *Italic* text
    '''
)
st.code(
    """
import pandas as pd

def create_dataframe():
    data = {
        '이름': ['철수', '영희'],
        '나이': [30, 28]
    }
    return pd.DataFrame(data)

df = create_dataframe()
st.dataframe(df)
""", language='python')

st.divider()



st.button('Hello') #secondary type -->기본값 
st.button('Hello', type='primary')
st.button('Hello', type='primary', icon="👀")
st.button('Hello1', type='primary', disabled=True,key=1)


def button_write():
    st.write('버튼이 클릭되었습니다!')
st.button('Reset',type='primary')
st.button('activate', on_click=button_write)

clicked=st.button('activate2', type='primary')
if clicked:
    st.write('버튼2가 클릭되었습니다')

#######################################
st.header('같은 버튼 여러개 만들기')
#key주고 primary이용하여 activate button 5개 만들기

# 버튼 개수
n_buttons = 5

# 버튼 반복 생성
for i in range(n_buttons):
    if st.button(f"Activate Button {i+1}", type="primary", key=f"btn_{i}"):
        st.write(f"👉 Button {i+1} 눌림!")
       
   
#######################################   
   
   
st.markdown("-----")