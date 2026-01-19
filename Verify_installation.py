# verify_installation.py
import sys

def test_imports():
    """Test all critical package imports"""
    
    results = []
    
    # Test 1: Python version
    print(f"Python Version: {sys.version}")
    print("-" * 60)
    
    packages = [
        # Core Framework
        ("llama_index", "LlamaIndex Core"),
        ("llama_index.embeddings.openai", "LlamaIndex OpenAI Embeddings"),
        ("llama_index.llms.openai", "LlamaIndex OpenAI LLM"),
        ("llama_index.vector_stores.qdrant", "LlamaIndex Qdrant"),
        
        # Vector Database
        ("qdrant_client", "Qdrant Client"),
        
        # PDF Processing
        ("pypdf", "PyPDF"),
        ("fitz", "PyMuPDF (fitz)"),
        ("pdfplumber", "PDF Plumber"),
        
        # Text Processing
        ("sentence_transformers", "Sentence Transformers"),
        ("nltk", "NLTK"),
        
        # OpenAI
        ("openai", "OpenAI"),
        
        # Async
        ("aiohttp", "AioHTTP"),
        
        # Rate Limiting & Caching
        ("tenacity", "Tenacity"),
        ("diskcache", "DiskCache"),
        
        # Streamlit
        ("streamlit", "Streamlit"),
        ("plotly", "Plotly"),
        ("pandas", "Pandas"),
        
        # Configuration
        ("dotenv", "Python Dotenv"),
        ("loguru", "Loguru"),
        ("pydantic", "Pydantic"),
        
        # Testing
        ("pytest", "Pytest"),
        
        # Utilities
        ("dateutil", "Python DateUtil"),
        ("tqdm", "TQDM"),
    ]
    
    print("Package Import Tests:")
    print("-" * 60)
    
    for module_name, display_name in packages:
        try:
            module = __import__(module_name)
            version = getattr(module, "__version__", "unknown")
            print(f"✅ {display_name:<35} v{version}")
            results.append((display_name, True, version))
        except ImportError as e:
            print(f"❌ {display_name:<35} MISSING")
            results.append((display_name, False, str(e)))
    
    print("-" * 60)
    
    # Summary
    passed = sum(1 for _, status, _ in results if status)
    total = len(results)
    
    print(f"\n{'='*60}")
    print(f"Results: {passed}/{total} packages installed successfully")
    print(f"{'='*60}")
    
    if passed == total:
        print("🎉 ALL PACKAGES INSTALLED CORRECTLY!")
        return True
    else:
        print("⚠️  Some packages are missing. Review errors above.")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)