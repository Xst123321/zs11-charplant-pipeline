# 环境搭建记录

## 1. WSL2 + Ubuntu 22.04

- 安装 WSL2，导入 Ubuntu 22.04 到 E 盘（`E:\WSL\Ubuntu`），避免占用 C 盘空间。 
- `.wslconfig` 配置：`memory=44GB`，`swap=32GB`。 
- 创建普通用户 `bio`，配置 SSH 服务，用 FinalShell 连接。

## 2. Miniconda

```bash
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

配置清华镜像源（加速国内下载）：

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ 
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ 
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ 
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
conda config --set show_channel_urls yes
```

## 3. atac 环境

```bash
conda create -n atac -c bioconda sra-tools bowtie2 samtools macs2 fastp fastqc picard bedtools kingfisher -y
```

## 4. charplant-cpu 环境

```bash
conda create -n charplant-cpu python=3.6 -y 
conda activate charplant-cpu 
pip install numpy==1.16.1 matplotlib==3.3.2 pyfiglet==0.8.post1 scikit-learn==0.22 h5py==2.7.1 
conda install tensorflow=1.15 -y 
pip install keras==2.2.4 
pip install h5py==2.10.0
conda install -c bioconda snakemake bowtie2 macs2 samtools -y
```

## 5. 关键问题记录

- MACS2 报错 __log_finite：Ubuntu 22.04 的 glibc 与 MACS2 2.2.9.1 不兼容，改用 MACS3 3.0.4。
- h5py 版本冲突：Keras 2.2.4 加载权重时报 'str' object has no attribute 'decode'，降级 h5py 到 2.10.0。
- 内存不足：WSL 默认内存上限为物理内存的 50%，调高 .wslconfig 的 memory 和 swap。
