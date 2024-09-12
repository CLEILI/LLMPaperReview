from setenvrion import pdf_dir,image_dir
import os
pdfs=[]
pdfs_path=pdf_dir
'''for filename in os.listdir(pdfs_path):#read all pdf names
    if filename.endswith('.pdf'):
        new_filename=''
        if "conff" in filename:
            print(filename)
            new_filename=filename.replace("conff","confi")
        if "Classiff" in filename:
            print(filename)
            new_filename=filename.replace("Classiff","Classifi")
        new,_ = os.path.splitext(filename)
        pdfs.append(new)'''
name=[]
#TODO:change pdf name and image name which include the words
#NOTE:dont consider the uppper lower alpherbet because I change all the file,just ensure the word have no syntax errors
for filename in os.listdir(pdfs_path):#read all pdf names
    if filename.endswith('.pdf'): 
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