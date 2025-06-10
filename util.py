import re

def extract_json(text):
    # 코드블록(```json ... ```) 제거
    text = text.strip()
    codeblock_pattern = r"```(?:json)?(.*?)```"
    match = re.search(codeblock_pattern, text, re.DOTALL)
    if match:
        json_text = match.group(1).strip()
    else:
        json_text = text
    # 가장 먼저 나오는 [ 또는 {부터 끝까지 추출
    start = min([json_text.find(c) if json_text.find(c) != -1 else 99999 for c in ['[', '{']])
    if start != 99999:
        json_text = json_text[start:]
    return json_text