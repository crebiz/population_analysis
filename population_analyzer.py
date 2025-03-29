import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.font_manager as fm
import json

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우의 기본 한글 폰트
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

def fetch_population_data():
    """
    통계청 KOSIS API를 통해 행정구역(시군구)별 주민등록세대수를 가져옵니다.
    """
    API_KEY = 'NDcxYmM3MzZiNDE3M2FjNjU1YmI4M2VhNDJjMWEyMGY='
    BASE_URL = 'https://kosis.kr/openapi/Param/statisticsParameterData.do'
# &itmId=T1+&objL1=ALL&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&newEstPrdCnt=3&orgId=101&tblId=DT_1B040B3
    params = {
        'method': 'getList',
        'apiKey': API_KEY,
        'itmId': 'T1',
        'objL1': 'ALL',  # 모든 시도
        'objL2': '', 
        'objL3': '', 
        'objL4': '', 
        'objL5': '', 
        'objL6': '', 
        'objL7': '', 
        'objL8': '', 
        'format': 'json',
        'jsonVD': 'Y',
        'prdSe': 'M',  # 월별
        'newEstPrdCnt': '3',
        'orgId': '101',  # 통계청
        'tblId': 'DT_1B040B3',  # 주민등록 인구현황
    }
    
    try:
        st.info("KOSIS API 호출 중...")
        response = requests.get(BASE_URL, params=params)
        
        # API 응답 로깅
        st.write("요청 URL:", response.url)
        st.write("응답 상태 코드:", response.status_code)
        
        try:
            data = response.json()
            st.write("응답 데이터 구조:", type(data))
            if isinstance(data, dict) and 'err' in data:
                raise ValueError(f"API 오류: {data['errMsg']} (에러 코드: {data['err']})")
            
            # 데이터가 리스트가 아닌 경우 처리
            if not isinstance(data, list):
                st.error("예상치 못한 응답 형식입니다.")
                raise ValueError(f"예상치 못한 응답 형식: {type(data)}")
            
            # 빈 데이터 처리
            if not data:
                st.warning("API에서 반환된 데이터가 없습니다.")
                raise ValueError("데이터가 비어있습니다.")
            
            # 데이터 구조 확인
            st.write("첫 번째 데이터 항목:", data[0] if data else "데이터 없음")
            
            # 데이터프레임 변환
            population_data = {}
            for item in data:
                if all(key in item for key in ['C1_NM', 'DT']):
                    region = item['C1_NM'].strip()
                    try:
                        population = int(float(item['DT'].replace(',', '')))
                        if population > 0:
                            population_data[region] = population
                    except (ValueError, TypeError) as e:
                        st.warning(f"데이터 변환 오류 ({region}): {str(e)}")
                        continue
            
            if not population_data:
                raise ValueError("유효한 인구 데이터를 찾을 수 없습니다.")
            
            df = pd.DataFrame(list(population_data.items()), columns=['행정구역', '인구수'])
            st.success("데이터 로딩 완료")
            return df
            
        except json.JSONDecodeError as e:
            st.error("JSON 파싱 오류")
            st.write("원본 응답:", response.text[:500])  # 처음 500자만 표시
            raise ValueError(f"JSON 파싱 오류: {str(e)}")
            
    except requests.exceptions.RequestException as e:
        st.error(f"API 요청 실패: {str(e)}")
        raise
    except Exception as e:
        st.error(f"처리 중 오류 발생: {str(e)}")
        # 오류 발생 시 샘플 데이터 반환
        sample_data = {
            '서울특별시': 9411138,
            '부산광역시': 3359527,
            '대구광역시': 2418346,
            '인천광역시': 2948542,
            '광주광역시': 1450062,
            '대전광역시': 1463882,
            '울산광역시': 1136017,
            '세종특별자치시': 371895,
            '경기도': 13807158,
            '강원도': 1542840,
            '충청북도': 1600007,
            '충청남도': 2121029,
            '전라북도': 1804104,
            '전라남도': 1851549,
            '경상북도': 2639422,
            '경상남도': 3340216,
            '제주특별자치도': 697578
        }
        return pd.DataFrame(list(sample_data.items()), columns=['행정구역', '인구수'])

def analyze_population(df):
    """인구 데이터를 분석하고 기본적인 통계를 계산합니다."""
    try:
        # 인구수를 숫자형으로 변환
        df['인구수'] = pd.to_numeric(df['인구수'], errors='coerce')
        
        # NaN 값이 있는 행 제거
        df = df.dropna(subset=['인구수'])
        
        if len(df) == 0:
            raise ValueError("유효한 데이터가 없습니다.")
        
        stats = {
            '총 인구': int(df['인구수'].sum()),
            '평균 인구': int(df['인구수'].mean()),
            '최대 인구 지역': df[df['행정구역'] != '전국'].loc[df[df['행정구역'] != '전국']['인구수'].idxmax(), '행정구역'],
            '최소 인구 지역': df[df['행정구역'] != '전국'].loc[df[df['행정구역'] != '전국']['인구수'].idxmin(), '행정구역']
        }
        return stats
    except Exception as e:
        st.error(f"통계 분석 중 오류가 발생했습니다: {str(e)}")
        return {
            '총 인구': 0,
            '평균 인구': 0,
            '최대 인구 지역': '데이터 없음',
            '최소 인구 지역': '데이터 없음'
        }

def create_visualization(df):
    """인구 데이터를 시각화합니다."""
    try:
        # 인구수를 숫자형으로 변환
        df['인구수'] = pd.to_numeric(df['인구수'], errors='coerce')
        
        # NaN 값이 있는 행 제거
        df = df.dropna(subset=['인구수'])
        
        if len(df) == 0:
            st.error("시각화할 데이터가 없습니다.")
            return None
            
        plt.figure(figsize=(15, 8))
        sns.barplot(data=df, x='행정구역', y='인구수')
        plt.xticks(rotation=45, ha='right')
        plt.title('대한민국 행정구역별 인구 분포')
        plt.tight_layout()
        return plt
    except Exception as e:
        st.error(f"시각화 중 오류가 발생했습니다: {str(e)}")
        return None

def main():
    st.title('대한민국 행정구역별 인구 분석')
    
    # 데이터 가져오기
    df = fetch_population_data()
    
    # 기본 통계 표시
    stats = analyze_population(df)
    st.header('기본 통계')
    for key, value in stats.items():
        if '인구' in key and '지역' not in key:
            st.metric(key, f'{value:,} 명')
        else:
            st.metric(key, value)
    
    # 데이터 테이블 표시
    st.header('행정구역별 인구 데이터')
    st.dataframe(df.style.format({'인구수': '{:,}'}))
    
    # 시각화
    st.header('인구 분포 그래프')
    fig = create_visualization(df)
    st.pyplot(fig)

if __name__ == '__main__':
    main()
