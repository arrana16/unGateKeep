from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance, CollectionStatus
from transformers import CLIPProcessor, CLIPModel
import torch

# === 1. Initialize Qdrant Client ===
client = QdrantClient(url = "https://0cc61245-df68-40da-a18e-67cc0df1d4f1.us-east-1-0.aws.cloud.qdrant.io", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.P7toB5RD6MBk6py4qQp9bUeyin-ePiiCxKtH7x2xoFY")  # Or your Qdrant Cloud host

collection_name = "fashion-demo"

# === 2. Create Collection if not exists ===
if collection_name not in [c.name for c in client.get_collections().collections]:
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=512, distance=Distance.COSINE)
    )
    print(f"✅ Created collection '{collection_name}'")

# === 3. Initialize FashionCLIP ===
model_name = "patrickjohncyh/fashion-clip"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CLIPModel.from_pretrained(model_name).to(device)
processor = CLIPProcessor.from_pretrained(model_name)

# === 4. Sample Dataset ===
sample_items = [
    # (0, "Jacob Cohen skinny-leg logo-patch jeans, dark blue denim", "Jacob Cohen", "jeans"),
    # (1, "Levi's 511 slim-fit jeans, classic indigo wash", "Levi's", "jeans"),
    # (2, "Balenciaga distressed black skinny jeans", "Balenciaga", "jeans"),
    # (3, "Diesel tapered-fit faded grey jeans", "Diesel", "jeans"),
    # (4, "Gucci straight-leg vintage-wash blue jeans", "Gucci", "jeans"),
    # (5, "Prada light blue slim-fit denim jeans", "Prada", "jeans"),
    # (6, "Rag & Bone dark wash straight-fit jeans", "Rag & Bone", "jeans"),
    # (7, "Calvin Klein mid-rise slim blue jeans", "Calvin Klein", "jeans"),
    # (8, "Saint Laurent ripped skinny-leg black jeans", "Saint Laurent", "jeans"),
    # (9, "Off-White painter print slim-fit jeans", "Off-White", "jeans"),

    # # JACKETS
    # (10, "The North Face puffer down jacket, black", "The North Face", "jacket"),
    # (11, "Canada Goose Expedition Parka, arctic navy", "Canada Goose", "jacket"),
    # (12, "Moncler quilted down bomber jacket, dark green", "Moncler", "jacket"),
    # (13, "Nike Windrunner lightweight jacket, grey", "Nike", "jacket"),
    # (14, "Zara faux-leather biker jacket, black", "Zara", "jacket"),

    # # T-SHIRTS
    # (15, "Supreme box logo cotton t-shirt, white", "Supreme", "t-shirt"),
    # (16, "Balenciaga oversized cotton jersey t-shirt, black", "Balenciaga", "t-shirt"),
    # (17, "Uniqlo dry-fit crew neck t-shirt, grey", "Uniqlo", "t-shirt"),
    # (18, "H&M basic slim fit t-shirt, navy", "H&M", "t-shirt"),
    # (19, "Off-White arrows print slim-fit t-shirt, black", "Off-White", "t-shirt"),

    # # SHOES
    # (20, "Nike Air Force 1 low-top sneakers, white", "Nike", "shoes"),
    # (21, "Adidas Yeezy Boost 350 v2, black/red", "Adidas", "shoes"),
    # (22, "Common Projects Achilles low sneakers, white leather", "Common Projects", "shoes"),
    # (23, "Balenciaga Triple S chunky sneakers, grey", "Balenciaga", "shoes"),
    # (24, "Converse Chuck Taylor All Star high-tops, black", "Converse", "shoes"),

    # # HOODIES
    # (25, "Champion reverse weave hoodie, grey", "Champion", "hoodie"),
    # (26, "Fear of God Essentials oversized hoodie, cream", "Fear of God", "hoodie"),
    # (27, "Nike Tech Fleece full-zip hoodie, black", "Nike", "hoodie"),
    # (28, "Gucci embroidered logo hoodie, red", "Gucci", "hoodie"),
    # (29, "H&M basic pullover hoodie, navy", "H&M", "hoodie"),

    # (30, "Levi's 502 regular tapered jeans, mid blue wash", "Levi's", "jeans"),
    # (31, "Levi's 505 straight fit jeans, dark indigo", "Levi's", "jeans"),
    # (32, "Diesel Sleenker skinny-fit faded blue jeans", "Diesel", "jeans"),
    # (33, "Diesel D-Strukt slim-fit grey stretch jeans", "Diesel", "jeans"),
    # (34, "Wrangler regular fit stonewash jeans", "Wrangler", "jeans"),
    # (35, "Lee relaxed fit black jeans, comfort stretch", "Lee", "jeans"),
    # (36, "Acne Studios slim fit raw denim jeans", "Acne Studios", "jeans"),
    # (37, "A.P.C. New Standard straight-leg raw indigo jeans", "A.P.C.", "jeans"),
    # (38, "Rag & Bone Fit 2 slim-fit faded indigo jeans", "Rag & Bone", "jeans"),
    # (39, "Balmain biker-style distressed skinny jeans, black", "Balmain", "jeans"),
    # (40, "Tommy Hilfiger regular fit blue jeans with logo patch", "Tommy Hilfiger", "jeans"),
    # (41, "Calvin Klein slim tapered stonewash blue jeans", "Calvin Klein", "jeans"),
    # (42, "Guess mid-rise skinny jeans, vintage wash", "Guess", "jeans"),
    # (43, "Jack & Jones Glenn slim fit dark blue jeans", "Jack & Jones", "jeans"),
    # (44, "Replay Hyperflex skinny-fit stretch jeans, faded black", "Replay", "jeans"),
    # (45, "Uniqlo relaxed fit light-wash jeans, casual style", "Uniqlo", "jeans"),
    # (46, "H&M skinny fit stretch jeans, medium blue", "H&M", "jeans"),
    # (47, "Zara slim ripped washed grey jeans", "Zara", "jeans"),
    # (48, "Pepe Jeans London slim fit mid-wash jeans", "Pepe Jeans", "jeans"),
    # (49, "Pull & Bear slim dark-wash casual jeans", "Pull & Bear", "jeans"),


    # (50, "Carhartt WIP baggy fit work jeans, dark rinse", "Carhartt WIP", "jeans"),
    # (51, "Dickies relaxed baggy fit carpenter jeans, stonewash blue", "Dickies", "jeans"),
    # (52, "Stüssy loose fit baggy jeans, faded black", "Stüssy", "jeans"),
    # (53, "Tommy Jeans 90s baggy fit denim jeans, light wash", "Tommy Jeans", "jeans"),
    # (54, "ASOS Design super baggy jeans, vintage blue", "ASOS Design", "jeans"),
    # (55, "Zara wide-leg baggy jeans, bleach wash", "Zara", "jeans"),
    # (56, "H&M relaxed baggy fit jeans, mid-wash blue", "H&M", "jeans"),
    # (57, "Pull & Bear extreme baggy jeans, washed grey", "Pull & Bear", "jeans"),
    # (58, "Urban Outfitters oversized baggy straight jeans, light blue", "Urban Outfitters", "jeans"),
    # (59, "Uniqlo loose tapered baggy jeans, navy denim", "Uniqlo", "jeans"),
    # (60, "Levi's Silver Tab loose fit baggy jeans, dark indigo", "Levi's", "jeans"),
    # (61, "Wrangler 90s relaxed baggy jeans, stone grey", "Wrangler", "jeans"),
    # (62, "Weekday Voyage wide baggy jeans, washed black", "Weekday", "jeans"),
    # (63, "Noah NYC baggy straight fit jeans, raw denim", "Noah NYC", "jeans"),
    # (64, "Everlane relaxed baggy fit organic denim jeans, faded indigo", "Everlane", "jeans"),

    # (65, "Acne Studios 1991 Toj slim-fit raw indigo jeans", "Acne Studios", "jeans"),
    # (66, "Acne Studios North slim-fit faded grey jeans", "Acne Studios", "jeans"),
    # (67, "Acne Studios River relaxed straight-leg blue jeans", "Acne Studios", "jeans"),
    # (68, "Acne Studios Peg loose-fit baggy jeans, light wash", "Acne Studios", "jeans"),
    # (69, "Acne Studios 2021 skinny-leg washed black jeans", "Acne Studios", "jeans"),
    # (70, "Acne Studios Climb mid-rise skinny-fit stretch jeans, dark navy", "Acne Studios", "jeans"),
    # (71, "Acne Studios Mece tapered-leg washed blue jeans", "Acne Studios", "jeans"),
    # (72, "Acne Studios Land relaxed straight-fit black jeans", "Acne Studios", "jeans"),
    # (73, "Acne Studios Roc regular fit stonewash jeans", "Acne Studios", "jeans"),
    # (74, "Acne Studios Ex baggy fit ripped blue jeans", "Acne Studios", "jeans"),
    # (75, "Acne Studios North slim faded stone grey jeans", "Acne Studios", "jeans"),
    # (76, "Acne Studios 2003 straight-leg raw blue jeans", "Acne Studios", "jeans"),
    # (77, "Acne Studios Taper loose tapered-fit light indigo jeans", "Acne Studios", "jeans"),
    # (78, "Acne Studios Baggy oversized fit jeans, medium wash", "Acne Studios", "jeans"),
    # (79, "Acne Studios North power stretch slim jeans, deep indigo", "Acne Studios", "jeans"),

    # (80, "Acne Studios Extreme Baggy wide-leg jeans, light blue", "Acne Studios", "jeans"),
    # (81, "Acne Studios Super Baggy oversized faded black jeans", "Acne Studios", "jeans"),
    # (82, "Acne Studios Wide Baggy loose fit distressed jeans, stonewash blue", "Acne Studios", "jeans"),
    # (83, "Acne Studios Extra Baggy relaxed wide-leg jeans, vintage wash", "Acne Studios", "jeans"),
    # (84, "Acne Studios Super Wide straight-leg baggy jeans, dark indigo", "Acne Studios", "jeans"),
    # (85, "Acne Studios Oversized Baggy fit raw denim jeans, navy", "Acne Studios", "jeans"),
    # (86, "Acne Studios Extreme Oversized baggy jeans, acid wash", "Acne Studios", "jeans"),
    # (87, "Acne Studios Relaxed Wide-Leg baggy jeans, faded grey", "Acne Studios", "jeans"),
    # (88, "Acne Studios Loose super baggy straight jeans, off-white", "Acne Studios", "jeans"),
    # (89, "Acne Studios 2023 super baggy fit jeanss", "Acne Studios", "jeans"),
    # (90, "Acne Studios 2023 super baggy fit jeans ", "Acne Studios", "jeans"),
    (91, "Acne Studios 2023 super baggy fit jeans light blue, cotton, denim, light wash, faded effect, mid-rise, belt loops, front button fastening, classic five pockets, wide leg", "Acne Studios", "jeans"),




]

# === 5. Embed and Insert into Qdrant ===
points = []
for item_id, text, brand, category in sample_items:
    print(f"Embedding: {text}")
    inputs = processor(text=[text], return_tensors="pt").to(device)

    with torch.no_grad():
        text_features = model.get_text_features(**inputs)

    # Normalize
    text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)
    vector = text_features.cpu().numpy().flatten()

    points.append(
        PointStruct(
            id=item_id,
            vector=vector.tolist(),
            payload={"brand": brand, "category": category, "description": text}
        )
    )

client.upsert(
    collection_name=collection_name,
    points=points,
)

print(f"\n✅ Inserted {len(points)} items into Qdrant collection '{collection_name}'.")
