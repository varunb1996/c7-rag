"""Run me once before starting: python check_setup.py

Verifies your environment so that every later failure is a *scheduled* failure,
not a broken install.
"""
import os
import sys


def ok(msg):
    print(f"  ✅ {msg}")


def bad(msg):
    print(f"  ❌ {msg}")
    return False


def main():
    good = True
    print("Checking environment...\n")

    if sys.version_info < (3, 9):
        good = bad(f"Python 3.9+ required, you have {sys.version.split()[0]}")
    else:
        ok(f"Python {sys.version.split()[0]}")

    for lib in ("groq", "requests", "numpy", "sentence_transformers", "tiktoken"):
        try:
            __import__(lib)
            ok(f"import {lib}")
        except ImportError:
            good = bad(f"missing library: {lib}  (pip install -r requirements.txt)")

    if os.environ.get("GROQ_API_KEY", "").startswith("gsk_"):
        ok("GROQ_API_KEY is set")
    else:
        good = bad('GROQ_API_KEY not set  (export GROQ_API_KEY="gsk_...")')

    try:
        import tiktoken

        enc = tiktoken.get_encoding("cl100k_base")
        n = len(enc.encode("retrieval augmented generation"))
        ok(f"tiktoken works ({n} tokens in 'retrieval augmented generation')")
    except Exception as e:
        good = bad(f"tiktoken failed: {e}")

    if "--download-model" in sys.argv:
        print("\nDownloading the embedding model for Module 2 (~90 MB, one time)...")
        from sentence_transformers import SentenceTransformer

        SentenceTransformer("all-MiniLM-L6-v2")
        ok("all-MiniLM-L6-v2 cached locally")
    else:
        print("\n  ℹ️  Optional: python check_setup.py --download-model")
        print("     pre-downloads Module 2's embedding model so it doesn't surprise you mid-exercise.")

    print()
    if good:
        print("All good. Start with module1_weather/README.md")
    else:
        print("Fix the ❌ items above before starting.")
        sys.exit(1)


if __name__ == "__main__":
    main()
