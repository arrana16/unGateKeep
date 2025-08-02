# fashion_clip_with_labels.py

from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import numpy as np

# === 1. Setup device ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Running on device: {device}")

# === 2. Load FashionCLIP Model to GPU ===
model_name = "patrickjohncyh/fashion-clip"
model = CLIPModel.from_pretrained(model_name).to(device)
processor = CLIPProcessor.from_pretrained(model_name)

# === 3. Load and Process the Image ===
image_path = "21832253_51686805_1000.jpg"  # Change this to your image path
image = Image.open(image_path).convert("RGB")
inputs = processor(images=image, return_tensors="pt").to(device)

# === 4. Get Image Embedding ===
with torch.no_grad():
    image_features = model.get_image_features(**inputs)

# Normalize the vector
image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)

# Convert to NumPy array
vector = image_features.cpu().numpy().flatten()

print(f"\n✅ Image Embedding Shape: {vector.shape}")
print(f"➡️ First 10 Embedding Values: {np.round(vector[:10], 4)}\n")

# === 5. Run Zero-Shot Classification (Feature Prediction) ===
# Define possible fashion categories (expand this as you like)
candidate_labels = [
    "baggy jeans", "wide legged jeans", "skinny jeans", "indigo jeans", "dark jeans", "light jeans", "light washed jeans", "skinny, dark jeans", "Jacob Cohen Jeans", "t-shirt", "jacket", "sneakers", "dress", "hoodie", "hat", "sunglasses", "boots", "sweater", "skirt"
]

# Tokenize labels and get text embeddings
text_inputs = processor(text=candidate_labels, return_tensors="pt", padding=True).to(device)

with torch.no_grad():
    text_features = model.get_text_features(**text_inputs)

text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)

# === 6. Compute Cosine Similarity ===
# (CLIP is optimized for cosine similarity between image & text vectors)
cos_sim = torch.matmul(image_features, text_features.T).squeeze(0)

# Convert similarity to a Python list
cos_sim = cos_sim.cpu().numpy()

# === 7. Display Results ===
print("🔍 Model's Feature Predictions (Higher = More Confident):\n")
for label, score in sorted(zip(candidate_labels, cos_sim), key=lambda x: -x[1]):
    print(f"{label:<12}: {score:.4f}")
