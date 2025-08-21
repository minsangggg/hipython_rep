import streamlit as st
import pandas as pd
import plotly.express as px


#layout 요소
#columns는 요소를 왼쪽-> 오른쪽으로 배치가능

col1, col2=st.columns(2)

with col1:
    st.metric(
     '오늘의 날씨',
     value='35도',
     delta='+3'
)

with col2:
    st.metric(
    '오늘의 미세먼지',
    value='좋음',
    delta='-30',
    delta_color='inverse'
)
    
##
st.markdown('---')


data={
    '이름': ['홍길동','김길동','박길동'],
    '나이': [10,20,30]
}
df=pd.DataFrame(data)
st.dataframe(df)


st.divider()

st.table(df)

st.divider()


st.json(data)


#datafile.csv > load >table 출력 >px.box() >st.plotly_chart()


df=pd.read_csv('data/ABNB_stock.csv')
print(df)
df

df['Date']=pd.to_datetime(df['Date'])
df['YearMonth']=df['Date'].dt.to_period('M').astype(str)

fig=px.box(df, x="YearMonth", y="Close", title="ABNB 월별 종가")

st.plotly_chart(fig, use_container_width=True)

################
# 3. Plotly Line Chart 생성
fig = px.line(df, x='Date', y='Close', title="ABNB 주가 (Line Chart)")

# 4. Streamlit에 출력
st.plotly_chart(fig, use_container_width=True)


##################
#위젯을 활용한 interactive 그래프 표현하기


# CSV 불러오기
df = pd.read_csv("data/airline_stats.csv")
print(df)
df

# 선택할 수 있는 옵션 지정
x_options = ['airline']   # 범주형 -> x축
y_options = ['pct_carrier_delay', 'pct_atc_delay', 'pct_weather_delay']
hue_options = ['airline'] # 색상 분류 기준

# Streamlit 위젯
x_option = st.selectbox('Select X-axis', 
                        options=x_options, 
                        )
y_option = st.selectbox('Select Y-axis', 
                        options=y_options, 
                        )
hue_option = st.selectbox('Select Hue', 
                          options=hue_options, 
)

# 선택된 값으로 Bar Chart 생성
if (x_option is not None) and (y_option is not None):
    if hue_option:
        fig = px.bar(
            df,
            x=x_option,
            y=y_option,
            color=hue_option,
            title=f"{y_option} by {x_option}",
            barmode="group"
        )
    else:
        fig = px.bar(
            df,
            x=x_option,
            y=y_option,
            title=f"{y_option} by {x_option}"
        )
    st.plotly_chart(fig, use_container_width=True)

