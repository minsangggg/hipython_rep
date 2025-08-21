import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import numpy as np
import os

# --------------------------
# 페이지 함수 정의
# --------------------------

# 홈 화면 (Dashboard 느낌)
def show_home():
    st.title("🏠 부동산 매물 추천 서비스")
    st.markdown("사용자 조건에 맞는 맞춤형 매물을 추천하고, 선호도 트렌드를 시각화합니다.")

    # 1. 주요 지표 요약 (Metric 카드)
    st.subheader(" 주요 지표 요약")
    col1, col2, col3 = st.columns(3)
    col1.metric("전체 매물 수", "1,245", "+30")
    col2.metric("평균 보증금", "2,500만 원")
    col3.metric("인기 유형", "투룸/오피스텔/빌라")

      # 현재 실행 중인 파일 경로 기준
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # 이미지 경로 생성
    img1_path = os.path.join(BASE_DIR, "house1.png")
    img2_path = os.path.join(BASE_DIR, "house2.png")

    # 2. 오늘의 추천 매물
    st.subheader("오늘의 추천 매물")
    col1, col2 = st.columns(2)

    with col1:
        st.image("house1.png", width=250, caption="서울시 강남구 / 전세 2억")
    with col2:
        st.image("house2.png", width=250, caption="경기도 성남시 / 월세 80만 원")

    # 3. 최근 선호도 트렌드 그래프
    st.subheader("📈 최근 선호도 변화")
    df = pd.DataFrame({
        "Date": range(20),
        "원룸": pd.Series(np.random.randn(20)).cumsum(),
        "투룸/오피스텔/빌라": pd.Series(np.random.randn(20)).cumsum()
    })
    fig = px.area(df, x="Date", y=["원룸", "투룸/오피스텔/빌라"],
                  title="최근 1개월간 선호도 변화")
    fig.update_layout(yaxis_title="선호도", xaxis_title="날짜")
    st.plotly_chart(fig, use_container_width=True)

    # 4. 안내문
    st.info(" 왼쪽 사이드바에서 지역과 조건을 선택해 매물 추천을 받아보세요!")


# 조건 선택 페이지
def show_filters():
    st.header("조건 선택")
      
    # 0) 지역 선택
    region = st.selectbox("지역을 선택하세요", ["서울", "경기"])
    st.session_state["region"] = region
    
    # 1) 주거 형태 선택
    housing_type = st.radio(
        "선호 주거 형태를 선택하세요",
        ["원룸", "투룸/오피스텔/빌라"]
    )
    st.session_state["housing_type"] = housing_type

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


# 추천 결과 페이지
def show_results():
    st.header("추천 결과")

    # 임시 매물 데이터
    data = {
        "지역": ["서울", "서울", "경기", "경기"],
        "유형": ["원룸", "투룸/오피스텔/빌라", "원룸", "투룸/오피스텔/빌라"],
        "가격(만원)": [1500, 2500, 1200, 1800],
        "주소": ["서울시 A구", "서울시 B구", "경기도 C시", "경기도 D시"]
    }
    df = pd.DataFrame(data)

    st.write("### 전체 매물 리스트")
    st.dataframe(df)

    # 매물 선택
    selected = st.selectbox("📍 지도를 보고 싶은 매물을 선택하세요", df["주소"])
    
    if selected:
        st.success(f"선택된 매물: {selected}")

        # 주소별 임시 위도/경도 매핑
        coords = {
            "서울시 A구": (37.5665, 126.9780),
            "서울시 B구": (37.56, 126.99),
            "경기도 C시": (37.39, 127.11),
            "경기도 D시": (37.41, 127.15),
        }
        lat, lon = coords.get(selected, (37.5665, 126.9780))

        # 지도 생성
        m = folium.Map(location=[lat, lon], zoom_start=13)
        folium.Marker([lat, lon], popup=selected).add_to(m)

        # Streamlit에 출력
        st_folium(m, width=700, height=500)

    # 필터 적용 (조건 맞는 매물만 보여줌)
    filtered = df[
        (df["유형"] == st.session_state.get("housing_type", "원룸")) &
        (df["가격(만원)"].between(*st.session_state.get("price_range", (500, 5000))))
    ]

    st.write("### 즉시 계약 가능 매물")
    st.dataframe(filtered)


# 이용자 선호도 페이지
def show_preference_chart():
    st.header("이용자 선호도")

    df = pd.DataFrame({
        "Date": range(20),
        "원룸": pd.Series(np.random.randn(20)).cumsum(),
        "투룸/오피스텔/빌라": pd.Series(np.random.randn(20)).cumsum()
    })

    fig = px.area(
        df,
        x="Date",
        y=["원룸", "투룸/오피스텔/빌라"],
        title="선택한 매물 선호도"
    )

    fig.update_layout(
        yaxis_title="선호도",
        xaxis_title="날짜"
    )

    st.plotly_chart(fig, use_container_width=True)


# 문의하기 페이지
def show_contact():
    st.header("📬 문의하기")
    st.write("문의사항은 아래 이메일로 보내주세요: support@example.com")


# --------------------------
# 메인 실행 부분
# --------------------------
def main():
    st.sidebar.title("🏠 Main Menu")

    menu = st.sidebar.radio(
        "선택",
        ["홈", "조건 선택", "추천 결과", "이용자 선호도", "문의하기"]
    )

    if menu == "홈":
        show_home()
    elif menu == "조건 선택":
        show_filters()
    elif menu == "추천 결과":
        show_results()
    elif menu == "이용자 선호도":
        show_preference_chart()
    elif menu == "문의하기":
        show_contact()


if __name__ == "__main__":
    main()
