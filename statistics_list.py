import requests
import pandas as pd
import streamlit as st
import json

def fetch_statistics_list():
    """
    KOSIS API를 통해 통계목록을 조회합니다.
    """
    API_KEY = 'NDcxYmM3MzZiNDE3M2FjNjU1YmI4M2VhNDJjMWEyMGY='  # API 키는 실제 발급받은 키로 변경해야 합니다
    BASE_URL = 'https://kosis.kr/openapi/statisticsList.do'
    
    params = {
        'method': 'getList',
        'apiKey': API_KEY,
        'vwCd': 'MT_ZTITLE',
        'parentListId' : 'I1_6',
        'format': 'json',
        'jsonVD': 'Y'
    }
    
    try:
        info_placeholder = st.empty()
        info_placeholder.info("KOSIS 통계목록 조회 중...")
        response = requests.get(BASE_URL, params=params)
        
        # API 응답 상태 확인
        st.write("응답 상태 코드:", response.status_code)
        
        if response.status_code == 200:
            # JSON 데이터 파싱
            data = response.json()
            
            # 데이터프레임으로 변환
            df = pd.DataFrame(data)
            
            # 주요 컬럼 선택 및 이름 변경
            if not df.empty:
                selected_columns = {
                    'VW_CD': '서비스뷰',
                    'LIST_ID': '목록ID',
                    'TBL_NM': '목록명',
                    'ORG_ID': '기관코드',
                    'TBL_ID': '통계표ID',
                    'STAT_ID': '통계조사ID',
                    'SEND_DE': '최종갱신일',
                    'REC_TBL_SE': '추천통계표여부'
                }
                
                # 존재하는 컬럼만 선택
                existing_columns = [col for col in selected_columns.keys() if col in df.columns]
                df_selected = df[existing_columns].copy()
                
                # 컬럼명 한글로 변경
                df_selected.columns = [selected_columns[col] for col in existing_columns]
                
                info_placeholder.info("KOSIS 통계목록 조회 완료")
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

def main():
    st.set_page_config(layout="wide")
    st.title("KOSIS 통계목록 조회")
    
    if st.button("통계목록 조회"):
        df = fetch_statistics_list()
        if not df.empty:
            st.write("### 조회된 통계목록")
            st.dataframe(df, use_container_width=True, height=600)
            
            # CSV 다운로드 버튼
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="CSV 파일 다운로드",
                data=csv,
                file_name="kosis_statistics_list.csv",
                mime="text/csv"
            )
        else:
            st.warning("조회할 통계목록이 없습니다.")

if __name__ == "__main__":
    main()
