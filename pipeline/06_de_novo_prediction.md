# 从头预测（de_novo_prediction.py）

## 1. 步长选择

CharPlant 原始代码中滑动窗口步长硬编码为 1bp，全基因组会产生约 10 亿个窗口。为评估步长对预测结果的影响，将步长改为 10bp 做对比测试。

```bash
cp /mnt/e/work/zs11_atac/CharPlant/src/de_novo_prediction.py /mnt/e/work/zs11_atac/CharPlant/src/de_novo_prediction_10bp.py
nano /mnt/e/work/zs11_atac/CharPlant/src/de_novo_prediction_10bp.py
```

把 for i in range(0, len_chrom[key], 1): 改成 for i in range(0, len_chrom[key], 10):。

## 2. Scaffold 测试（scaffoldA04）

```bash
cd /mnt/e/work/zs11_atac/CharPlant/de_novo_prediction

python ../src/de_novo_prediction_10bp.py -g /tmp/scaffoldA04.fa -l 20000 -t 0.5 -o split_A04_10bp_
```

生成 129 个预测脚本，批量跑完后合并、转 BED、算召回率。

结果：

| 指标 | 数值 |
|:---|:---|
| A04 上的实验 OCR 总数 | 491 |
| 被预测覆盖的实验 OCR | 470 |
| 召回率 | 95.7% |
| 预测 OCR 总数(合并后) | 219,937 |

## 3. A 亚基因组预测

```bash
conda activate atac
samtools faidx /mnt/e/work/zs11_atac/genome/Brassica_napus.ZS11.v0.genome.fa scaffoldA01 scaffoldA02 scaffoldA03 scaffoldA04 scaffoldA05 scaffoldA06 scaffoldA07 scaffoldA08 scaffoldA09 scaffoldA10 > /tmp/A_subgenome.fa
conda activate charplant-cpu

cd /mnt/e/work/zs11_atac/CharPlant/de_novo_prediction
python ../src/de_novo_prediction_10bp.py -g /tmp/A_subgenome.fa -l 20000 -t 0.5 -o split_A_10bp_
```

生成 1962 个预测脚本，用断点续跑方式批量执行：

```bash
nohup bash -c 'for f in split_A_10bp_*.py; do output="whole_predict_fasta${f%.py}.txt"; if [ -f "$output" ]; then echo "Skipping $f"; continue; fi; echo "Running $f..."; python $f; done' > run_A_10bp.log 2>&1 &
```

结果：A 亚基因组 1962 个脚本全部完成，预测 OCR 已生成，与 C 亚基因组统一合并后同意评估。

## 4. C 亚基因组预测

```bash
conda activate atac
samtools faidx /mnt/e/work/zs11_atac/genome/Brassica_napus.ZS11.v0.genome.fa scaffoldC01 
scaffoldC02 scaffoldC03 scaffoldC04 scaffoldC05 scaffoldC06 scaffoldC07 scaffoldC08 scaffoldC09 > /tmp/C_subgenome.fa conda 

activate charplant-cpu
cd /mnt/e/work/zs11_atac/CharPlant/de_novo_prediction python ../src/de_novo_prediction_10bp.py -g 
/tmp/C_subgenome.fa -l 20000 -t 0.5 -o split_C_10bp_ 
```

生成 2843 个预测脚本，用断点续跑方式批量执行。

结果：C 亚基因组 2843 个脚本全部完成。

## 5. 全基因组合并与评估

```bash
cat whole_predict_fastasplit_A_10bp_*.txt whole_predict_fastasplit_C_10bp_*.txt > all_AC_10bp_predict.txt
cp split_A_10bp_ all_AC_10bp_windows.txt
cat split_C_10bp_ >> all_AC_10bp_windows.txt

paste all_AC_10bp_predict.txt all_AC_10bp_windows.txt | \
  awk -F'\t' '$1=="[1]" {print $2"\t"$3"\t"$4}' > AC_10bp_predicted_ocr.bed

conda activate atac
sort -k1,1 -k2,2n AC_10bp_predicted_ocr.bed | bedtools merge -i - > AC_10bp_predicted_ocr_merged.bed
```

全基因组召回率：18,247 / 19,041 = 95.8%。

