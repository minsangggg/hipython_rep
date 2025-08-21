import streamlit as st
from PIL import Image


#분석페이지의 분석탭 구성함수
def make_anal_tab():
    st.header('탭 추가')
    
    tab1, tab2, tab3=st.tabs(['차트','데이터','설정'])
    with tab1:
        st.subheader('차트 탭')
        st.bar_chart({'데이터': [1,2,3,4,5]})
    
    with tab2:
        st.subheader('데이터 탭')
        st.dataframe({'기준': ['a','b','c','d','e'], '값':[1,2,3,4,5]})
    
#체크박스(활성화여부),슬라이더(업데이트 주기 sec)   
    with tab3:
     st.subheader('데이터 탭')
     st.checkbox('자동 업데이트 활성화 여부')
     st.slider('업데이트 주기 (sec) ', 1,60,10)
    #3번째 설정 탭 : 체크박스(활성화여부), 슬라이더(업데이트 주기sec)


st.title("Streamlit 웹 페이지 구성하기")

st.sidebar.header('메뉴')
selected_menu=st.sidebar.selectbox(
    '메뉴선택', ['메인','분석','설정']
)

images = [
    ("./images/img.png", "img"),
    ("./images/img2.png", "img2"),
    ("./images/img3.png", "img3")
]


# 선택에 따라 메인 화면 내용 변경
if selected_menu == '메인':
    st.header('홈페이지')
    st.write('환영합니다!')
    cols = st.columns(len(images))  # 이미지 개수만큼 컬럼 생성
    for col, (path, caption) in zip(cols, images):
        with col:
         img = Image.open(path)
         st.image(img, width=235, caption=caption)
elif selected_menu == '분석':
    st.header('데이터 분석 페이지')
    st.write('여기서 데이터를 분석해보세요.')
    make_anal_tab()
else:
    st.header('설정')
    st.write('앱 설정을 변경할 수 있습니다.')

if st.sidebar.button('선택'):
    st.sidebar.write('선택을 클릭하셨습니다')
    
#슬라이드바 추가 0~100, 50
st.sidebar.slider('슬라이더',0,100,50)  
st.divider()

# 확장영역 추가
st.header('익스팬더 추가')

with st.expander('숨긴 영역'):
  st.write('여기는 보이지 않습니다. 클릭해야 보입니다.')
  
