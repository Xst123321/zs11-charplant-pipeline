# Motif 提取（motif.py）

## 1. 运行 motif.py

```bash
cd /mnt/e/work/zs11_atac/CharPlant/motif
conda activate charplant-cpu

python ../src/motif.py -n1 200 -fl1 19 -o ZS11
```

## 2. 内存问题与修复

原始 motif.py 会把所有 22,848 个数据点的卷积输出累积在 final_output 数组中，峰值内存约 36.5 GB，在 WSL 默认 23 GB 上限下被 OOM Killer 杀掉。 

修复方法：把先全部算完再写文件改成边算边写。每批 128 个样本算完后，立刻对每个 filter 提取序列，追加写入对应的 filter_*.fa 文件。

修改前：

```python
final_output = np.empty([0, 1000, 200])
while y < data.shape[0]:
    x = data[y:y+128]
    cnn_output = f([x])[0]
    y += 128
    final_output = np.concatenate([final_output, cnn_output], axis=0)
```

修改后：

```python
filter_files = [] 
for i in range(int(args.nb_filter1)):
    filter_files.append(open('%s/filter_%s.fa' % ((args.out+"_motif"), i), 'w'))

y = 0
batch_size = 128
while y < int(data.shape[0]):
    x = data[y:y+batch_size]
    cnn_output = f([x])[0]
    for i in range(int(args.nb_filter1)): 
        logo_kmers(cnn_output[:, :, i], filter_size, sequence[y:y+batch_size], filter_files[i], maxpct_t=0.7)
    y += batch_size
```

同时把 logo_kmers 的参数从 filename 改成文件句柄 f，去掉 with open(filename, 'w') as f:。

## 3. 输出

- ZS11_motif/filter_meme.txt：所有 motif 的 PWM 矩阵
- ZS11_motif/filter_*.fa：200 个 filter 的序列文件

