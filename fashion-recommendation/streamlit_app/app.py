# import streamlit as st
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import os
# from sklearn.decomposition import PCA

# # -----------------------------
# # 1. 앱 기본 설정
# # -----------------------------
# st.set_page_config(
#     page_title="Fashion Image Embedding Dashboard",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# st.title("Fashion Image Embedding & Similarity Dashboard")
# st.markdown("""
# - ResNet50 기반 TensorFlow / PyTorch 이미지 임베딩 비교
# - 이미지 유사도 및 추천 상품 확인
# """)

# # -----------------------------
# # 2. 데이터 로드
# # -----------------------------
# @st.cache_data
# def load_embeddings(path):
#     return np.load(path)

# @st.cache_data
# def load_metadata(path):
#     return pd.read_csv(path)

# # 현재 파일 위치 기준 상위 폴더 -> embeddings 폴더 경로 설정
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# tf_embeddings_path = os.path.join(BASE_DIR, 'embeddings', 'tf_embeddings.npy')
# torch_embeddings_path = os.path.join(BASE_DIR, 'embeddings', 'torch_embeddings.npy')
# metadata_path = os.path.join(BASE_DIR, 'embeddings', 'torch_metadata.csv')

# tf_embeddings = load_embeddings(tf_embeddings_path)
# torch_embeddings = load_embeddings(torch_embeddings_path)
# metadata = load_metadata(metadata_path)

# # -----------------------------
# # 3. 사이드바 - 상품 선택
# # -----------------------------
# st.sidebar.header("Select a Product to Analyze")

# product_ids = metadata['id'].tolist()
# selected_id = st.sidebar.selectbox("Product ID", product_ids)

# selected_row = metadata[metadata['id'] == selected_id].iloc[0]

# st.sidebar.markdown(f"**Product Name:** {selected_row['productDisplayName']}")
# st.sidebar.markdown(f"**Category:** {selected_row['masterCategory']}")

# # -----------------------------
# # 4. 유사도 계산 함수
# # -----------------------------
# def cosine_similarity(vec1, vec2):
#     norm1 = np.linalg.norm(vec1)
#     norm2 = np.linalg.norm(vec2)
#     if norm1 == 0 or norm2 == 0:
#         return 0.0
#     return np.dot(vec1, vec2) / (norm1 * norm2)

# # -----------------------------
# # 5. 유사 상품 추천
# # -----------------------------
# def get_top_similar(embeddings, index, top_k=5):
#     query_vec = embeddings[index]
#     similarities = [cosine_similarity(query_vec, emb) for emb in embeddings]
#     sim_series = pd.Series(similarities)
#     sim_series.iloc[index] = -1  # 자기 자신 제외
#     top_indices = sim_series.nlargest(top_k).index
#     return top_indices, sim_series[top_indices]

# selected_index = metadata.index[metadata['id'] == selected_id][0]

# # PyTorch 기준 유사 상품
# top_indices, top_sims = get_top_similar(torch_embeddings, selected_index, top_k=5)

# st.header("Selected Product Details")
# st.write(selected_row)

# st.header("Top 5 Similar Products (PyTorch Embeddings)")
# for rank, (idx, sim) in enumerate(zip(top_indices, top_sims), 1):
#     prod = metadata.iloc[idx]
#     st.markdown(f"**{rank}. ID:** {prod['id']}, **Name:** {prod['productDisplayName']}")
#     st.markdown(f"Category: {prod['masterCategory']} | Similarity: {sim:.4f}")
#     st.write("---")

# # -----------------------------
# # 6. 임베딩 분포 시각화 (PCA)
# # -----------------------------
# st.header("Embedding Distribution Visualization")

# pca = PCA(n_components=2)
# reduced_embeddings = pca.fit_transform(torch_embeddings)

# df_vis = pd.DataFrame({
#     'x': reduced_embeddings[:, 0],
#     'y': reduced_embeddings[:, 1],
#     'category': metadata['masterCategory']
# })

# fig, ax = plt.subplots(figsize=(10, 6))
# sns.scatterplot(data=df_vis, x='x', y='y', hue='category', palette='tab10', ax=ax, s=60, alpha=0.7)
# ax.set_title('PCA Projection of PyTorch Embeddings')
# ax.legend(loc='best', fontsize='small')
# st.pyplot(fig)

# # -----------------------------
# # 7. 처리 시간 및 통계 표시
# # -----------------------------
# st.header("Performance Summary")

# tf_time = 61.72
# torch_time = 57.29
# speed_diff = (tf_time - torch_time) / tf_time * 100

# st.write(f"- TensorFlow processing time: {tf_time} seconds")
# st.write(f"- PyTorch processing time: {torch_time} seconds")
# st.write(f"- Speed difference: {speed_diff:.2f}% faster (PyTorch)")

# # -----------------------------
# # 8. 마무리
# # -----------------------------
# st.markdown("---")
# st.markdown("Created by JongHun Lee | Portfolio Project")

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.decomposition import PCA

# -----------------------------
# 1. 기본 설정
# -----------------------------
st.set_page_config(
    page_title="Fashion Embedding Dashboard | TF vs Torch",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title(" Fashion Image Embedding & Similarity Dashboard")
st.caption("ResNet50 기반 TensorFlow / PyTorch 이미지 임베딩 비교 및 추천 분석")

# -----------------------------
# 2. 데이터 로드
# -----------------------------
@st.cache_data
def load_embeddings(path):
    return np.load(path)

@st.cache_data
def load_metadata(path):
    return pd.read_csv(path)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMB_DIR = os.path.join(BASE_DIR, "..", "embeddings")
paths = {
    "tf": os.path.join(EMB_DIR, "tf_embeddings.npy"),
    "torch": os.path.join(EMB_DIR, "torch_embeddings.npy"),
    "meta": os.path.join(EMB_DIR, "torch_metadata.csv")
}

tf_emb = load_embeddings(paths["tf"])
torch_emb = load_embeddings(paths["torch"])
meta = load_metadata(paths["meta"])

# -----------------------------
# 3. 사이드바
# -----------------------------
st.sidebar.header(" 설정")
framework = st.sidebar.radio("임베딩 프레임워크", ["PyTorch", "TensorFlow"])
product_ids = meta["id"].tolist()
selected_id = st.sidebar.selectbox("상품 ID", product_ids)
top_k = st.sidebar.slider("추천 상품 수", 1, 10, 5)

selected_idx = meta.index[meta["id"] == selected_id][0]
selected_row = meta.iloc[selected_idx]

st.sidebar.markdown(f"**상품명:** {selected_row['productDisplayName']}")
st.sidebar.markdown(f"**카테고리:** {selected_row['masterCategory']}")

# -----------------------------
# 4. 유사도 계산
# -----------------------------
def cosine_sim(a, b):
    n1, n2 = np.linalg.norm(a), np.linalg.norm(b)
    return np.dot(a, b) / (n1 * n2 + 1e-8)

def top_similar(emb, idx, k=5):
    q = emb[idx]
    sims = np.dot(emb, q) / (np.linalg.norm(emb, axis=1) * np.linalg.norm(q) + 1e-8)
    sims[idx] = -1
    top_idx = np.argsort(sims)[::-1][:k]
    return top_idx, sims[top_idx]

embeddings = torch_emb if framework == "PyTorch" else tf_emb
top_idx, top_sims = top_similar(embeddings, selected_idx, top_k)

# -----------------------------
# 5. 섹션: 추천 결과
# -----------------------------
st.header(f" Top {top_k} Similar Products ({framework} Embeddings)")

for rank, (idx, sim) in enumerate(zip(top_idx, top_sims), 1):
    prod = meta.iloc[idx]
    st.markdown(f"**{rank}. {prod['productDisplayName']}**")
    st.write(f"ID: {prod['id']} | Category: {prod['masterCategory']} | Similarity: {sim:.4f}")
    st.divider()

# -----------------------------
# 6. 임베딩 시각화 (PCA)
# -----------------------------
st.header(" Embedding Distribution (PCA 2D)")
pca = PCA(n_components=2, random_state=42)
reduced = pca.fit_transform(embeddings)
df_vis = pd.DataFrame({
    "x": reduced[:, 0],
    "y": reduced[:, 1],
    "cat": meta["masterCategory"]
})

fig, ax = plt.subplots(figsize=(9, 6))
sns.scatterplot(data=df_vis, x="x", y="y", hue="cat", s=50, alpha=0.7, palette="tab10", ax=ax)
ax.set_title(f"PCA Projection ({framework})", fontsize=13)
st.pyplot(fig)

# -----------------------------
# 7. 성능 비교
# -----------------------------
st.header(" Performance Summary")

tf_time, torch_time = 61.72, 57.29
speed_diff = (tf_time - torch_time) / tf_time * 100

col1, col2, col3 = st.columns(3)
col1.metric("TensorFlow (sec)", f"{tf_time:.2f}")
col2.metric("PyTorch (sec)", f"{torch_time:.2f}")
col3.metric("Speed Gain", f"{speed_diff:.1f}% faster")

# -----------------------------
# 8. insight
# -----------------------------
st.markdown("###  분석 인사이트")
st.markdown("""
- PyTorch가 약 7% 빠른 처리 효율을 보임  
- 두 모델의 임베딩 분포는 유사하지만, **상관 구조는 거의 독립적**  
- 동일 모델 구조라도 프레임워크 차이에 따라 **추천 결과가 달라질 수 있음**
- 향후 광고 CTR 모델이나 추천 알고리즘에서 **임베딩 품질 검증** 실험 설계 가능
""")

# -----------------------------
# 9. footer
# -----------------------------
st.markdown("---")
st.caption("Created by JongHun Lee | Data Analytics Portfolio")
