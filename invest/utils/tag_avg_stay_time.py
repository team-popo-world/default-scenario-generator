import pandas as pd

# 평균 tag 뉴스 발생 턴 체류 시간
def tag_avg_stay_time(df):
    tag_turn_df = df[['investSessionId',
                        'userId',
                        'age',
                        'turn',
                        'newsTag',
                        'startedAt',
                        'endedAt']].drop_duplicates()

    tagAvgStayTime = tag_turn_df.drop_duplicates(subset=['investSessionId', 'turn']).copy()
    tagAvgStayTime = tagAvgStayTime[tagAvgStayTime['newsTag'] != "all"]

    # 문자열을 datetime으로 변환
    tagAvgStayTime['startedAt'] = pd.to_datetime(tagAvgStayTime['startedAt'])
    tagAvgStayTime['endedAt'] = pd.to_datetime(tagAvgStayTime['endedAt'])

    tagAvgStayTime["turnDuration"] = tagAvgStayTime["endedAt"] - tagAvgStayTime["startedAt"]
    tagAvgStayTime = tagAvgStayTime.groupby(["investSessionId", 'userId', 'age'])["turnDuration"].mean().reset_index(name="tagAvgStayTime")

    return tagAvgStayTime