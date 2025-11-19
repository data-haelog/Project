import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(
    page_title="모바일 앱 사용자 분석 대시보드",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .insight-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# 데이터 생성 함수
@st.cache_data
def generate_sample_data():
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-11-12', freq='D')
    
    # 사용자 데이터
    n_users = 50000
    user_data = pd.DataFrame({
        'user_id': range(1, n_users + 1),
        'signup_date': np.random.choice(dates, n_users),
        'user_type': np.random.choice(['Free', 'Premium'], n_users, p=[0.7, 0.3]),
        'platform': np.random.choice(['iOS', 'Android'], n_users, p=[0.45, 0.55]),
        'age_group': np.random.choice(['18-24', '25-34', '35-44', '45+'], n_users, p=[0.3, 0.4, 0.2, 0.1]),
        'country': np.random.choice(['US', 'UK', 'KR', 'JP', 'Other'], n_users, p=[0.3, 0.15, 0.25, 0.15, 0.15])
    })
    
    # 일별 활성 사용자 데이터
    daily_data = []
    for date in dates:
        active_users = int(5000 + 2000 * np.sin(2 * np.pi * (date.dayofyear / 365)) + np.random.normal(0, 500))
        daily_data.append({
            'date': date,
            'dau': max(1000, active_users),
            'sessions': int(active_users * np.random.uniform(2.5, 3.5)),
            'avg_session_duration': np.random.uniform(8, 15),
            'revenue': max(0, np.random.normal(15000, 3000))
        })
    
    daily_df = pd.DataFrame(daily_data)
    daily_df['wau'] = daily_df['dau'].rolling(7, min_periods=1).sum()
    daily_df['mau'] = daily_df['dau'].rolling(30, min_periods=1).sum()
    
    return user_data, daily_df

# 코호트 데이터 생성
@st.cache_data
def generate_cohort_data():
    months = pd.date_range(start='2024-01', end='2024-10', freq='MS')
    cohort_data = []
    
    for i, month in enumerate(months):
        base_retention = 100
        for period in range(7):
            if period == 0:
                retention = 100
            else:
                retention = base_retention * (0.85 ** period) + np.random.uniform(-5, 5)
            
            cohort_data.append({
                'cohort': month.strftime('%Y-%m'),
                'period': f'M{period}',
                'retention': max(0, min(100, retention))
            })
    
    return pd.DataFrame(cohort_data)

# 퍼널 데이터 생성
@st.cache_data
def generate_funnel_data():
    return pd.DataFrame({
        'stage': ['앱 다운로드', '회원가입', '첫 구매', '재구매', '프리미엄 전환'],
        'users': [100000, 65000, 32500, 19500, 6500],
        'conversion': [100, 65, 50, 60, 33.3]
    })

# A/B 테스트 데이터
@st.cache_data
def generate_ab_test_data():
    return pd.DataFrame({
        'group': ['Control (A)', 'Treatment (B)'],
        'users': [10000, 10000],
        'conversions': [1250, 1580],
        'conversion_rate': [12.5, 15.8],
        'avg_revenue': [28.5, 34.2],
        'retention_d7': [35.2, 42.8]
    })

# 데이터 로드
user_data, daily_df = generate_sample_data()
cohort_df = generate_cohort_data()
funnel_df = generate_funnel_data()
ab_test_df = generate_ab_test_data()

# 사이드바
st.sidebar.markdown("##  필터 설정")
st.sidebar.markdown("---")

# 날짜 범위 선택
date_range = st.sidebar.date_input(
    "분석 기간 선택",
    value=(daily_df['date'].min(), daily_df['date'].max()),
    min_value=daily_df['date'].min(),
    max_value=daily_df['date'].max()
)

# 플랫폼 필터
platform_filter = st.sidebar.multiselect(
    "플랫폼",
    options=['전체', 'iOS', 'Android'],
    default=['전체']
)

# 사용자 타입 필터
user_type_filter = st.sidebar.multiselect(
    "사용자 타입",
    options=['전체', 'Free', 'Premium'],
    default=['전체']
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
    ### 💡 대시보드 정보
    - **데이터 기간**: 2024년 1월 ~ 11월
    - **총 사용자**: 50,000명
    - **업데이트**: 실시간
""")

# 메인 헤더
st.markdown('<h1 class="main-header"> 모바일 앱 사용자 분석 대시보드</h1>', unsafe_allow_html=True)
st.markdown("---")

# 탭 생성
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    " Overview", 
    " 리텐션 분석", 
    " 코호트 분석", 
    " 퍼널 분석", 
    " A/B 테스트",
    " 시계열 분석"
])

# TAB 1: Overview
with tab1:
    st.markdown("### 📊 주요 지표 (KPI)")
    
    # 날짜 필터 적용
    if len(date_range) == 2:
        filtered_daily = daily_df[(daily_df['date'] >= pd.Timestamp(date_range[0])) & 
                                   (daily_df['date'] <= pd.Timestamp(date_range[1]))]
    else:
        filtered_daily = daily_df
    
    # KPI 메트릭
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_dau = int(filtered_daily['dau'].mean())
        st.metric("평균 DAU", f"{avg_dau:,}", delta="+12.5%")
    
    with col2:
        avg_wau = int(filtered_daily['wau'].mean() / 7)
        st.metric("평균 WAU", f"{avg_wau:,}", delta="+8.3%")
    
    with col3:
        avg_revenue = filtered_daily['revenue'].mean()
        st.metric("일평균 매출", f"${avg_revenue:,.0f}", delta="+15.2%")
    
    with col4:
        avg_session = filtered_daily['avg_session_duration'].mean()
        st.metric("평균 세션 시간", f"{avg_session:.1f}분", delta="+2.1분")
    
    st.markdown("---")
    
    # 차트 행
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 일별 활성 사용자 추이")
        fig_dau = px.line(filtered_daily, x='date', y='dau', 
                          title='DAU Trend',
                          labels={'date': '날짜', 'dau': 'DAU'})
        fig_dau.update_traces(line_color='#1f77b4', line_width=2)
        fig_dau.update_layout(hovermode='x unified')
        st.plotly_chart(fig_dau, use_container_width=True)
    
    with col2:
        st.markdown("#### 💰 일별 매출 추이")
        fig_revenue = px.area(filtered_daily, x='date', y='revenue',
                              title='Revenue Trend',
                              labels={'date': '날짜', 'revenue': '매출 ($)'})
        fig_revenue.update_traces(line_color='#2ca02c', fillcolor='rgba(44,160,44,0.3)')
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    # 사용자 분포
    st.markdown("---")
    st.markdown("#### 👥 사용자 분포")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        platform_dist = user_data['platform'].value_counts()
        fig_platform = px.pie(values=platform_dist.values, names=platform_dist.index,
                              title='플랫폼별 분포',
                              color_discrete_sequence=['#ff7f0e', '#2ca02c'])
        st.plotly_chart(fig_platform, use_container_width=True)
    
    with col2:
        user_type_dist = user_data['user_type'].value_counts()
        fig_user_type = px.pie(values=user_type_dist.values, names=user_type_dist.index,
                               title='사용자 타입 분포',
                               color_discrete_sequence=['#9467bd', '#8c564b'])
        st.plotly_chart(fig_user_type, use_container_width=True)
    
    with col3:
        age_dist = user_data['age_group'].value_counts()
        fig_age = px.bar(x=age_dist.index, y=age_dist.values,
                        title='연령대별 분포',
                        labels={'x': '연령대', 'y': '사용자 수'},
                        color_discrete_sequence=['#17becf'])
        st.plotly_chart(fig_age, use_container_width=True)

# TAB 2: 리텐션 분석
with tab2:
    st.markdown("### 📊 리텐션 분석")
    
    # 리텐션 지표
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("D1 Retention", "65.3%", delta="+2.1%")
    with col2:
        st.metric("D7 Retention", "38.7%", delta="+1.5%")
    with col3:
        st.metric("D30 Retention", "22.4%", delta="+0.8%")
    
    st.markdown("---")
    
    # 리텐션 곡선
    retention_data = pd.DataFrame({
        'day': ['D0', 'D1', 'D3', 'D7', 'D14', 'D30', 'D60', 'D90'],
        'retention': [100, 65.3, 52.1, 38.7, 28.5, 22.4, 18.2, 15.7],
        'users': [10000, 6530, 5210, 3870, 2850, 2240, 1820, 1570]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_retention = go.Figure()
        fig_retention.add_trace(go.Scatter(
            x=retention_data['day'], 
            y=retention_data['retention'],
            mode='lines+markers',
            name='Retention Rate',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=10)
        ))
        fig_retention.update_layout(
            title='리텐션 곡선',
            xaxis_title='기간',
            yaxis_title='리텐션율 (%)',
            hovermode='x unified'
        )
        st.plotly_chart(fig_retention, use_container_width=True)
    
    with col2:
        fig_users = px.bar(retention_data, x='day', y='users',
                          title='기간별 잔존 사용자 수',
                          labels={'day': '기간', 'users': '사용자 수'},
                          color='users',
                          color_continuous_scale='Blues')
        st.plotly_chart(fig_users, use_container_width=True)
    
    # 인사이트
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown("""
        **💡 주요 인사이트:**
        - D1 리텐션 65.3%로 업계 평균(40-50%) 대비 우수
        - D7에서 급격한 이탈 발생 → 온보딩 개선 필요
        - D30 이후 안정화 → 코어 유저층 형성
        - **권장 액션**: 7일차 리인게이지먼트 캠페인 실행
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 3: 코호트 분석
with tab3:
    st.markdown("### 🔥 코호트 분석")
    
    # 코호트 히트맵 데이터 준비
    cohort_pivot = cohort_df.pivot(index='cohort', columns='period', values='retention')
    
    # 히트맵
    fig_cohort = go.Figure(data=go.Heatmap(
        z=cohort_pivot.values,
        x=cohort_pivot.columns,
        y=cohort_pivot.index,
        colorscale='RdYlGn',
        text=np.round(cohort_pivot.values, 1),
        texttemplate='%{text}%',
        textfont={"size": 10},
        colorbar=dict(title="Retention %")
    ))
    
    fig_cohort.update_layout(
        title='월별 코호트 리텐션 히트맵',
        xaxis_title='가입 후 경과 개월',
        yaxis_title='가입 월',
        height=500
    )
    
    st.plotly_chart(fig_cohort, use_container_width=True)
    
    # 코호트별 비교 그래프
    st.markdown("---")
    st.markdown("#### 📊 코호트별 리텐션 곡선")
    
    selected_cohorts = st.multiselect(
        "비교할 코호트 선택",
        options=cohort_df['cohort'].unique(),
        default=cohort_df['cohort'].unique()[:3]
    )
    
    fig_cohort_lines = px.line(
        cohort_df[cohort_df['cohort'].isin(selected_cohorts)],
        x='period', y='retention', color='cohort',
        title='선택된 코호트 리텐션 비교',
        labels={'period': '기간', 'retention': '리텐션율 (%)', 'cohort': '코호트'}
    )
    st.plotly_chart(fig_cohort_lines, use_container_width=True)
    
    # 인사이트
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown("""
        **💡 코호트 분석 인사이트:**
        - 최근 코호트(2024-09, 10)의 초기 리텐션이 이전 대비 12% 향상
        - M3에서 모든 코호트 평균 65% 리텐션 유지
        - 시즌성 영향: 여름(6-8월) 코호트가 상대적으로 낮은 리텐션
        - **권장 액션**: 성공적인 최근 온보딩 전략을 이전 사용자에게도 적용
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 4: 퍼널 분석
with tab4:
    st.markdown("### 🎯 전환 퍼널 분석")
    
    # 퍼널 차트
    fig_funnel = go.Figure(go.Funnel(
        y=funnel_df['stage'],
        x=funnel_df['users'],
        textposition="inside",
        textinfo="value+percent previous",
        marker=dict(
            color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        )
    ))
    
    fig_funnel.update_layout(
        title='사용자 전환 퍼널',
        height=500
    )
    
    st.plotly_chart(fig_funnel, use_container_width=True)
    
    # 상세 전환율 테이블
    st.markdown("---")
    st.markdown("#### 📋 단계별 전환율 상세")
    
    funnel_df['drop_off'] = 100 - funnel_df['conversion']
    funnel_df['drop_off_users'] = funnel_df['users'].diff().abs().fillna(0).astype(int)
    
    st.dataframe(
        funnel_df[['stage', 'users', 'conversion', 'drop_off', 'drop_off_users']].style.format({
            'users': '{:,.0f}',
            'conversion': '{:.1f}%',
            'drop_off': '{:.1f}%',
            'drop_off_users': '{:,.0f}'
        }),
        use_container_width=True,
        hide_index=True
    )
    
    # 전환율 개선 시뮬레이터
    st.markdown("---")
    st.markdown("#### 🔮 전환율 개선 시뮬레이션")
    
    col1, col2 = st.columns(2)
    
    with col1:
        signup_improve = st.slider("회원가입 전환율 개선 (%p)", 0, 20, 5)
        purchase_improve = st.slider("첫 구매 전환율 개선 (%p)", 0, 20, 5)
    
    with col2:
        new_signup = 100000 * (65 + signup_improve) / 100
        new_purchase = new_signup * (50 + purchase_improve) / 100
        additional_revenue = (new_purchase - 32500) * 50  # 건당 평균 $50
        
        st.metric("예상 신규 구매자", f"{int(new_purchase - 32500):,}명")
        st.metric("예상 추가 매출", f"${additional_revenue:,.0f}")
    
    # 인사이트
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown("""
        **💡 퍼널 분석 인사이트:**
        - 회원가입 단계에서 35% 이탈 → 간소화된 가입 프로세스 필요
        - 첫 구매 전환율 50%는 양호하나 개선 여지 존재
        - 재구매율 60%는 우수 → 초기 경험이 만족스러움을 의미
        - 프리미엄 전환율 33.3% → 업계 평균(5-10%) 대비 매우 높음
        - **권장 액션**: 
          1. 소셜 로그인 추가로 가입 마찰 감소
          2. 신규 사용자 대상 첫 구매 인센티브 강화
          3. 재구매 고객 대상 프리미엄 혜택 강조
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 5: A/B 테스트
with tab5:
    st.markdown("### 🧪 A/B 테스트 결과")
    
    st.info("**테스트 내용**: 새로운 온보딩 플로우 (Treatment B) vs 기존 플로우 (Control A)")
    
    # 주요 지표 비교
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "전환율 개선", 
            "+3.3%p",
            delta=f"+26.4% 상대적 개선"
        )
    
    with col2:
        st.metric(
            "평균 매출 증가",
            "+$5.7",
            delta="+20% 증가"
        )
    
    with col3:
        st.metric(
            "D7 리텐션 개선",
            "+7.6%p",
            delta="+21.6% 개선"
        )
    
    st.markdown("---")
    
    # 그룹 비교 차트
    col1, col2 = st.columns(2)
    
    with col1:
        fig_ab_conv = px.bar(
            ab_test_df,
            x='group',
            y='conversion_rate',
            title='전환율 비교',
            labels={'group': '그룹', 'conversion_rate': '전환율 (%)'},
            color='group',
            color_discrete_map={'Control (A)': '#ff7f0e', 'Treatment (B)': '#2ca02c'},
            text='conversion_rate'
        )
        fig_ab_conv.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig_ab_conv, use_container_width=True)
    
    with col2:
        fig_ab_rev = px.bar(
            ab_test_df,
            x='group',
            y='avg_revenue',
            title='평균 매출 비교',
            labels={'group': '그룹', 'avg_revenue': '평균 매출 ($)'},
            color='group',
            color_discrete_map={'Control (A)': '#ff7f0e', 'Treatment (B)': '#2ca02c'},
            text='avg_revenue'
        )
        fig_ab_rev.update_traces(texttemplate='$%{text:.1f}', textposition='outside')
        st.plotly_chart(fig_ab_rev, use_container_width=True)
    
    # 통계적 유의성
    st.markdown("---")
    st.markdown("#### 📊 통계적 유의성 검정")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            **전환율**
            - p-value: 0.0012
            - 신뢰구간: 95%
            - ✅ 통계적으로 유의미
        """)
    
    with col2:
        st.markdown("""
            **평균 매출**
            - p-value: 0.0089
            - 신뢰구간: 95%
            - ✅ 통계적으로 유의미
        """)
    
    with col3:
        st.markdown("""
            **D7 리텐션**
            - p-value: 0.0003
            - 신뢰구간: 99%
            - ✅ 매우 유의미
        """)
    
    # ROI 계산
    st.markdown("---")
    st.markdown("#### 💰 예상 ROI")
    
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown("""
        **Treatment B 전면 적용 시 예상 효과:**
        - 월간 추가 전환: 약 1,650명
        - 월간 추가 매출: 약 $285,000
        - 연간 추가 매출: 약 $3,420,000
        - 개발 비용 대비 ROI: **약 342%**
        
        **권장 사항**: ✅ Treatment B를 전체 사용자에게 즉시 배포
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 6: 시계열 분석
with tab6:
    st.markdown("### 📈 시계열 분석")
    
    # 지표 선택
    metric_option = st.selectbox(
        "분석할 지표 선택",
        ["DAU", "세션 수", "평균 세션 시간", "매출"]
    )
    
    # 이동평균 기간
    ma_period = st.slider("이동평균 기간 (일)", 1, 30, 7)
    
    # 지표별 차트
    if metric_option == "DAU":
        filtered_daily['ma'] = filtered_daily['dau'].rolling(ma_period).mean()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_daily['date'], y=filtered_daily['dau'],
                                 mode='lines', name='DAU', line=dict(color='lightgray')))
        fig.add_trace(go.Scatter(x=filtered_daily['date'], y=filtered_daily['ma'],
                                 mode='lines', name=f'{ma_period}일 이동평균',
                                 line=dict(color='#1f77b4', width=3)))
        fig.update_layout(title='DAU 추이', xaxis_title='날짜', yaxis_title='사용자 수')
        
    elif metric_option == "세션 수":
        filtered_daily['ma'] = filtered_daily['sessions'].rolling(ma_period).mean()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_daily['date'], y=filtered_daily['sessions'],
                                 mode='lines', name='세션 수', line=dict(color='lightgray')))
        fig.add_trace(go.Scatter(x=filtered_daily['date'], y=filtered_daily['ma'],
                                 mode='lines', name=f'{ma_period}일 이동평균',
                                 line=dict(color='#ff7f0e', width=3)))
        fig.update_layout(title='세션 수 추이', xaxis_title='날짜', yaxis_title='세션 수')
        
    elif metric_option == "평균 세션 시간":
        filtered_daily['ma'] = filtered_daily['avg_session_duration'].rolling(ma_period).mean()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_daily['date'], y=filtered_daily['avg_session_duration'],
                                 mode='lines', name='세션 시간', line=dict(color='lightgray')))
        fig.add_trace(go.Scatter(x=filtered_daily['date'], y=filtered_daily['ma'],
                                 mode='lines', name=f'{ma_period}일 이동평균',
                                 line=dict(color='#2ca02c', width=3)))
        fig.update_layout(title='평균 세션 시간 추이', xaxis_title='날짜', yaxis_title='시간 (분)')
        
    else:  # 매출
        filtered_daily['ma'] = filtered_daily['revenue'].rolling(ma_period).mean()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_daily['date'], y=filtered_daily['revenue'],
                                 mode='lines', name='매출', line=dict(color='lightgray')))
        fig.add_trace(go.Scatter(x=filtered_daily['date'], y=filtered_daily['ma'],
                                 mode='lines', name=f'{ma_period}일 이동평균',
                                 line=dict(color='#d62728', width=3)))
        fig.update_layout(title='매출 추이', xaxis_title='날짜', yaxis_title='매출 ($)')
    
    fig.update_layout(hovermode='x unified', height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # 요일별 패턴 분석
    st.markdown("---")
    st.markdown("#### 📅 요일별 패턴 분석")
    
    filtered_daily['weekday'] = filtered_daily['date'].dt.day_name()
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_stats = filtered_daily.groupby('weekday').agg({
        'dau': 'mean',
        'sessions': 'mean',
        'revenue': 'mean'
    }).reindex(weekday_order)
    
    weekday_stats_kr = weekday_stats.copy()
    weekday_stats_kr.index = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_weekday_dau = px.bar(
            x=weekday_stats_kr.index,
            y=weekday_stats_kr['dau'],
            title='요일별 평균 DAU',
            labels={'x': '요일', 'y': 'DAU'},
            color=weekday_stats_kr['dau'],
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_weekday_dau, use_container_width=True)
    
    with col2:
        fig_weekday_revenue = px.bar(
            x=weekday_stats_kr.index,
            y=weekday_stats_kr['revenue'],
            title='요일별 평균 매출',
            labels={'x': '요일', 'y': '매출 ($)'},
            color=weekday_stats_kr['revenue'],
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_weekday_revenue, use_container_width=True)
    
    # 월별 성장률
    st.markdown("---")
    st.markdown("#### 📊 월별 성장률 분석")
    
    filtered_daily['year_month'] = filtered_daily['date'].dt.to_period('M').astype(str)
    monthly_stats = filtered_daily.groupby('year_month').agg({
        'dau': 'mean',
        'revenue': 'sum'
    }).reset_index()
    
    monthly_stats['dau_growth'] = monthly_stats['dau'].pct_change() * 100
    monthly_stats['revenue_growth'] = monthly_stats['revenue'].pct_change() * 100
    
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Bar(
        x=monthly_stats['year_month'],
        y=monthly_stats['dau_growth'],
        name='DAU 성장률 (%)',
        marker_color='#1f77b4'
    ))
    fig_growth.add_trace(go.Bar(
        x=monthly_stats['year_month'],
        y=monthly_stats['revenue_growth'],
        name='매출 성장률 (%)',
        marker_color='#2ca02c'
    ))
    fig_growth.update_layout(
        title='월별 성장률 (전월 대비)',
        xaxis_title='월',
        yaxis_title='성장률 (%)',
        barmode='group'
    )
    st.plotly_chart(fig_growth, use_container_width=True)
    
    # 시계열 인사이트
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown("""
        **💡 시계열 분석 인사이트:**
        - **계절성 패턴**: 주말(토,일) DAU가 평일 대비 평균 18% 높음
        - **매출 패턴**: 금요일 매출이 가장 높음 (평균 $18,500)
        - **성장 추세**: 최근 3개월 평균 DAU 성장률 +8.3%
        - **이상 징후**: 9월 중순 급격한 DAU 하락 → 서버 장애 영향
        - **권장 액션**: 
          1. 주말 특화 이벤트로 높은 트래픽 활용
          2. 금요일 프로모션 강화로 매출 극대화
          3. 성장 모멘텀 유지를 위한 마케팅 투자 지속
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; padding: 2rem;'>
        <p>📱 <b>Mobile App Analytics Dashboard</b></p>
        <p>Data Range: 2024-01-01 ~ 2024-11-12 | Last Updated: 2024-11-12</p>
        <p>Made with ❤️ using Streamlit</p>
    </div>
""", unsafe_allow_html=True)