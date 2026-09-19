# 模型训练（CharPlant）

## 1. 下载 CharPlant

```bash
cd /mnt/e/work/zs11_atac

git clone https://github.com/Yin-Shen/CharPlant.git

cd CharPlant
```

## 2. 配置config.yaml

```yaml
genome : /mnt/e/work/zs11_atac/genome/Brassica_napus.ZS11.v0.genome.fa
bed : /mnt/e/work/zs11_atac/bed/zs11_merged_ocr.bed
out : zs11

epochs : 150 
patience : 20
learningrate : 0.001
batch_size : 256
dropout : 0.6
nb_filter1 : 200
nb_filter2 : 100
filter_len1 : 19
filter_len2 : 11
hidden : 200 

motif_out : ZS11 
prediction_out : split_fasta_36_1_
split_lines : 20000
threshold : 0.5

run_type : local
batch_submit_jobs_number : 80

speices_name : Brassica_napus
index_name : /mnt/e/work/zs11_atac/genome/zs11_index
sam_prefix : whole_fasta_36_1
peak_prefix : Brassica_napus
```

## 3. 数据预处理

```bash
cd /mnt/e/work/zs11_atac/CharPlant
conda activate charplant-cpu

mkdir -p data_preprocessing
cd data_preprocessing
python ../src/data_preprocess.py -g /mnt/e/work/zs11_atac/genome/Brassica_napus.ZS11.v0.genome.fa -b /mnt/e/work/zs11_atac/bed/zs11_merged_ocr.bed -o zs11
```

## 4. 模型训练

```bash
cd /mnt/e/work/zs11_atac/CharPlant/model
conda activate charplant-cpu

python ../src/model.py -e 150 -p 20 -lr 0.001 -b 256 -d 0.6 -n1 200 -n2 100 -fl1 19 -fl2 11 -hd 200
```

## 5. 训练结果

- 训练轮数：150
- 验证集最优 val_loss：0.1933（第 148 轮）
- 验证集最优 val_acc：92.36%
- 最终模型权重：model_weights200-100-19-11-200-0.6-0.001-256-150-20.h5
