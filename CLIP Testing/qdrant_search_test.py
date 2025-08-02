# search_qdrant.py

from qdrant_client import QdrantClient
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

# === 1. Qdrant Setup ===
client = QdrantClient(url = "https://0cc61245-df68-40da-a18e-67cc0df1d4f1.us-east-1-0.aws.cloud.qdrant.io", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.P7toB5RD6MBk6py4qQp9bUeyin-ePiiCxKtH7x2xoFY")  # Or your Qdrant Cloud host
collection_name = "fashion-demo"

# === 2. Load FashionCLIP ===
model_name = "patrickjohncyh/fashion-clip"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CLIPModel.from_pretrained(model_name).to(device)
processor = CLIPProcessor.from_pretrained(model_name)

# === 3. Load & Embed the Image 
image = Image.open("Acne Jeans 2.jpg").convert("RGB")

inputs = processor(images=image, return_tensors="pt").to(device)

with torch.no_grad():
    image_features = model.get_image_features(**inputs)

# Normalize
image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
query_vector = image_features.cpu().numpy().flatten()

# === 4. Search Qdrant ===
search_results = client.search(
    collection_name=collection_name,
    query_vector=query_vector.tolist(),
    limit=5
)

# === 5. Print Results ===
print("\n✅ Top Results:\n")
for result in search_results:
    print(f"ID: {result.id}")
    print(f"Score: {result.score:.4f}")
    print(f"Brand: {result.payload.get('brand')}")
    print(f"Category: {result.payload.get('category')}")
    print(f"Description: {result.payload.get('description')}\n")
