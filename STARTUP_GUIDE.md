# 🚀 AI Onboarding Buddy - Startup Guide

## ✅ What's Been Completed
- ✓ Project structure organized
- ✓ app.py - Complete RAG application with error handling
- ✓ requirements.txt - All dependencies listed
- ✓ Python environment configured (Python 3.13)
- ✓ All Python packages installed
- ✓ ProjectDetails/ folder ready for your documents

## 📋 Before You Start

### Step 1: Install & Run Ollama
1. Download Ollama from https://ollama.ai
2. Install and run it
3. Open PowerShell/Terminal and pull required models:
```powershell
ollama pull llama3
ollama pull nomic-embed-text
```
4. Ollama will run on http://localhost:11434 by default

### Step 2: Verify Your Documents Are Ready
Your documentation files are in the `ProjectDetails/` folder:
- ✓ agile_methodology (1).pdf
- ✓ CORE-JAVA MATERIAL-UPDATED.pdf
- ✓ Day 1 Selenium.docx
- ✓ JavaScript.txt
- ✓ Levels of testing.pdf
- ✓ SDLC.pptx
- ... and more

**You can add more PDF, Word, or text files here anytime**

## 🎯 Run the Application

### Option A: From Terminal (Recommended)
```powershell
cd d:\Copilot\QACopilot
.\.venv\Scripts\Activate.ps1
chainlit run app.py -w
```

### Option B: From VS Code
1. Open integrated terminal (Ctrl + `)
2. Copy and paste the commands above

## 🌐 Access the Chat
After running, your browser will open automatically at:
```
http://localhost:8000
```

If not, manually open http://localhost:8000 in your browser.

## ✨ Features Built In

### 1. **Self-Healing** ✓
- Checks if ProjectDetails folder exists (creates if missing)
- Verifies Ollama is running before startup
- Clear error messages if something fails

### 2. **Document Processing** ✓
- Supports: PDF, Word (.docx), Text (.txt), PowerPoint (.pptx)
- Uses RecursiveCharacterTextSplitter for optimal chunks
- Processes all files in ProjectDetails/ automatically

### 3. **Direct Answer Guardrails** ✓
- If info not in docs: "I don't have this in my current documentation; please consult a Senior."
- Won't make up answers
- Temperature set to 0.7 for balanced responses

### 4. **Citations** ✓
- Shows which files each answer came from
- Formatted with 📄 file icons for clarity
- Easy to verify sources

### 5. **Chainlit UI** ✓
- User-friendly chat interface
- Shows thinking indicator while searching
- Welcome message on startup
- Clean error handling

## 🐛 Troubleshooting

### "Ollama is not running"
- Make sure Ollama app is running
- Check http://localhost:11434 is accessible
- Try restarting Ollama

### "No documents found in ProjectDetails"
- Ensure you have files in ProjectDetails/ folder
- Supported formats: PDF, DOCX, TXT, PPTX
- Wait a moment if you just added files

### "ConnectionError" at startup
- Check Ollama is fully started
- Wait a few seconds and retry
- Try: `ollama serve` in terminal

### Port 8000 already in use
- Change the port: `chainlit run app.py -w --port 8001`

## 📚 Architecture

```
ProjectDetails/          📁 Your documentation (auto-loaded)
  ├── *.pdf
  ├── *.docx
  ├── *.txt
  └── *.pptx

chroma_db/              📁 Vector database (auto-created on first run)

app.py                  🤖 RAG application with Chainlit UI
requirements.txt        📋 All dependencies
```

## 🎓 How It Works

1. **Load**: Reads all docs from ProjectDetails/
2. **Split**: Chunks text with 1000 chars, 200 overlap
3. **Embed**: Uses nomic-embed-text model
4. **Store**: Saves vectors to chroma_db/ (persistent)
5. **Chat**: User asks, searches top 5 chunks
6. **Answer**: llama3 generates response with guardrails
7. **Cite**: Shows source files with answers

## ✅ Ready to Go!

Your system is configured and ready. Just follow the "Run the Application" steps above.

**Questions?** Check the troubleshooting section or review the detailed comments in app.py
