# 过滤与去重

## 1. 过滤（samtools）

保留 properly paired（-f 2）、MAPQ ≥ 10（-q 10），去掉未比对、非主要比对、PCR 重复等（-F 1804）。

```bash
cd /mnt/e/work/zs11_atac

for sample in SRR17036599 SRR17036598; do
    samtools view -@ 8 -h -f 2 -F 1804 -q 10 bam/${sample}.sorted.bam \
    | samtools view -b -o bam_filt/${sample}.filt.bam
    samtools sort -@ 8 -o bam_filt/${sample}.filt.sorted.bam bam_filt/${sample}.filt.bam
    samtools index bam_filt/${sample}.filt.sorted.bam
done
```

## 2. 去重（Picard）

```bash
cd /mnt/e/work/zs11_atac

for sample in SRR17036599 SRR17036598; do
    picard AddOrReplaceReadGroups \
        I=bam_filt/${sample}.filt.sorted.bam \ 
        O=bam_filt/${sample}.rg.bam \
        RGID=${sample} RGLB=lib1 RGPL=ILLUMINA RGPU=unit1 RGSM=${sample} \
        SORT_ORDER=coordinate CREATE_INDEX=true

    picard MarkDuplicates \
        I=bam_filt/${sample}.rg.bam \
        O=bam_filt/${sample}.dedup.bam \
        M=bam_filt/${sample}.dup_metrics.txt \ 
        REMOVE_DUPLICATES=true READ_NAME_REGEX=null CREATE_INDEX=true
done
```

##3. 去重率

| 样本 | 重复率 |
|:---|:---|
| SRR17036599 | 24.8% |
| SRR17036598 |	19.6% |

