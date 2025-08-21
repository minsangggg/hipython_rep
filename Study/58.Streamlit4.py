import streamlit as st
import os

# 페이지 설정 (맨 위에 있어야 함)
st.set_page_config(layout="centered", page_title="방구 대시보드", page_icon="💨")

# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "intro"

# Intro 페이지
def show_intro():
    
    # 현재 파일(58.Streamlit4.py)이 있는 폴더 기준으로 경로 설정
    current_dir = os.path.dirname(__file__)
    image_path = os.path.join(current_dir, "hhh.png")

    col1, col2, col3 = st.columns([1,2,1])  # 비율 조정
    with col2:
        st.image(image_path, width=400)

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
    if st.button("⬅ 뒤로가기"):   # 🔙 Intro로
        st.session_state.page = "intro"
        st.rerun()
    
    
    
    st.header("어떤 방식으로 지역을 정할까요?")
    option = st.radio("선택하세요:", ["회사 근처가 좋아요", "내가 원하는 동네"])
    
    if option == "회사 근처가 좋아요":
        company = st.text_input("회사 주소를 입력하세요")
        radius = st.slider("반경(km)", 1, 10, 3)
        if st.button("다음"):
            st.session_state.page = "filters"
            st.rerun()   # 🔑 rerun 바로 호출
    else:
        region = st.text_input("원하는 동네를 입력하세요")
        if st.button("다음"):
            st.session_state.page = "filters"
            st.rerun()   # 🔑 rerun 바로 호출

  
        
        
# 조건 선택 페이지
def show_filters():
    if st.button("⬅ 뒤로가기"):   # 🔙 지역 선택으로
        st.session_state.page = "select_location"
        st.rerun()

        
    st.header("세부 조건을 선택하세요")
    age = st.selectbox("연령대", ["20대", "30대", "40대 이상"])
    deposit = st.slider("보증금(만원)", 0, 10000, (500, 2000))
    rent = st.slider("월세(만원)", 10, 200, (30, 70))
    size = st.slider("평수", 5, 50, (10, 20))
    rooms = st.slider("방 개수", 1, 5, 2)
    
    if st.button("완료"):
        st.success("조건이 저장되었습니다!")
          # 🔑 다음 페이지로 이동 (예: 결과 페이지)
        st.session_state.page = "results"
        st.rerun()

# 결과 페이지 (예시)
def show_results():
    if st.button("⬅ 뒤로가기"):   # 🔙 조건 선택으로
        st.session_state.page = "filters"
        st.rerun()
    
    st.markdown("<h2 style='text-align:center;'>추천 매물 결과</h2>", unsafe_allow_html=True)
    
    # 예시 데이터 (DB 또는 크롤링 데이터로 교체 가능)
    results = [
        {
            "title": "강남 오피스텔",
            "image": "house1.png",
            "price": "월세 50 / 보증금 1000",
            "location": "서울 강남구 역삼동",
            "size": "20평 / 1.5룸",
        },
        {
            "title": "신촌 원룸",
            "image": "house2.png",
            "price": "월세 40 / 보증금 500",
            "location": "서울 서대문구 창천동",
            "size": "12평 / 원룸",
        },
        {
            "title": "잠실 투룸",
            "image": "house3.png",
            "price": "월세 70 / 보증금 2000",
            "location": "서울 송파구 잠실동",
            "size": "25평 / 2룸",
        },
    ]

    # 카드 형식으로 결과 출력
    for r in results:
        with st.container():
            col1, col2 = st.columns([1,2])
            with col1:
                img_path = os.path.join(os.path.dirname(__file__), r["image"])
                st.image(img_path, width=150)
            with col2:
                st.subheader(r["title"])
                st.write(f"📍 {r['location']}")
                st.write(f"🏠 {r['size']}")
                st.write(f"💰 {r['price']}")
                if st.button("상세보기", key=r["title"]):
                    st.info(f"{r['title']} 상세 페이지로 이동합니다 (추후 구현).")

        st.markdown("---")  # 구분선
    
    
    
    if st.button("처음으로 돌아가기"):
        st.session_state.page = "intro"
        st.rerun()


# 메인 앱
if st.session_state.page == "intro":
    show_intro()
elif st.session_state.page == "select_location":
    show_select_location()
elif st.session_state.page == "filters":
    show_filters()
elif st.session_state.page == "results":   # ✅ 결과 페이지 분기 추가
    show_results()