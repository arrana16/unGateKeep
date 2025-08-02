# app.py

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from qdrant_client import QdrantClient
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import io

app = FastAPI()

# === Qdrant Setup ===
client = QdrantClient(url = URL, api_key=KEY)  # Or your Qdrant Cloud host
collection_name = "fashion-demo"

# === Load FashionCLIP ===
model_name = "patrickjohncyh/fashion-clip"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CLIPModel.from_pretrained(model_name).to(device)
processor = CLIPProcessor.from_pretrained(model_name)

@app.post("/search-image/")
async def search_image(file: UploadFile = File(...), top_k: int = 5):
    try:
        # === 1. Load image from uploaded file ===
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        # === 2. Generate image embedding ===
        inputs = processor(images=image, return_tensors="pt").to(device)

        with torch.no_grad():
            image_features = model.get_image_features(**inputs)

        image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
        query_vector = image_features.cpu().numpy().flatten().tolist()

        # === 3. Query Qdrant ===
        search_results = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k
        )

        # === 4. Format results ===
        results = []
        for result in search_results:
            results.append({
                "id": result.id,
                "score": round(result.score, 4),
                "brand": result.payload.get("brand"),
                "category": result.payload.get("category"),
                "description": result.payload.get("description")
            })

        return JSONResponse(content={"results": results}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.get("/")
def read_root():
    return {"message": "Welcome to the Fashion Image Search API. Use POST /search-image to search for fashion items by image."}
