import streamlit as st

# 페이지 설정 (맨 위에 있어야 함)
st.set_page_config(layout="centered", page_title="방구 대시보드", page_icon="💨")

# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "intro"

# Intro 페이지
def show_intro():
   

    col1, col2, col3 = st.columns([1,2,1])  # 비율 조정
    with col2:
        st.image("Study/hhh.png", width=400)

    st.markdown("<h2 style='text-align:center;'>방구</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>사회 초년생의 방구하기!</p>", unsafe_allow_html=True)

    # CSS로 Streamlit 버튼 스타일 덮어쓰기
    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            background-color: skyblue;
            color: white;
            padding: 12px 30px;
            font-size: 18px;
            border: none;
            border-radius: 8px;
        }
        div.stButton > button:first-child:hover {
            background-color: #4da6ff;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 실제 동작하는 버튼
    if st.button("지금 시작하기", use_container_width=True):
        st.session_state.page = "select_location"
        st.rerun()



# 지역 선택 페이지
def show_select_location():
    st.header("어떤 방식으로 지역을 정할까요?")
    option = st.radio("선택하세요:", ["회사 근처가 좋아요", "내가 원하는 동네"])
    
    if option == "회사 근처가 좋아요":
        company = st.text_input("회사 주소를 입력하세요")
        radius = st.slider("반경(km)", 1, 10, 3)
        if st.button("다음"):
            st.session_state.page = "filters"
    else:
        region = st.text_input("원하는 동네를 입력하세요")
        if st.button("다음"):
            st.session_state.page = "filters"

  
        
        
# 조건 선택 페이지
def show_filters():
    st.header("세부 조건을 선택하세요")
    age = st.selectbox("연령대", ["20대", "30대", "40대 이상"])
    deposit = st.slider("보증금(만원)", 0, 10000, (500, 2000))
    rent = st.slider("월세(만원)", 10, 200, (30, 70))
    size = st.slider("평수", 5, 50, (10, 20))
    rooms = st.slider("방 개수", 1, 5, 2)
    
    if st.button("완료"):
        st.success("조건이 저장되었습니다!")

# 메인 앱
if st.session_state.page == "intro":
    show_intro()
elif st.session_state.page == "select_location":
    show_select_location()
elif st.session_state.page == "filters":
    show_filters()
