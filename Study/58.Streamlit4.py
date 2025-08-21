import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------
# 페이지 함수 정의
# --------------------------

def show_intro():
    st.title("🏠 부동산 추천 서비스")
    st.write("환영합니다! 사이드바에서 메뉴를 선택해주세요.")

def show_select_location():
    st.header("📍 지역 선택")
    region = st.selectbox("지역을 선택하세요", ["서울", "경기", "부산", "대구", "기타"])
    st.session_state["region"] = region
    st.success(f"선택된 지역: {region}")

def show_filters():
    st.header("⚙️ 조건 선택")

    # ✅ 주거 형태 선택 (원룸, 투룸/오피스텔/빌라)
    housing_type = st.radio(
        "선호 주거 형태를 선택하세요",
        ["원룸", "투룸/오피스텔/빌라"]
    )
    st.session_state["housing_type"] = housing_type
    st.info(f"선택된 주거 형태: {housing_type}")

       # 2) 가격 범위
    price_range = st.slider("가격 범위 (만원)", 500, 5000, (1000, 3000))
    st.session_state["price_range"] = price_range

    # 3) 면적 범위
    size_range = st.slider("면적 범위 (평)", 5, 100, (10, 40))
    st.session_state["size_range"] = size_range

    # 4) 옵션 선택
    options = st.multiselect(
        "옵션 선택",
        ["주차 가능", "엘리베이터", "보안시설", "반려동물 가능", "가구 포함"]
    )
    st.session_state["options"] = options

    # 5) 교통편
    transport = st.selectbox("교통편 접근성", ["상관없음", "지하철 5분 이내", "버스정류장 5분 이내"])
    st.session_state["transport"] = transport

    # 6) 입주 가능일
    move_in = st.date_input("입주 가능일 선택")
    st.session_state["move_in"] = move_in

     
def show_results():
    st.header("📊 추천 결과")

    # 임시 매물 데이터
    data = {
        "지역": ["서울", "서울", "경기", "부산"],
        "유형": ["원룸", "투룸/오피스텔/빌라", "원룸", "투룸/오피스텔/빌라"],
        "가격(만원)": [1500, 2500, 1200, 1800],
        "주소": ["서울시 A구", "서울시 B구", "경기도 C시", "부산 D구"]
    }
    df = pd.DataFrame(data)

    # 필터 적용
    filtered = df[
        (df["유형"] == st.session_state.get("housing_type", "원룸")) &
        (df["가격(만원)"].between(*st.session_state.get("price_range", (500, 5000))))
    ]

    st.write("### 추천 매물 리스트")
    st.dataframe(filtered)

def show_preference_chart():
    st.header(" 이용자 선호도")

    # 예시 데이터
    df = pd.DataFrame({
        "Date": range(20),
        "a": pd.Series(np.random.randn(20)).cumsum(),
        "b": pd.Series(np.random.randn(20)).cumsum(),
        "c": pd.Series(np.random.randn(20)).cumsum(),
    })

    fig = px.area(df, x="Date", y=["a", "b", "c"], title="주거 형태 선호도 변화")
    st.plotly_chart(fig, use_container_width=True)

def show_contact():
    st.header("📬 문의하기")
    st.write("문의사항은 아래 이메일로 보내주세요: support@example.com")

# --------------------------
# 메인 실행 부분
# --------------------------
def main():
    st.sidebar.title("🏠 Main Menu")

    menu = st.sidebar.radio(
        "Navigation",
        ["홈", "지역 선택", "조건 선택", "추천 결과", "이용자 선호도", "문의하기"]
    )

    if menu == "홈":
        show_intro()
    elif menu == "지역 선택":
        show_select_location()
    elif menu == "조건 선택":
        show_filters()
    elif menu == "추천 결과":
        show_results()
    elif menu == "이용자 선호도":
        show_preference_chart()
    elif menu == "문의하기":
        show_contact()

if __name__ == "__main__":
    import numpy as np
    main()
