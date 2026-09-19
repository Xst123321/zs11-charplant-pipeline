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

（待跑完后补充结果）


