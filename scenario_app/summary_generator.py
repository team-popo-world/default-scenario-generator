"""
LLM 기반 스토리 요약 모듈
"""
import os
import json
import logging
from typing import Optional
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.schema import HumanMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

# 설정값
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-preview-05-20")
DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.9"))

# 로거 설정
logger = logging.getLogger(__name__)

class SummaryGenerator:
    """LLM 기반 스토리 요약 생성기"""
    
    def __init__(self):
        self.llm_model = None
        self.is_initialized = False
        
    def initialize_llm(self) -> bool:
        """LLM 모델을 초기화합니다."""
        if not LANGCHAIN_AVAILABLE:
            logger.warning("LangChain 패키지가 설치되지 않았습니다.")
            return False
            
        try:
            if GEMINI_API_KEY:
                self.llm_model = ChatGoogleGenerativeAI(
                    model=GEMINI_MODEL,
                    google_api_key=GEMINI_API_KEY,
                    temperature=DEFAULT_TEMPERATURE
                )
                self.is_initialized = True
                logger.info("LLM 모델 초기화 성공")
                return True
            else:
                logger.warning("GEMINI_API_KEY가 설정되지 않았습니다.")
                return False
        except Exception as e:
            logger.error(f"LLM 모델 초기화 실패: {e}")
            return False
    
    def generate_basic_summary(self, story_json: str) -> str:
        """
        스토리 JSON에서 기본적인 요약을 생성합니다. (LLM이 없을 때 대체용)
        
        Args:
            story_json (str): 스토리 JSON 문자열
            
        Returns:
            str: 기본 요약
        """
        try:
            story_data = json.loads(story_json)
            if isinstance(story_data, list) and story_data:
                scenario_count = len(story_data)
                
                # 첫 번째 턴에서 종목 정보 추출
                if story_data and 'stocks' in story_data[0] and story_data[0]['stocks']:
                    stocks = story_data[0]['stocks']
                    stock_count = len(stocks)
                    
                    # 위험도별 분석
                    risk_levels = [stock.get('risk_level', '') for stock in stocks]
                    high_risk = len([r for r in risk_levels if '고위험' in r])
                    medium_risk = len([r for r in risk_levels if '중위험' in r])
                    low_risk = len([r for r in risk_levels if '저위험' in r])
                    
                    return f"총 {scenario_count}개 턴으로 구성된 투자 시나리오입니다. {stock_count}개 종목(고위험:{high_risk}, 중위험:{medium_risk}, 저위험:{low_risk})의 등락을 통해 투자 전략을 학습할 수 있습니다."
                else:
                    return f"총 {scenario_count}개 구간으로 구성된 투자 시나리오로, 다양한 종목의 등락을 통해 투자 전략을 학습할 수 있습니다."
            else:
                return "투자 시나리오를 통해 시장 상황에 따른 종목별 등락 패턴을 학습할 수 있습니다."
        except Exception as e:
            logger.error(f"기본 요약 생성 중 오류: {e}")
            return "투자 교육을 위한 시나리오입니다."
    
    def generate_llm_summary(self, story_json: str) -> str:
        """
        LLM을 활용하여 스토리의 흐름과 종목별 등락을 자연스럽게 요약합니다.
        
        Args:
            story_json (str): 스토리 JSON 문자열
            
        Returns:
            str: LLM이 생성한 스토리 요약
        """
        if not self.is_initialized or not self.llm_model:
            logger.warning("LLM 모델이 초기화되지 않았습니다.")
            return self.generate_basic_summary(story_json)
        
        # 스토리 요약을 위한 프롬프트 생성
        summary_prompt = self._create_summary_prompt(story_json)
        
        try:
            # LLM을 통해 요약 생성 (동기)
            try:
                response = self.llm_model.invoke([HumanMessage(content=summary_prompt)])
                summary_result = response.content
            except Exception as sync_error:
                logger.error(f"동기 방식 요약 생성 실패: {sync_error}")
                summary_result = None
            
            if not summary_result:
                logger.warning("LLM 요약 생성 실패, 기본 요약으로 대체합니다.")
                return self.generate_basic_summary(story_json)
            
            # 요약 텍스트 정리 및 길이 제한
            processed_summary = self._process_summary_text(summary_result)
            
            return processed_summary if processed_summary else self.generate_basic_summary(story_json)
            
        except Exception as e:
            logger.error(f"LLM 요약 생성 중 오류 발생: {e}")
            return self.generate_basic_summary(story_json)
    
    def _create_summary_prompt(self, story_json: str) -> str:
        """요약 생성을 위한 프롬프트를 생성합니다."""
        # 데이터가 너무 클 경우 일부만 사용
        story_data_for_prompt = story_json[:3000] if len(story_json) > 3000 else story_json
        
        return f"""당신은 투자교육 게임 스토리 분석 전문가입니다.

아래 JSON 스토리 데이터를 분석하여 투자 전략과 시장 흐름을 분석하는 전문적인 요약을 생성해주세요.

요약 작성 지침:
- 120자 이내로 전문적이고 분석적으로 작성 (공백 포함)
- 추측성 어조 사용 ("~할 수 있습니다", "~일 것입니다", "~될 수 있습니다")
- 저위험/중위험/고위험 종목별 흐름 패턴 분석
- 투자 시점과 전략의 효과성 평가
- 분산투자 vs 집중투자 전략 관점에서 분석
- 시장 상황에 따른 기회 포착 능력 평가

분석 관점:
- 초반/중반/후반 구간별 종목 성과 변화
- 위험도별 수익률과 변동성 패턴
- 외부 이벤트(뉴스)에 대한 종목별 반응
- 최적 투자 전략과 포트폴리오 구성

좋은 예시:
"중위험 종목은 초반 급등 후 조정, 고위험 종목은 큰 등락을 거쳐 회복할 수 있어 분산보다 고위험 중심 전략이 유리할 것입니다."
"저위험 종목은 안정적 상승, 고위험 종목은 후반 급등으로 적극적 리스크 테이킹이 높은 수익을 가져다줄 수 있을 것입니다."

스토리 데이터:
{story_data_for_prompt}

위 데이터를 바탕으로 투자 전략과 시장 흐름을 분석하는 전문적인 요약을 생성해주세요."""
    
    def _process_summary_text(self, summary_result: str) -> str:
        """요약 텍스트를 정리하고 길이를 제한합니다."""
        # 요약 텍스트 정리 (JSON이나 불필요한 태그 제거)
        summary_text = summary_result.strip()
        
        # JSON 형태로 반환된 경우 텍스트만 추출
        if summary_text.startswith('{') or summary_text.startswith('['):
            try:
                import re
                # 간단한 텍스트 추출 시도
                text_match = re.search(r'"([^"]+)"', summary_text)
                if text_match:
                    summary_text = text_match.group(1)
            except:
                pass
        
        # 불필요한 따옴표나 특수문자 제거
        summary_text = summary_text.replace('"', '').replace("'", '').strip()
        
        # 요약이 너무 길면 자연스럽게 잘라내기 (120자 제한)
        if len(summary_text) > 120:
            # 문장이 끝나는 지점에서 자르기 시도
            cut_point = 117
            while cut_point > 80 and summary_text[cut_point] not in ['!', '?', '.', '요', '다', '네', '죠']:
                cut_point -= 1
            
            if cut_point <= 80:  # 적절한 자를 지점을 못 찾으면 강제로 자르기
                summary_text = summary_text[:117] + "..."
            else:
                summary_text = summary_text[:cut_point + 1]
        
        return summary_text

# 전역 인스턴스 (싱글톤 패턴)
_summary_generator = None

def get_summary_generator() -> SummaryGenerator:
    """요약 생성기 인스턴스를 반환합니다. (싱글톤 패턴)"""
    global _summary_generator
    if _summary_generator is None:
        _summary_generator = SummaryGenerator()
    return _summary_generator

# 편의 함수들
def generate_story_summary_with_llm(story_json: str) -> str:
    """
    LLM을 활용한 스토리 요약 생성 (동기 함수)
    
    Args:
        story_json (str): 스토리 JSON 문자열
        
    Returns:
        str: 생성된 요약
    """
    generator = get_summary_generator()
    if not generator.is_initialized:
        generator.initialize_llm()
    return generator.generate_llm_summary(story_json)

def generate_story_summary(story_json: str) -> str:
    """
    기본 스토리 요약 생성 (편의 함수)
    
    Args:
        story_json (str): 스토리 JSON 문자열
        
    Returns:
        str: 생성된 기본 요약
    """
    generator = get_summary_generator()
    return generator.generate_basic_summary(story_json)

def initialize_llm() -> bool:
    """
    LLM 초기화 (편의 함수)
    
    Returns:
        bool: 초기화 성공 여부
    """
    generator = get_summary_generator()
    return generator.initialize_llm()