# 数据下载记录


## 1. ZS11 参考基因组


```bash
cd /mnt/e/work/zs11_atac/genome 
wget -c "https://yanglab.hzau.edu.cn/static/bnir/assets//genomic_sequence/BnIRData/AACC.Brassica_napus/ZS11/v0/Brassica_napus.ZS11.v0.genome.fa.gz" 
wget -c "https://yanglab.hzau.edu.cn/static/bnir/assets//genomic_sequence/BnIRData/AACC.Brassica_napus/ZS11/v0/Brassica_napus.ZS11.v0.gene.gff3.gz" 
gunzip Brassica_napus.ZS11.v0.genome.fa.gz
gunzip Brassica_napus.ZS11.v0.gene.gff3.gz
```


## 2. ATAC-seq 数据

NCBI 直连速度极慢（约 12 KB/s），清华镜像无对应文件，ENA 单线程 wget 也只有 366 KB/s。

最终用 kingfisher 的 ena-ftp 模式（底层 aria2c 多线程）成功下载，速度达到 4.5–10 MiB/s。

```bash
cd /mnt/e/work/zs11_atac/fastq
kingfisher get -r SRR17036599 -m ena-ftp --output-format fastq.gz
kingfisher get -r SRR17036598 -m ena-ftp --output-format fastq.gz
```

下载后得到四个文件:

- SRR17036599_1.fastq.gz、SRR17036599_2.fastq.gz
- SRR17036598_1.fastq.gz、SRR17036598_2.fastq.gz

