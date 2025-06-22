# Default Scenario Generator

투자 시나리오 생성 및 사용자 투자 성향 분석을 위한 통합.

## 📋 프로젝트 개요

본 프로젝트는 다음과 같은 기능을 제공합니다:

1. **시나리오 생성**: AI를 활용한 투자 관련 뉴스 시나리오 자동 생성
2. **투자 성향 분석**: 사용자의 투자 행동 데이터를 기반으로 한 클러스터링 분석
3. **데이터 파이프라인**: Apache Airflow를 통한 자동화된 데이터 처리 워크플로우
4. **API 서비스**: FastAPI를 통한 RESTful API 제공

## 🏗️ 시스템 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Airflow       │    │   FastAPI       │    │   Database      │
│   (Scheduler)   │◄──►│   (API Server)  │◄──►│   PostgreSQL    │
└─────────────────┘    └─────────────────┘    │   MongoDB       │
         │                       │             └─────────────────┘
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│  Scenario App   │    │   Invest App    │
│  (AI Generator) │    │  (ML Analysis)  │
└─────────────────┘    └─────────────────┘
```

## 📁 프로젝트 구조

```
default-scenario-generator/
├── 📁 dags/                    # Airflow DAG 파일들
│   ├── invest_dag.py          # 투자 데이터 처리 파이프라인
│   └── scenario_generator_dag.py # 시나리오 생성 파이프라인
├── 📁 scenario_app/           # 시나리오 생성 애플리케이션
│   ├── main.py               # 메인 시나리오 생성 로직
│   ├── send_data.py          # 데이터 전송 기능
│   ├── config.py             # 설정 관리
│   ├── util.py               # 유틸리티 함수들
│   ├── 📁 tools/             # AI 도구들
│   │   ├── news_tool.py      # 뉴스 생성 도구
│   │   └── result_tool.py    # 결과 생성 도구
│   └── 📁 templates/         # 템플릿 파일들
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
- **Google Generative AI (Gemini)** - 시나리오 생성
- **LangChain** - LLM 통합

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

### 1. 시나리오 생성 (Scenario Generation)

```python
# scenario_app/main.py
def main(theme, n):
    """지정된 테마로 n개의 시나리오 생성"""
    # AI를 활용한 뉴스 시나리오 생성
    # 결과를 JSON 파일로 저장
```

**지원 테마**: `pig`, `food`, `magic`, `moon`

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
└── 3. 생성된 시나리오 전송
```

#### Investment Analysis Pipeline
```
매일 09:00 실행
├── 1. 데이터 전처리 (preprocess_data)
├── 2. 머신러닝 모델링 (modeling_data)
└── 3. 결과 데이터베이스 업데이트 (update_data)
```

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

### 새로운 분석 지표 추가

1. `invest/utils/` 에 새 분석 함수 생성
2. `invest/main_preprocess.py`에 함수 import 및 호출 추가
3. `invest/models/preprocessing/` 에 전처리 로직 추가

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

# AI API 키
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

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

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**마지막 업데이트**: 2025년 6월 22일
