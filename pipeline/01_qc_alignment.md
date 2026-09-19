# 质控与比对

## 1. 质控（fastp + FastQC）

```bash
conda activate atac
cd /mnt/e/work/zs11_atac

for sample in SRR17036599 SRR17036598; do
    fastqc fastq/${sample}_1.fastq.gz fastq/${sample}_2.fastq.gz -o qc/raw
    fastp -i fastq/${sample}_1.fastq.gz -I fastq/${sample}_2.fastq.gz \
          -o qc/clean/${sample}_clean_1.fastq.gz \
          -O qc/clean/${sample}_clean_2.fastq.gz \
          -h qc/clean/${sample}.html -j qc/clean/${sample}.json \ 
          --thread 16
done
```

## 2. 构建 Bowtie2 索引

```bash
cd /mnt/e/work/zs11_atac/genome

bowtie2-build --threads 8 Brassica_napus.ZS11.v0.genome.fa zs11_index
```

## 3. 比对（Bowtie2）

```bash
cd /mnt/e/work/zs11_atac

for sample in SRR17036599 SRR17036598; do
    bowtie2 -x genome/zs11_index \
            -1 qc/clean/${sample}_clean_1.fastq.gz \
            -2 qc/clean/${sample}_clean_2.fastq.gz \
            --very-sensitive -X 2000 -p 8 \
            2> logs/${sample}_bowtie2.log \
    | samtools sort -@ 8 -o bam/${sample}.sorted.bam -
    samtools index bam/${sample}.sorted.bam
done
```

## 4. 比对结果统计

| 样本 | 比对率 | properly paired |
|:---|:---|
| SRR17036599 | 88.13% | 75.38% |
| SRR17036598 |	89.90% | 77.06% |

