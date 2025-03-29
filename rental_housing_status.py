import pandas as pd
import requests
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from config import API_KEY, RENTAL_HOUSING_URL

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def fetch_rental_housing_data():
    """
    KOSIS API를 통해 민간임대주택 재고현황 데이터를 조회합니다.
    """
    params = {
        'method': 'getList',
        'apiKey': API_KEY,
        'format': 'json',
        'itmId': '13103134365T1+13103134365T4',
        'objL1': '13102134365A.0001+13102134365A.0002',
        'objL2': '13102134365B.0001+13102134365B.0002+13102134365B.0003+13102134365B.0004+13102134365B.0005+13102134365B.0006',
        'objL3': '',
        'objL4': '',
        'objL5': '',
        'objL6': '',
        'objL7': '',
        'objL8': '',
        'jsonVD': 'Y',
        'prdSe': 'Y',
        'newEstPrdCnt': '3',
        'orgId': '116',
        'tblId': 'DT_MLTM_6828'
    }

    try:
        info_placeholder = st.empty()
        info_placeholder.info("민간임대주택 재고현황 데이터 조회 중...")
        response = requests.get(RENTAL_HOUSING_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(data)
            
            if isinstance(data, list) and len(data) > 0:
                df = pd.DataFrame(data)
                
                # 데이터 전처리
                if 'PRD_DE' in df.columns:
                    df['년도'] = df['PRD_DE']
                if 'C1_NM' in df.columns:  # 지역
                    df['지역'] = df['C1_NM']
                if 'C2_NM' in df.columns:  # 지역명
                    df['구분'] = df['C2_NM']
                if 'DT' in df.columns:  # 값
                    df['값'] = df['DT']
                if 'PRD_SE' in df.columns:  # 기관코드
                    df['기관코드'] = df['PRD_SE']
                
                # 필요한 컬럼만 선택
                columns_to_show = ['기관코드', '통계표ID', '통계표명', '지역', '구분', '년도', '값']
                df_selected = df[[col for col in columns_to_show if col in df.columns]]
                
                # 값 컬럼을 숫자형으로 변환
                if '값' in df_selected.columns:
                    df_selected['값'] = pd.to_numeric(df_selected['값'], errors='coerce')
                
                info_placeholder.info("민간임대주택 재고현황 데이터 조회 완료")
                return df_selected
            
            else:
                st.error("조회된 데이터가 없습니다.")
                return pd.DataFrame()
        else:
            st.error(f"API 호출 실패: {response.status_code}")
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"오류 발생: {str(e)}")
        return pd.DataFrame()

def create_visualization(df):
    """
    민간임대주택 재고현황 데이터를 시각화합니다.
    """
    if not df.empty:
        # 최신 년도 데이터로 지역별 현황 시각화
        latest_year = df['년도'].max()
        latest_data = df[df['년도'] == latest_year]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=latest_data, x='지역', y='값', ax=ax)
        plt.xticks(rotation=45, ha='right')
        plt.title(f'{latest_year}년 지역별 민간임대주택 현황')
        plt.xlabel('지역')
        plt.ylabel('주택 수')
        
        return fig
    return None

def main():
    st.set_page_config(layout="wide", page_title="민간임대주택 재고현황")
    
    st.title("민간임대주택 재고현황 분석")
    
    if st.button("데이터 조회"):
        df = fetch_rental_housing_data()
        
        if not df.empty:
            # 데이터 테이블 표시
            st.write("### 민간임대주택 재고현황 데이터")
            st.dataframe(df, use_container_width=True, height=400)
            
            # 시각화
            st.write("### 지역별 현황 시각화")
            fig = create_visualization(df)
            if fig:
                st.pyplot(fig)
            
            # CSV 다운로드 버튼
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="CSV 파일 다운로드",
                data=csv,
                file_name="rental_housing_status.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
