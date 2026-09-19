# ZS11 CharPlant OCR Prediction Pipeline

基于 CharPlant 的甘蓝型油菜 ZS11 染色质开放区域（OCR）从头预测流程记录。

## 项目目标

- 利用 ZS11 种子时期 ATAC-seq 数据，训练 CharPlant 模型 
- 对 ZS11 全基因组进行 OCR 从头预测 
- 评估预测 OCR 与实验 ATAC-seq 峰的重叠率（召回率） 
- 探索不同步长（1bp vs 10bp）对预测结果的影响（待定）

## 数据来源

| 数据类型 | 来源 | 编号 |
|:---|:---|:---|
| ZS11 参考基因组 | BnIR 数据库 | Brassica_napus.ZS11.v0 |
| ZS11 ATAC-seq 重复1 | NCBI SRA | SRR17036599 | 
| ZS11 ATAC-seq 重复2 | NCBI SRA | SRR17036598 |

## 流程概览

1. 数据下载（ENA FTP） 
2. 质控（fastp、FastQC） 
3. 比对（Bowtie2） 
4. 过滤去重（samtools、Picard） 
5. Peak Calling（MACS3） 
6. 模型训练（CharPlant） 
7. Motif 提取（motif.py） 
8. 从头预测（de_novo_prediction.py） 
9. 结果评估（bedtools intersect）

## 环境依赖

- WSL2 Ubuntu 22.04 
- Miniconda 
- Python 3.6 
- TensorFlow 1.15 (CPU) 
- Keras 2.2.4 
- Bowtie2 2.5.5 
- samtools 1.24 
- MACS3 3.0.4 
- bedtools 2.31.1 
- Picard 3.5.0

## 关键结果
（待补充）

## 目录结构

- `environment/`：环境搭建记录 
- `data/`：数据下载记录 
- `pipeline/`：各步骤操作记录
- `results/`：结果汇总
