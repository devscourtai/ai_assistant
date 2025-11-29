"""
Download required NLTK data for document processing.
Run this once to set up NLTK resources.
"""
import nltk

print("📥 Downloading required NLTK data...")

# Download punkt_tab tokenizer
try:
    nltk.download('punkt_tab')
    print("✅ punkt_tab downloaded successfully")
except Exception as e:
    print(f"⚠️  Error downloading punkt_tab: {e}")

# Download punkt (legacy, for compatibility)
try:
    nltk.download('punkt')
    print("✅ punkt downloaded successfully")
except Exception as e:
    print(f"⚠️  Error downloading punkt: {e}")

# Download averaged_perceptron_tagger (often needed by unstructured)
try:
    nltk.download('averaged_perceptron_tagger')
    print("✅ averaged_perceptron_tagger downloaded successfully")
except Exception as e:
    print(f"⚠️  Error downloading averaged_perceptron_tagger: {e}")

print("\n✨ NLTK data download complete!")
print("You can now upload documents.")
