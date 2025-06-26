"""
데이터 변환 및 인코딩 처리 유틸리티 함수들
"""
import pandas as pd
import json

def clean_string_encoding(text):
    """문자열의 인코딩 문제를 해결하는 함수"""
    if text is None or text == 'nan':
        return None
    
    if not isinstance(text, str):
        text = str(text)
    
    try:
        # UTF-8 인코딩 테스트
        text.encode('utf-8')
        return text
    except UnicodeEncodeError:
        # 문제가 있는 문자 제거
        return text.encode('utf-8', errors='ignore').decode('utf-8')
    except Exception:
        # 모든 예외 상황에서 안전한 변환
        try:
            return repr(text)
        except:
            return "encoding_error"


def sanitize_dataframe_for_json(df):
    """DataFrame을 JSON 변환에 안전하게 만드는 함수"""
    print("DataFrame JSON 변환 준비 중...")
    
    # 복사본 생성
    df_clean = df.copy()
    
    for col in df_clean.columns:
        print(f"컬럼 '{col}' 처리 중... (타입: {df_clean[col].dtype})")
        
        try:
            # UUID 객체 처리
            if df_clean[col].dtype == 'object':
                # UUID 객체를 문자열로 변환
                df_clean[col] = df_clean[col].apply(lambda x: str(x) if x is not None else None)
                
                # 문자열 인코딩 문제 해결
                df_clean[col] = df_clean[col].apply(lambda x: clean_string_encoding(x) if x is not None else None)
            
            # 숫자형 데이터에서 inf, -inf 처리
            elif df_clean[col].dtype in ['float64', 'float32']:
                df_clean[col] = df_clean[col].replace([float('inf'), float('-inf')], None)
            
        except Exception as e:
            print(f"컬럼 '{col}' 처리 실패: {e}")
            # 실패한 컬럼은 안전하게 문자열로 변환
            try:
                df_clean[col] = df_clean[col].astype(str, errors='ignore')
                df_clean[col] = df_clean[col].apply(lambda x: clean_string_encoding(x) if x != 'nan' else None)
            except:
                # 최후의 수단: 모든 값을 None으로 설정
                df_clean[col] = None
                print(f"컬럼 '{col}'을 None으로 설정했습니다.")
    
    print("DataFrame JSON 변환 준비 완료")
    return df_clean




def safe_dataframe_to_json(df):
    """안전한 DataFrame to JSON 변환 (default_handler 사용)"""
    try:
        # 첫 번째 시도: default_handler를 사용한 변환
        json_data = df.to_json(orient='records', default_handler=str, force_ascii=False)
        return json_data
        
    except Exception as e:
        print(f"기본 JSON 변환 실패: {e}")
        
        # 두 번째 시도: 청크 단위 처리
        chunk_size = 500  # 더 작은 청크 크기
        json_chunks = []
        
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i:i+chunk_size]
            
            try:
                # default_handler 사용
                chunk_json = chunk.to_json(orient='records', default_handler=str, force_ascii=False)
                json_chunks.append(chunk_json)
                
            except Exception as chunk_error:
                print(f"청크 {i//chunk_size + 1} 변환 실패: {chunk_error}")
                
                # 청크를 더 작은 단위로 분할하여 처리
                try:
                    mini_chunks = []
                    for j in range(0, len(chunk), 10):  # 10개씩 처리
                        mini_chunk = chunk.iloc[j:j+10]
                        try:
                            mini_json = mini_chunk.to_json(orient='records', default_handler=str, force_ascii=False)
                            mini_chunks.append(mini_json[1:-1])  # 대괄호 제거
                        except:
                            # 개별 행 처리
                            for idx, row in mini_chunk.iterrows():
                                try:
                                    row_dict = {}
                                    for col, val in row.items():
                                        try:
                                            row_dict[col] = str(val) if val is not None else None
                                        except:
                                            row_dict[col] = "conversion_error"
                                    
                                    row_json = json.dumps(row_dict, ensure_ascii=False)
                                    mini_chunks.append(row_json)
                                except:
                                    continue
                    
                    if mini_chunks:
                        chunk_json = '[' + ','.join(mini_chunks) + ']'
                        json_chunks.append(chunk_json)
                    else:
                        json_chunks.append('[]')
                        
                except Exception as final_error:
                    print(f"청크 최종 처리 실패: {final_error}")
                    json_chunks.append('[]')
        
        # 최종 결합
        if json_chunks:
            valid_chunks = []
            for chunk in json_chunks:
                if chunk != '[]' and len(chunk) > 2:
                    # 대괄호 제거
                    inner_content = chunk[1:-1].strip()
                    if inner_content:
                        valid_chunks.append(inner_content)
            
            if valid_chunks:
                json_data = '[' + ','.join(valid_chunks) + ']'
            else:
                json_data = '[]'
        else:
            json_data = '[]'
        
        return json_data