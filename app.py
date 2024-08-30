import streamlit as st
import pandas as pd
import plotly.express as px
import io

def main():
    st.title('성적 데이터 시각화 대시보드')

    # 파일 업로더
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")
    
    if uploaded_file is not None:
        # 데이터 로드
        df = load_data(uploaded_file)
        
        if df is not None:
            # 사이드바: 시각화 옵션 선택
            st.sidebar.header('시각화 옵션')
            chart_type = st.sidebar.selectbox('차트 유형', ['막대 그래프', '선 그래프'])
            
            # 숫자형 컬럼만 선택 가능하도록 필터링
            numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
            metric = st.sidebar.selectbox('보고 싶은 지표', numeric_columns)

            # 메인 차트
            st.header(f'{metric} 기준 과목별 분포')
            
            if chart_type == '막대 그래프':
                fig = px.bar(df, x=df.index, y=metric, title=f'과목별 {metric} 분포')
            else:  # 선 그래프
                fig = px.line(df, x=df.index, y=metric, title=f'과목별 {metric} 분포')
            
            st.plotly_chart(fig)

            # 데이터 테이블 표시
            st.header('전체 데이터')
            st.dataframe(df)

            # 통계 요약
            st.header('통계 요약')
            st.write(df.describe())
        else:
            st.error('CSV 파일을 읽는 데 문제가 발생했습니다. 파일 형식을 확인해 주세요.')
    else:
        st.info('위의 파일 업로더를 사용하여 CSV 파일을 업로드해 주세요.')

@st.cache_data
def load_data(file):
    try:
        # CSV 파일 읽기
        df = pd.read_csv(file, encoding='utf-8')
        
        # '과목' 열을 인덱스로 설정
        if '과목' in df.columns:
            df.set_index('과목', inplace=True)
        
        # 숫자형 데이터만 추출
        df = df.apply(pd.to_numeric, errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return None

if __name__ == '__main__':
    main()
