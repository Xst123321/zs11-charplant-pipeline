# Peak Calling（MACS3）

## 1. 生成基因组索引

```bash
conda activate atac
cd /mnt/e/work/zs11_atac

samtools faidx genome/Brassica_napus.ZS11.v0.genome.fa
GENOME_SIZE=$(awk '{sum+=$2} END{print sum}' genome/Brassica_napus.ZS11.v0.genome.fa.fai)
echo ${GENOME_SIZE}
```

基因组有效大小：1,010,887,456 bp（约 1.01 Gb）。

## 2. MACS3 Peak Calling

```bash
cd /mnt/e/work/zs11_atac

for sample in SRR17036599 SRR17036598; do
    macs3 callpeak \
    -t bam_filt/${sample}.dedup.bam \
    -f BAMPE \
    -g ${GENOME_SIZE} \
    -n ${sample} \
    --outdir macs2_out \
    -q 0.01 \
    --keep-dup all 2> logs/${sample}_macs3.log
done
```

## 3. 生成 OCR BED

```bash 
cd /mnt/e/work/zs11_atac

for sample in SRR17036599 SRR17036598; do
    awk 'BEGIN{OFS="\t"} ($3-$2)>200 {print $1,$2,$3}' \ 
        macs2_out/${sample}_peaks.narrowPeak > bed/${sample}.ocr.gt200.bed
done

cat bed/SRR17036599.ocr.gt200.bed bed/SRR17036598.ocr.gt200.bed \
    | sort -k1,1 -k2,2n \
    | bedtools merge -i - > bed/zs11_merged_ocr.bed

wc -l bed/zs11_merged_ocr.bed
```

合并后共得到 19,041 个 OCR 区域，文件为 bed/zs11_merged_ocr.bed。

## 4. 备注

- MACS2 2.2.9.1 在 Ubuntu 22.04 上因 __log_finite 符号缺失无法运行，改用 MACS3 3.0.4。
- MACS2 2.2.7.1 因与 Python 3.11 冲突，无法安装。

