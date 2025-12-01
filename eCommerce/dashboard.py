import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SKU RFM 분석 대시보드")

df = pd.read_csv('output/sku_rfm_segments.csv')

col1, col2, col3 = st.columns(3)
col1.metric("전체 SKU", len(df))
col2.metric("Active 상품", len(df[df['Segment_Name']=='Active High-Performer']))
col3.metric("총 매출", f"${df['Monetary'].sum():,.0f}")

st.plotly_chart(px.pie(df, names='Segment_Name', values='Monetary'))
