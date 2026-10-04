import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY", "")

print("Testing Gemini API Key:", api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else api_key)

try:
    client = genai.Client(api_key=api_key)
    
    # 1. Test Embedding API
    emb_res = client.models.embed_content(
        model="text-embedding-004",
        contents="Photosynthesis in plants"
    )
    print("1. Embedding API Success! Vector length:", len(emb_res.embedding.values))

    # 2. Test Generation API
    gen_res = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Explain quantum mechanics in 1 short sentence."
    )
    print("2. Generation API Success! Response:", gen_res.text)

except Exception as e:
    print("❌ Gemini API Error:", type(e).__name__, "-", e)
