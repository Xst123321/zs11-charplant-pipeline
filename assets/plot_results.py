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
