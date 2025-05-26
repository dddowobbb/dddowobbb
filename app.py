import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

st.set_page_config(page_title="Diabetes Data Visualization", layout="wide")

st.title("📊 당뇨병 데이터 시각화 대시보드")
st.markdown("Google Drive에서 제공된 데이터를 기반으로 시각화를 수행합니다.")

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ 데이터 업로드 완료!")

    # 기본 정보 출력
    st.subheader("데이터 미리보기")
    st.dataframe(df.head())

    # 클래스 분포 시각화
    st.subheader("당뇨병 여부 분포 (class 컬럼)")
    class_fig = px.histogram(df, x="class", color="class", 
                             category_orders={"class": [0, 1]},
                             labels={"class": "Diabetes"},
                             title="당뇨병 유무 분포")
    st.plotly_chart(class_fig, use_container_width=True)

    # 사용자 선택 시각화
    st.subheader("개별 특성과 당뇨병 여부 시각화")
    features = df.columns.drop("class")
    selected_feature = st.selectbox("특성을 선택하세요", features)

    fig = px.histogram(df, x=selected_feature, color="class", barmode="group",
                       category_orders={"class": [0, 1]},
                       labels={"class": "Diabetes", selected_feature: selected_feature},
                       title=f"{selected_feature}에 따른 당뇨병 여부 분포")
    st.plotly_chart(fig, use_container_width=True)

    # 상관관계 히트맵
    st.subheader("📈 특성 간 상관관계 히트맵")
    corr = df.corr(numeric_only=True)
    heatmap = ff.create_annotated_heatmap(
        z=corr.values,
        x=list(corr.columns),
        y=list(corr.index),
        colorscale='Viridis',
        showscale=True
    )
    st.plotly_chart(heatmap, use_container_width=True)

else:
    st.info("먼저 CSV 파일을 업로드해주세요.")
