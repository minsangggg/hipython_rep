import streamlit as st

st.set_page_config(layout="wide")
st.title("방구 대시보드 (프로토타입 뷰어)")

# 사이드바 메뉴
menu = st.sidebar.selectbox(
    "페이지 선택",
    [
        "index", "region", "region_seoul",
        "company_address_search", "filters", "detail_filters",
        "results", "result2", "detail", "agent_review"
    ]
)

# 파일 경로 매핑
pages = {
    "index": "index.html",
    "region": "region.html",
    "region_seoul": "region_seoul.html",
    "company_address_search": "company_address_search.html",
    "filters": "filters.html",
    "detail_filters": "detail_filters.html",
    "results": "results.html",
    "result2": "result2.html",
    "detail": "detail.html",
    "agent_review": "agent_review.html"
}

# 선택된 파일 불러오기
file_path = pages[menu]
with open(file_path, "r", encoding="utf-8") as f:
    html_code = f.read()

st.components.v1.html(html_code, height=800, scrolling=True)
