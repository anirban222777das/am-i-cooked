import os
import sys
from huggingface_hub import snapshot_download

MODEL_ID = "Qwen/Qwen3-4B-Instruct-2507"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIR = os.path.join(BASE_DIR, "models", "qwen3-4b")

def download_model():
    print(f"Starting download of {MODEL_ID} to {TARGET_DIR}...")
    
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    try:
        # Download the model files (excluding heavy safetensors if using MLX, but for 4B we download all)
        path = snapshot_download(
            repo_id=MODEL_ID,
            local_dir=TARGET_DIR,
            local_dir_use_symlinks=False,
            ignore_patterns=["*.msgpack", "*.h5", "*.ot"]
        )
        print("\n✅ Download completed successfully!")
        print(f"Model physically stored at: {path}")
        
        # Verify essential files
        files = os.listdir(path)
        if not any(f.endswith(".safetensors") for f in files) or "config.json" not in files:
            raise ValueError("Missing critical model files (safetensors or config.json)")
            
        print("Model verification passed.")
        
    except Exception as e:
        print(f"\n❌ Error downloading model: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_model()
