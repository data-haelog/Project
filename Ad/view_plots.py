import os
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

plots_dir = 'output/plots'
plot_files = sorted([f for f in os.listdir(plots_dir) if f.endswith('.png')])

print(f"생성된 그래프 {len(plot_files)}개:")
for i, file in enumerate(plot_files, 1):
    print(f"{i}. {file}")

cols = 2  
rows = math.ceil(len(plot_files) / cols)

fig, axes = plt.subplots(rows, cols, figsize=(16, rows * 6))
axes = axes.flatten()

for idx, file in enumerate(plot_files):
    img = mpimg.imread(os.path.join(plots_dir, file))
    axes[idx].imshow(img, aspect='auto')
    axes[idx].set_title(file, fontsize=10)
    axes[idx].axis('off')


for idx in range(len(plot_files), len(axes)):
    axes[idx].axis('off')

plt.tight_layout()
plt.show()
