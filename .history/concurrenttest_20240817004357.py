import re
import json

# 长字符串示例
long_string = """
Some random text before...
{"comment": "This paper presents a strong research background addressing important questions in mobile crowd sensing. It utilizes deep learning techniques for data aggregation and quality assurance. However, the completeness of the paper structure is uncertain, and while it has a clear theme and analysis, the originality of the content is not fully established. The algorithm appears feasible based on simulation results, but the details on experiments and high-tech standards are lacking. The conclusion's clarity and contribution to the field need further evaluation.", "papername": "A Data Aggregation Framework based on Deep Learning for Mobile Crowd-sensing Paradigm", "score": "75.00"}
Some random text after...
"""

# 正则表达式匹配 JSON 格式的字符串
pattern = r'\{.*?"comment".*?"papername".*?"score".*?\}'

# 使用正则表达式在长字符串中查找符合格式的子字符串
matches = re.findall(pattern, long_string)

# 遍历匹配结果并将其解析为字典
for match in matches:
    try:
        parsed_json = json.loads(match)
        print(parsed_json)
    except json.JSONDecodeError as e:
        print(f"JSON 解码失败: {e}")

