# 图一：召回率对比图
import matplotlib.pyplot as plt
# 数据
labels = ['scaffoldA04\n(10bp)', '全基因组\n(10bp)']
recall = [95.7, 95.8]
colors = ['#4C72B0', '#DD8452']
fig, ax = plt.subplots(figsize=(6, 5))
bars = ax.bar(labels, recall, color=colors, width=0.5)
# 在柱子上标数值
for bar, val in zip(bars, recall):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
ax.set_ylabel('Recall (%)', fontsize=12)
ax.set_title('CharPlant OCR Prediction Recall', fontsize=14, fontweight='bold')
ax.set_ylim(0, 105)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('recall_comparison.png', dpi=300)
plt.show()

# 图二：预测 vs 实验 OCR 数量对比图
import matplotlib.pyplot as plt
# 数据
labels = ['实验 OCR\n(ATAC-seq)', '预测 OCR\n(CharPlant)']
counts = [19041, 8348361]
colors = ['#55A868', '#C44E52']
fig, ax = plt.subplots(figsize=(6, 5))
bars = ax.bar(labels, counts, color=colors, width=0.5)
# 对数坐标
ax.set_yscale('log')
ax.set_ylabel('Number of OCR regions (log scale)', fontsize=12)
ax.set_title('Experimental vs Predicted OCR Counts', fontsize=14, fontweight='bold')
# 标数值
for bar, val in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.2,
            f'{val:,}', ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('ocr_count_comparison.png', dpi=300)
plt.show()

# 图三：A/C 亚基因组预测脚本数对比图
import matplotlib.pyplot as plt
labels = ['A 亚基因组', 'C 亚基因组']
scripts = [1962, 2843]
colors = ['#4C72B0', '#DD8452']
fig, ax = plt.subplots(figsize=(6, 5))
bars = ax.bar(labels, scripts, color=colors, width=0.5)
for bar, val in zip(bars, scripts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
            f'{val}', ha='center', va='bottom', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of prediction scripts', fontsize=12)
ax.set_title('A/C Subgenome Prediction Scale', fontsize=14, fontweight='bold')
ax.set_ylim(0, 3200)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('subgenome_scripts.png', dpi=300)
plt.show()

# 图四：比对率与去重率对比图
import matplotlib.pyplot as plt
import numpy as np
samples = ['SRR17036599', 'SRR17036598']
alignment = [88.13, 89.90]
properly_paired = [75.38, 77.06]
duplication = [24.8, 19.6]
x = np.arange(len(samples))
width = 0.25
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(x - width, alignment, width, label='Alignment rate', color='#4C72B0')
ax.bar(x, properly_paired, width, label='Properly paired', color='#55A868')
ax.bar(x + width, duplication, width, label='Duplication rate', color='#C44E52')
ax.set_ylabel('Percentage (%)', fontsize=12)
ax.set_title('ATAC-seq Quality Metrics', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(samples)
ax.legend()
ax.set_ylim(0, 100)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('qc_metrics.png', dpi=300)
plt.show()

# 图五：模型训练曲线
import matplotlib.pyplot as plt
import re
# 从日志里提取每轮数据
epochs, train_loss, val_loss, train_acc, val_acc = [], [], [], [], []
current_epoch = None

with open('/mnt/e/work/zs11_atac/CharPlant/model/training_log.txt') as f:
    for line in f:
        m = re.search(r'Epoch (\d+)/', line)
        if m:
            current_epoch = int(m.group(1))
            continue
        loss_m = re.search(r'loss: ([\d.]+) - acc: ([\d.]+) - val_loss: ([\d.]+) - val_acc: ([\d.]+)', line)
        if loss_m and current_epoch is not None:
            epochs.append(current_epoch)
            train_loss.append(float(loss_m.group(1)))
            train_acc.append(float(loss_m.group(2)))
            val_loss.append(float(loss_m.group(3)))
            val_acc.append(float(loss_m.group(4)))
            current_epoch = None

print(f'提取到 {len(epochs)} 轮数据')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(epochs, train_loss, '-', label='Train loss', color='#4C72B0')
ax1.plot(epochs, val_loss, '-', label='Val loss', color='#DD8452')
ax1.set_xlabel('Epoch', fontsize=12)
ax1.set_ylabel('Loss', fontsize=12)
ax1.set_title('Training and Validation Loss', fontsize=14, fontweight='bold')
ax1.legend()
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

ax2.plot(epochs, train_acc, '-', label='Train acc', color='#4C72B0')
ax2.plot(epochs, val_acc, '-', label='Val acc', color='#DD8452')
ax2.set_xlabel('Epoch', fontsize=12)
ax2.set_ylabel('Accuracy', fontsize=12)
ax2.set_title('Training and Validation Accuracy', fontsize=14, fontweight='bold')
ax2.legend()
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('training_curves.png', dpi=300)
plt.show()


# 图六：全基因组预测 OCR 的染色体分布
import matplotlib.pyplot as plt
# 从 AC_10bp_predicted_ocr_merged.bed 里统计各染色体的预测 OCR 数量 你需要先跑这条命令： cut -f1
# AC_10bp_predicted_ocr_merged.bed | sort | uniq -c | sort -rn > chr_ocr_counts.txt 假设你已经生成了 chr_ocr_counts.txt
chroms = []
counts = []
with open('chr_ocr_counts.txt') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 2:
            counts.append(int(parts[0]))
            chroms.append(parts[1])
# 只画前 20 条
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(chroms[:20], counts[:20], color='#4C72B0')
ax.set_xlabel('Chromosome', fontsize=12)
ax.set_ylabel('Number of predicted OCR', fontsize=12)
ax.set_title('Predicted OCR Distribution across Chromosomes', fontsize=14, fontweight='bold')
ax.tick_params(axis='x', rotation=45)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('chr_ocr_distribution.png', dpi=300)
plt.show()
