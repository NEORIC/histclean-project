# 🧹 HistClean

A tiny Python script that cleans your terminal history by removing junk (like `ls`, `pwd`), hiding accidentally pasted secrets (passwords/tokens), and deduplicating commands so you can actually find what you typed last week.

## 🚀 How to use

1. Navigate to your project folder.
2. Run it safely (creates a `.clean` file):
   ```bash
   python3 histclean.py
