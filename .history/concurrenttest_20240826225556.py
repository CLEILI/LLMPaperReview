import re
import json

def extract_papers(text):
    # 定义匹配模式来提取 Paper, Comment 和 Score
    paper_pattern = r"Paper:\s*(.*)"
    comment_pattern = r"Comment:\s*(.*)"
    score_pattern = r"Score:\s*(\d+\.\d+)"

    # 用来存储每个提取到的 JSON 对象的元组
    papers = []

    # 匹配所有 Paper、Comment 和 Score 段落
    paper_sections = re.findall(r"Paper:(.*?)\n\s*- Comment:(.*?)\n\s*- Score:(\d+\.\d+)", text, re.DOTALL)

    # 遍历每个匹配的部分并转换为 JSON 格式
    for paper_section in paper_sections:
        paper_title = paper_section[0].strip()
        comment = paper_section[1].strip()
        score = float(paper_section[2].strip())

        # 创建一个 JSON 对象
        paper_json = {
            "title": paper_title,
            "comment": comment,
            "score": score
        }

        # 将 JSON 转换为字符串并添加到元组中
        papers.append(json.dumps(paper_json))

    return tuple(papers)

# 示例字符串
text = """
Based on the evaluations of the papers, here are the comments and scores for each paper:

1. **Paper: A Flexible Numerology Resource Allocation to Guarantee Delay and Reliability Requirements in 5G NR-V2X Networks**
   - Comment: This paper addresses important questions in resource allocation for 5G NR-V2X networks by proposing a flexible numerology resource allocation algorithm based on deep learning. It contributes to enhancing existing knowledge in the field and demonstrates the feasibility and effectiveness of the algorithm through simulations.
   - Score: 85.00

2. **Paper: A DRL-Based Edge Intelligent Servo Control with Semi-Closed-Loop Feedbacks in Industrial IoT**
   - Comment: The paper presents a novel deep reinforcement learning-based control algorithm for industrial servo systems, showcasing advancements in edge computing and control strategies. It contributes to the thematic area of industrial IoT and servo control with its innovative approach.
   - Score: 88.00

3. **Paper: FEKNN A Wi-Fi Indoor Localization Method Based on Feature Enhancement and KNN**
   - Comment: This paper introduces the FEKNN method for Wi-Fi indoor localization, enhancing accuracy through feature enhancement and KNN. The experiments validate the effectiveness of the approach, although more details on experiments and analyses would further strengthen the paper.
   - Score: 82.00

4. **Paper: A DRL-Based Hierarchical Game for Physical Layer Security Aware Cooperative Communications**
   - Comment: The paper proposes a hierarchical game framework for physical layer security in wireless networks, integrating deep reinforcement learning for optimal strategies. It contributes to the field by addressing security challenges in cooperative communications.
   - Score: 87.00

5. **Paper: BCPP-IAS Blockchain-Based Cross-Domain Identity Authentication Scheme for IoT with Privacy Protection**
   - Comment: This paper introduces a blockchain-based identity authentication scheme for IoT, focusing on security and privacy. The proposed scheme enhances authentication efficiency and privacy protection, contributing significantly to cross-domain identity authentication.
   - Score: 84.00

These scores reflect the evaluation of each paper based on the standards provided.

"""

# 提取信息并返回元组
result = extract_papers(text)
print(result)
