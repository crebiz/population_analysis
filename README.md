# 대한민국 인구 분석 프로젝트

이 프로젝트는 대한민국의 행정구역별 인구 데이터를 분석하고 시각화하는 웹 애플리케이션입니다. 통계청 KOSIS API를 활용하여 최신 인구 데이터를 가져오고, 이를 분석하여 다양한 통계 정보와 시각적 자료를 제공합니다.

## 주요 기능

- **인구 데이터 수집**: 통계청 KOSIS API를 통해 행정구역별 주민등록 인구 데이터를 가져옵니다.
- **기본 통계 분석**: 총 인구, 평균 인구, 최대/최소 인구 지역 등의 기본 통계를 제공합니다.
- **데이터 시각화**: 행정구역별 인구 분포를 그래프로 시각화합니다.
- **임대주택 현황 분석**: 지역별 임대주택 현황 데이터를 분석합니다.
- **다양한 통계 목록 제공**: 인구 관련 다양한 통계 지표를 제공합니다.

## 설치 방법

1. 저장소를 클론합니다:
   ```
   git clone <저장소 URL>
   cd population_analysis
   ```

2. 필요한 패키지를 설치합니다:
   ```
   pip install -r requirements.txt
   ```

3. `config.py` 파일을 생성하고 API 키를 설정합니다:
   ```python
   # config.py
   API_KEY = "your_kosis_api_key"
   POPULATION_URL = "https://kosis.kr/openapi/statisticsData.do"
   ```

## 실행 방법

다음 명령어로 애플리케이션을 실행합니다:

```
streamlit run population_analyzer.py
```

웹 브라우저에서 `http://localhost:8501` 주소로 접속하여 애플리케이션을 사용할 수 있습니다.

## 프로젝트 구조

- `population_analyzer.py`: 메인 애플리케이션 파일로, 인구 데이터를 가져오고 분석하는 기능을 포함합니다.
- `rental_housing_status.py`: 임대주택 현황 데이터를 분석하는 모듈입니다.
- `statistics_list.py`: 다양한 통계 목록을 제공하는 모듈입니다.
- `config.py`: API 키 및 URL 등의 설정 정보를 포함합니다.
- `requirements.txt`: 프로젝트에 필요한 Python 패키지 목록입니다.

## 필요 조건

- Python 3.7 이상
- 통계청 KOSIS API 키 (https://kosis.kr/openapi/application/apie.jsp 에서 신청 가능)

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## Windsurf
- 이 프로젝트는 Windsurf AI를 사용하여 생성되었습니다.
- 이 프로젝트는 Claude 3.5와 Claude 3.7를 사용하여 코딩하였습니다.