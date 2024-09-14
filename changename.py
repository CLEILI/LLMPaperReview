from setenvrion import pdf_dir,image_dir
import os
def WrongWords():
    #TODO:change pdf name and image name which include the words
    #NOTE:dont consider the uppper lower alpherbet because I change all the file,just ensure the word have no syntax errors
    for filename in os.listdir(image_dir):#read all pdf names
        if filename.endswith('.pdf'): 
            newname=filename
            temp=filename
            #Trafffc,Conffdential,Classiffcation,Offfoading,Afffnity,Proffle
            #Identiffcation,Efffcient,efficient,Efffciency,Artiffcial,Speciffc
            if "Trafffc" in filename:
                newname=temp.replace("Trafffc","Traffic")
            if "Conffdential" in filename:
                newname=temp.replace("Conffdential","Confidential")
            if "Classiffcation" in filename:
                newname=temp.replace("Classiffcation","Classification")
            if "Offfoading" in filename:
                newname=temp.replace("Offfoading","Offloading")
            if "Afffnity" in filename:
                newname=temp.replace("Afffnity","Affinity")
            if "Proffle" in filename:
                newname=temp.replace("Proffle","Profile")
            if "Identiffcation" in filename:
                newname=temp.replace("Identiffcation","Identification")
            if "Efffcient" in filename:
                newname=temp.replace("Efffcient","Efficient")
            if "efffcient" in filename:
                newname=temp.replace("efffcient","efficient")
            if "Efffciency" in filename:
                newname=temp.replace("Efffciency","Efficiency")
            if "Artiffcial" in filename:
                newname=temp.replace("Artiffcial","Artificial")
            if "Speciffc" in filename:
                newname=temp.replace("Speciffc","Specific")
            os.rename(f"./paper_pdfs/{filename}",f"./paper_pdfs/{newname}")
        if filename.endswith('.jpg'):
            newname=filename
            temp=filename
            #Trafffc,Conffdential,Classiffcation,Offfoading,Afffnity,Proffle
            #Identiffcation,Efffcient,Efffciency,Artiffcial,Speciffc
            if "Trafffc" in filename:
                newname=temp.replace("Trafffc","Traffic")
            if "Conffdential" in filename:
                newname=temp.replace("Conffdential","Confidential")
            if "Classiffcation" in filename:
                newname=temp.replace("Classiffcation","Classification")
            if "Offfoading" in filename:
                newname=temp.replace("Offfoading","Offloading")
            if "Afffnity" in filename:
                newname=temp.replace("Afffnity","Affinity")
            if "Proffle" in filename:
                newname=temp.replace("Proffle","Profile")
            if "Identiffcation" in filename:
                newname=temp.replace("Identiffcation","Identification")
            if "Efffcient" in filename:
                newname=temp.replace("Efffcient","Efficient")
            if "efffcient" in filename:
                newname=temp.replace("efffcient","efficient")
            if "Efffciency" in filename:
                newname=temp.replace("Efffciency","Efficiency")
            if "Artiffcial" in filename:
                newname=temp.replace("Artiffcial","Artificial")
            if "Speciffc" in filename:
                newname=temp.replace("Speciffc","Specific")
            os.rename(f"./images/{filename}",f"./images/{newname}")


'''
TBA-GNN A Trafffc Behavior Analysis Model with Graph Neural Networks for Malicious Trafffc Detection
A Conffdential Batch Payment Scheme with Integrated Auditing for Enhanced Data Trading Security
Towards Robust Internet of Vehicles Security An Edge Node-Based Machine Learning Framework for Attack Classiffcation
Joint Data and Computing Offfoading Strategies for Cloud-Edge Collaboration
Dynamic Offfoading Control for Waste Sorting Based on Deep Q-Network
QoS-aware Energy-Efffcient Multi-UAV Offfoading Ratio and Trajectory Control Algorithm in Mobile Edge Computing
Harnessing Afffnity Propagation for Enhanced Clustering in Federated Learning
Large Language Models Know Your Intention and Proffle if Given the Trajectory Data
RF Fingerprint Identiffcation of Wireless Devices Based on Machine Learning
Task-aware Power Allocation with Efffcient Temporal Charging Scheduling
Efffcient Deployment and Fine-Tuning of Transformer-Based Models on the Device-Edge
MineLoRa Markov Transition Fields and Adaptive Neural Networks for LoRa Device Radio Frequency Fingerprint Identiffcation 
Towards Communication-Efffcient Collaborative Perception Harnessing Channel-Spatial Attention and Knowledge Distillation
------------AST-PG Attention Based Spatial-Temporal Point-ofInterest Groups Model for Real-Time Point-of-Interest Recommendation
DevDet Detecting IoT Device Impersonation Attacks via Trafffc Based Identiffcation
CoR-FHD Communication-Efffcient and Robust Federated Hyperdimensional Computing for Activity Recognition
HyperFedNet Communication-Efffcient Personalized Federated Learning Via Hypernetwork
Optimization of Energy Efffciency in Hierarchical Federated Learning Based on NOMA and Aircomp
Enhancing Wireless Security in IoT Ecosystems through Artiffcial Intelligence Opportunities and Challenges
Anti-Packet-Loss Encrypted Trafffc Classification via Masked Autoencoder
An Efffcient Fire Detection Algorithm with Dataset Augumentation Based on Diffusion
FusionFlow Neural Fusion and Compression for Communication-Efffcient Edge-Cloud Collaborative Computing
SAE-CNN A Spatial Attention Augmented Convolutional Neural Network for Service Type Identiffcation in 5G Heterogeneous Networks
DS-TFP A Distriuted and Secure Trafffc Flow Prediction Framework Based on Federated Graph Learning
A Provably Secure and Efffcient One-to-many Authentication and Key Agreement Protocol for Asymmetric Intelligent Environments
Mar-DSL A Domain-Speciffc Language for IoT Systems Implementation
QoS-Constrained, Reliable and Energy-Efffcient Task Deployment in Cloud Computing
BufferConcede Conceding Buffer for RoCE Trafffc in TCP RoCE Mix-Flows


'''
def DeleteSpace(folder_path):

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 检查文件是否以 ".pdf" 结尾，并且在 ".pdf" 前是否有空格
        if filename.endswith('.jpg') and ' .jpg' in filename:
            # 构造新的文件名，去除 .pdf 前的空格
            new_filename = filename.replace(' .jpg', '.jpg')
            
            # 获取完整的旧文件路径和新文件路径
            old_file = os.path.join(folder_path, filename)
            new_file = os.path.join(folder_path, new_filename)
            
            # 重命名文件
            os.rename(old_file, new_file)
            print(f"重命名: {filename} -> {new_filename}")

    print("文件名处理完成。")

DeleteSpace("./images")