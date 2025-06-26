# Default Scenario Generator

AI 기반 투자 시나리오 생성 및 사용자 투자 성향 분석을 위한 통합 플랫폼

## 📋 프로젝트 개요

본 프로젝트는 다음과 같은 기능을 제공합니다:

1. **AI 시나리오 생성**: Google Gemini AI를 활용한 투자 관련 뉴스 시나리오 자동 생성 및 요약
2. **투자 성향 분석**: 사용자의 투자 행동 데이터를 기반으로 한 머신러닝 클러스터링 분석
3. **자동화 파이프라인**: Apache Airflow를 통한 자동화된 데이터 처리 워크플로우
4. **RESTful API**: FastAPI를 통한 고성능 API 서비스 제공
5. **스마트 요약**: LangChain과 LLM을 이용한 시나리오 자동 요약 생성

## 🏗️ 시스템 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Airflow       │    │   FastAPI       │    │   Database      │
│   (Scheduler)   │◄──►│   (API Server)  │◄──►│   PostgreSQL    │
└─────────────────┘    └─────────────────┘    │   MongoDB       │
         │                       │             └─────────────────┘
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Scenario App   │    │   Invest App    │    │   Google AI     │
│  (AI Generator) │◄──►│  (ML Analysis)  │    │   (Gemini 2.5)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                                              ▲
         ▼                                              │
┌─────────────────┐                          ┌─────────────────┐
│   LangChain     │                          │   Summary       │
│   Integration   │─────────────────────────►│   Generator     │
└─────────────────┘                          └─────────────────┘
```

## 📁 프로젝트 구조

```
default-scenario-generator/
├── 📁 dags/                    # Airflow DAG 파일들
│   ├── invest_dag.py          # 투자 데이터 처리 파이프라인
│   └── scenario_generator_dag.py # 시나리오 생성 파이프라인
├── 📁 scenario_app/           # 시나리오 생성 애플리케이션
│   ├── main.py               # 메인 시나리오 생성 로직
│   ├── send_data.py          # 데이터 전송 및 요약 처리
│   ├── summary_generator.py  # LLM 기반 스토리 요약 모듈
│   ├── config.py             # 설정 관리
│   ├── util.py               # 유틸리티 함수들
│   ├── 📁 tools/             # AI 도구들
│   ├── 📁 templates/         # 템플릿 파일들
│   ├── 📁 news_json_files/   # 생성된 뉴스 데이터
│   └── 📁 result_json_files/ # 최종 시나리오 결과
├── 📁 invest/                 # 투자 분석 애플리케이션
│   ├── main_api.py           # FastAPI 서버
│   ├── main_preprocess.py    # 데이터 전처리
│   ├── main_train.py         # 머신러닝 모델 학습
│   ├── 📁 db/                # 데이터베이스 핸들러
│   ├── 📁 models/            # ML 모델 및 전처리
│   ├── 📁 routers/           # API 라우터
│   └── 📁 utils/             # 유틸리티 함수들
├── 📁 logs/                   # 로그 파일들
├── docker-compose.yaml        # Docker Compose 설정
├── Dockerfile                 # Airflow 컨테이너 설정
├── Dockerfile.fastapi         # FastAPI 컨테이너 설정
├── requirements.txt           # 전체 의존성
├── requirements.airflow.txt   # Airflow 의존성
├── requirements.fastapi.txt   # FastAPI 의존성
└── .env.example              # 환경변수 예제
```

## 🛠️ 기술 스택

### Backend
- **Python 3.10+**
- **Apache Airflow 2.8.1** - 워크플로우 오케스트레이션
- **FastAPI** - REST API 서버
- **SQLAlchemy** - ORM
- **Pandas & NumPy** - 데이터 처리
- **Scikit-learn** - 머신러닝

### AI/ML
- **Google Generative AI (Gemini 2.5 Flash)** - 시나리오 생성
- **LangChain** - LLM 통합 및 체인 관리
- **LangChain Google GenAI** - Google AI 통합

### Database
- **PostgreSQL** - 관계형 데이터베이스
- **MongoDB** - 문서형 데이터베이스

### Infrastructure
- **Docker & Docker Compose** - 컨테이너화
- **Uvicorn** - ASGI 서버

## 🚀 빠른 시작

### 1. 사전 요구사항

- Docker Desktop
- Git

### 2. 프로젝트 클론

```bash
git clone <repository-url>
cd default-scenario-generator
```

### 3. 환경 설정

```bash
# 환경변수 파일 생성
cp .env.example .env

# .env 파일을 편집하여 실제 값으로 설정
# - API 키 (GEMINI_API_KEY, OPENAI_API_KEY)
# - 데이터베이스 연결 정보
```

### 4. Docker Compose 실행

```bash
# 모든 서비스 빌드 및 시작
docker-compose up --build

# 백그라운드에서 실행
docker-compose up -d --build
```

### 5. 서비스 접속

- **Airflow Web UI**: http://localhost:8080
  - 사용자명: `admin`
  - 비밀번호: `admin`
- **FastAPI 문서**: http://localhost:8002/docs
- **PostgreSQL**: localhost:5432

## 📊 주요 기능

### 1. 시나리오 생성 및 요약 (AI-Powered Scenario Generation)

```python
# scenario_app/main.py
def main(theme, n):
    """지정된 테마로 n개의 시나리오 생성"""
    # Google Gemini AI를 활용한 뉴스 시나리오 생성
    # 결과를 JSON 파일로 저장

# scenario_app/send_data.py  
async def send_data():
    """생성된 시나리오 전송 및 요약"""
    # LLM을 통한 자동 요약 생성
    # API 서버로 데이터 전송
```

**지원 테마**: `pig`, `food`, `magic`, `moon`

**새로운 기능**:
- ✅ **LLM 기반 자동 요약**: Google Gemini를 이용한 시나리오 요약 생성
- ✅ **Fallback 메커니즘**: LLM 실패 시 기본 요약으로 자동 전환
- ✅ **모듈화된 구조**: `SummaryGenerator` 클래스로 요약 기능 분리

### 2. 투자 성향 분석 (Investment Analysis)

```python
# invest/main_preprocess.py  
def model_preprocess():
    """사용자 투자 데이터 전처리 및 특성 추출"""
    # MongoDB에서 투자 로그 데이터 로드
    # PostgreSQL에서 사용자 정보 로드
    # 특성 엔지니어링 및 전처리
```

**분석 지표**:
- 평균 체류 시간
- 거래 비율 (매수/매도)
- 현금 보유 비율
- 위험 선호도

### 3. 자동화된 파이프라인

#### Scenario Generation Pipeline
```
매일 09:00 실행
├── 1. 기존 파일 정리
├── 2. 테마별 시나리오 생성 (pig → food → magic → moon)
├── 3. LLM 기반 요약 생성
└── 4. 생성된 시나리오 및 요약 전송
```

#### Investment Analysis Pipeline
```
매일 09:00 실행
├── 1. 데이터 전처리 (preprocess_data)
├── 2. 머신러닝 모델링 (modeling_data)
└── 3. 결과 데이터베이스 업데이트 (update_data)
```

### 4. LLM 요약 시스템 (Summary Generation System)

```python
# scenario_app/summary_generator.py
class SummaryGenerator:
    """LLM 기반 스토리 요약 생성기"""
    
    async def generate_story_summary_with_llm(self, story_json: str) -> str:
        """Google Gemini를 이용한 스토리 요약 생성"""
        # LangChain과 Google Generative AI 활용
        # 투자 시나리오에 최적화된 프롬프트 사용
```

**요약 시스템 특징**:
- 🤖 **Google Gemini 2.5 Flash** 모델 사용
- 🔄 **비동기 처리**로 성능 최적화
- 🛡️ **안전한 Fallback**: LLM 실패 시 기본 요약으로 전환
- 📊 **상세 로깅**: 요약 생성 과정 추적

## 🔧 개발 가이드

### 로컬 개발 환경 설정

```bash
# Python 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 개발용 서버 실행 (FastAPI)
uvicorn invest.main_api:app --host 0.0.0.0 --port 8002 --reload
```

### 새로운 시나리오 테마 추가

1. `scenario_app/templates/` 에 새 테마 디렉토리 생성
2. `scenario_generator_dag.py`의 `themes` 리스트에 추가
3. 테마별 프롬프트 템플릿 작성
4. `send_data.py`의 `chapter_id_map`에 새 테마 추가

### 새로운 분석 지표 추가

1. `invest/utils/` 에 새 분석 함수 생성
2. `invest/main_preprocess.py`에 함수 import 및 호출 추가
3. `invest/models/preprocessing/` 에 전처리 로직 추가

### LLM 요약 시스템 커스터마이징

```python
# scenario_app/summary_generator.py 수정 예시
class SummaryGenerator:
    def __init__(self, custom_model="gemini-2.5-flash-preview-05-20"):
        self.model_name = custom_model
        # 커스텀 모델 설정
        
    async def generate_custom_summary(self, story_json: str, prompt_template: str):
        """커스텀 프롬프트로 요약 생성"""
        # 사용자 정의 프롬프트 템플릿 적용
```

## 📚 API 문서

### FastAPI 엔드포인트

```python
# 투자 그래프 데이터 조회
GET /graph/{graph_type}

# 클러스터링 결과 조회  
GET /cluster/results

# 사용자별 투자 성향 조회
GET /user/{user_id}/investment-type
```

자세한 API 문서는 http://localhost:8002/docs 에서 확인할 수 있습니다.

## 🔒 환경변수

`.env` 파일에 다음 변수들을 설정해야 합니다:

```bash
# Airflow 설정
AIRFLOW_UID=50000
AIRFLOW__WEBSERVER__DEFAULT_USER=admin
AIRFLOW__WEBSERVER__DEFAULT_PASSWORD=admin

# AI API 키 (필수)
GEMINI_API_KEY=your_gemini_api_key_here

# LLM 모델 설정
GEMINI_MODEL=gemini-2.5-flash-preview-05-20
DEFAULT_TEMPERATURE=0.9

# API 엔드포인트
API_URL=http://your-api-server/scenarios

# 데이터베이스 설정
DB_HOST=postgres
DB_PORT=5432
DB_USER=airflow
DB_PASSWORD=airflow
DB_NAME=airflow

# MongoDB 설정
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB=your_database
```

## 🐛 트러블슈팅

### 일반적인 문제들

1. **Docker 컨테이너가 시작되지 않는 경우**
   ```bash
   # 로그 확인
   docker-compose logs
   
   # 특정 서비스 로그 확인
   docker-compose logs airflow-webserver
   ```

2. **모듈 import 오류**
   ```bash
   # Python path 확인
   echo $PYTHONPATH
   
   # Docker 내에서 확인
   docker-compose exec airflow-webserver python -c "import sys; print(sys.path)"
   ```

3. **데이터베이스 연결 오류**
   - .env 파일의 DB 설정 확인
   - PostgreSQL 컨테이너 상태 확인: `docker-compose ps`

### 로그 위치

- **Airflow 로그**: `./logs/`
- **시나리오 생성 로그**: `./scenario_app/scenario_generator_log.log`
- **시나리오 전송 로그**: `./scenario_app/scenario_send_log.log`

### LLM 관련 문제

4. **LLM 요약 생성 실패**
   ```bash
   # 환경변수 확인
   echo $GEMINI_API_KEY
   
   # LangChain 패키지 설치 확인
   pip list | grep langchain
   ```

5. **요약 생성 성능 이슈**
   - `DEFAULT_TEMPERATURE` 값 조정 (0.1 ~ 1.0)
   - `GEMINI_MODEL` 변경 고려
   - 비동기 처리 배치 크기 조정

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📈 최근 업데이트 (2025.06.26)

### ✨ 새로운 기능
- **LLM 기반 자동 요약**: Google Gemini 2.5 Flash를 이용한 시나리오 요약 자동 생성
- **모듈화된 요약 시스템**: `SummaryGenerator` 클래스로 요약 기능 분리
- **비동기 처리**: 요약 생성의 성능 최적화
- **Fallback 메커니즘**: LLM 실패 시 기본 요약으로 자동 전환

### 🔧 개선사항
- **코드 구조 개선**: 요약 관련 로직을 별도 모듈로 분리
- **에러 핸들링 강화**: LLM API 호출 실패에 대한 안정적인 처리
- **로깅 시스템 개선**: 요약 생성 과정의 상세한 추적 가능

### 🛠️ 기술적 변경사항
- LangChain Google GenAI 통합
- 비동기 요약 생성 (`async/await` 패턴)
- 환경변수 기반 모델 설정 (`GEMINI_MODEL`, `DEFAULT_TEMPERATURE`)

**마지막 업데이트**: 2025년 6월 26일
