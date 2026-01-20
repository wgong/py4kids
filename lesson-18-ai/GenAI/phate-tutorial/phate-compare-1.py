import phate
import umap
import pacmap
import trimap
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler

# 1. Load and Scale Data
digits = load_digits()
data = StandardScaler().fit_transform(digits.data) # Scaling helps TriMAP/PHATE
labels = digits.target

# 2. Initialize Embedders
phate_op = phate.PHATE(random_state=42, n_jobs=-1)
umap_op = umap.UMAP(init='pca', n_neighbors=30, random_state=42) # Increased neighbors for global
pacmap_op = pacmap.PaCMAP(n_components=2, random_state=42)
trimap_op = trimap.TRIMAP(n_inliers=12, n_outliers=4, random_state=42)

# 3. Fit and Transform
print("Running PHATE...")
data_phate = phate_op.fit_transform(data)

print("Running UMAP...")
data_umap = umap_op.fit_transform(data)

print("Running PaCMAP...")
data_pacmap = pacmap_op.fit_transform(data)

print("Running TriMAP...")
data_trimap = trimap_op.fit_transform(data)

# 4. Visualization (4 Panels)
fig, axes = plt.subplots(1, 4, figsize=(24, 6))
results = [("PHATE", data_phate), ("UMAP", data_umap), 
           ("PaCMAP", data_pacmap), ("TriMAP", data_trimap)]

for i, (name, coords) in enumerate(results):
    axes[i].scatter(coords[:, 0], coords[:, 1], c=labels, cmap='Spectral', s=5, alpha=0.8)
    axes[i].set_title(name, fontsize=16)
    axes[i].axis('off')

plt.tight_layout()
plt.show()