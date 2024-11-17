import re
import json

def re3_5turbo(text):

    # 匹配所有 Paper、Comment 和 Score 段落
   pattern1=r'\*\*Papername:\*\*\s*(.*?)\n\*\*Comment:\*\*\s*(.*?)\n\*\*Score:\*\*\s*([0-9.]+)'

   paper_sections = re.findall(pattern1, text)
   pdfdic={}
   # 遍历每个匹配的部分并转换为 JSON 格式
   for element in paper_sections:
      print(element[0])
      print(element[1])
      print(element[2])
   return pdfdic


    

# 示例字符串
text = """
Based on the evaluations of the papers, here are the comments and scores for each paper:

1. Paper: A Flexible Numerology Resource Allocation to Guarantee Delay and Reliability Requirements in 5G NR-V2X Networks**
   - Comment: This paper addresses important questions in resource allocation for 5G NR-V2X networks by proposing a flexible numerology resource allocation algorithm based on deep learning. It contributes to enhancing existing knowledge in the field and demonstrates the feasibility and effectiveness of the algorithm through simulations.
   - Score: 85.00

2. **Paper: A DRL-Based Edge Intelligent Servo Control with Semi-Closed-Loop Feedbacks in Industrial IoT**
   - **Comment**: The paper presents a novel deep reinforcement learning-based control algorithm for industrial servo systems, showcasing advancements in edge computing and control strategies. It contributes to the thematic area of industrial IoT and servo control with its innovative approach.
   - **Score**: 88.00

3. **Paper: FEKNN A Wi-Fi Indoor Localization Method Based on Feature Enhancement and KNN**
   - Comment: This paper introduces the FEKNN method for Wi-Fi indoor localization, enhancing accuracy through feature enhancement and KNN. The experiments validate the effectiveness of the approach, although more details on experiments and analyses would further strengthen the paper.
   - Score: 82.00

4. **Paper: A DRL-Based Hierarchical Game for Physical Layer Security Aware Cooperative Communications**
   - **Comment:** The paper proposes a hierarchical game framework for physical layer security in wireless networks, integrating deep reinforcement learning for optimal strategies. It contributes to the field by addressing security challenges in cooperative communications.
   - **Score:** 87.00

5. **Paper: BCPP-IAS Blockchain-Based Cross-Domain Identity Authentication Scheme for IoT with Privacy Protection**
   - Comment: This paper introduces a blockchain-based identity authentication scheme for IoT, focusing on security and privacy. The proposed scheme enhances authentication efficiency and privacy protection, contributing significantly to cross-domain identity authentication.
   - Score: 84.00

**Papername:**  
An Effective Cooperative Jamming-based Secure Transmission Scheme for a Mobile Scenario  
**Comment:**  
This paper addresses an important question in the realm of Physical Layer Security (PLS) for mobile communications, proposing a novel cooperative jamming scheme. While it presents a clear theme and analysis, the paper lacks detailed information on the structure and experimental validation. The originality is evident in its approach to enhancing security in dynamic environments. However, without specific details on the feasibility and effectiveness of the algorithm, the contributions remain somewhat unclear. Overall, it provides valuable insights into secure communication in mobile scenarios.  
**Score:**  
75.00  

These scores reflect the evaluation of each paper based on the standards provided.

- Paper: A Novel Merging Framework for Homogeneous and Heterogeneous Blockchain Systems
  - **Score**: 85.00
  - **Comment**: The paper presents feasible solutions for blockchain merging, although more detailed experiments and analyses could enhance its overall impact.

- Paper: An Effective Cooperative Jamming-based Secure Transmission Scheme for a Mobile Scenario
  - **Score**: 80.00
  - **Comment**: The paper contributes to enhancing physical layer security in mobile scenarios, but further details on experiments and algorithm feasibility would strengthen its findings.

### Paper: A Novel Merging Framework for Homogeneous and Heterogeneous Blockchain Systems
- **Score**: 85.00
- **Comments**: This paper presents innovative solutions, Homogeneous Chain Consolidation (HCC) and Heterogeneous Multi-chain Integration Architecture (HMIA), for merging diverse blockchain systems. The research background is strong, addressing the important question of efficient blockchain system integration. The paper has a complete structure with a clear theme, analysis, and conclusion. It contributes to the existing knowledge system in blockchain merging by proposing original solutions. While the experiments and analyses are not detailed, the proposed algorithm is deemed feasible and effective. The conclusion is clear, correct, reliable, and valuable, summarizing the contributions effectively. The paper has a certain contribution and driving effect on the thematic area of blockchain integration.

### Paper: An Effective Cooperative Jamming-based Secure Transmission Scheme for a Mobile Scenario
- **Score**: 80.00
- **Comments**: This paper introduces a Cooperative Jamming scheme for enhancing physical layer security in mobile scenarios. The research background is strong, addressing an important question in wireless communication security. While the paper's structure and theme are clear, the detailed experiments and analyses are not explicitly provided. The content is original and contributes to the existing knowledge system in physical layer security. The proposed algorithm is considered feasible and effective, focusing on enhancing system security performance in mobile scenarios. The conclusion, although not directly assessed, is expected to be valuable based on the paper's contributions. The paper has a certain contribution and driving effect on the thematic area of Physical Layer Security (PLS) in wireless communications.

**Papername:**  
A Flexible Numerology Resource Allocation to Guarantee Delay and Reliability Requirements in 5G NR-V2X Networks  
**Comment:**  
The paper effectively addresses the delay and reliability challenges in 5G NR-V2X networks, proposing a flexible numerology resource allocation algorithm based on deep learning. It has a clear structure and theme, with an original approach that enhances existing knowledge in resource allocation. The experimental results indicate good convergence and effectiveness in meeting transmission requirements. However, the paper lacks detailed descriptions of the experimental methodologies. The contributions to the field are significant, particularly in optimizing resource allocation for vehicular communication.  
**Score:**  
82.00  

"""

# 提取信息并返回元组
string="fnasfjioals\n"
tt=string.replace("\n","")
print(tt)
