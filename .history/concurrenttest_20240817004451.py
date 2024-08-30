import re
import json

# 长字符串示例
long_string = """
Some random text before...
{"comment": "This paper presents a strong research background addressing important questions in mobile crowd sensing. It utilizes deep learning techniques for data aggregation and quality assurance. However, the completeness of the paper structure is uncertain, and while it has a clear theme and analysis, the originality of the content is not fully established. The algorithm appears feasible based on simulation results, but the details on experiments and high-tech standards are lacking. The conclusion's clarity and contribution to the field need further evaluation.", "papername": "A Data Aggregation Framework based on Deep Learning for Mobile Crowd-sensing Paradigm", "score": "75.00"}
Some random text after...
{"comment": "This paper has a strong research background and a complete structure, presenting two effective algorithms for merging blockchain systems. It has a clear theme and analysis, with valuable conclusions that highlight the efficiency and scalability of the proposed solutions. The content is original and contributes significantly to the field of blockchain integration. The experiments and analyses conducted meet high-tech standards, making it a robust contribution to the thematic area.", "papername": "A Novel Merging Framework for Homogeneous and Heterogeneous Blockchain Systems", "score": "88.00"}
{"comment": "This paper addresses significant challenges in Physical Layer Security for mobile communications, proposing an original cooperative jamming scheme. It demonstrates feasibility and effectiveness through numerical simulations, although details on high-tech standards are not fully provided. The conclusions drawn are valuable, and the paper contributes meaningfully to the field of secure transmission. However, further evaluation of practical applications is necessary.", "papername": "An Effective Cooperative Jamming-based Secure Transmission Scheme for a Mobile Scenario", "score": "85.00"}
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

