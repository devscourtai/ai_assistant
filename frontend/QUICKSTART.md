# Frontend Quick Start Guide

Get your frontend running in 3 minutes!

## Prerequisites

- [ ] Node.js 18+ installed
- [ ] Backend API running at http://localhost:8000
- [ ] npm or yarn installed

## Steps

### 1. Install Dependencies (1 minute)

```bash
cd frontend
npm install
```

### 2. Configure Environment (30 seconds)

```bash
# Create environment file
cp .env.example .env.local

# Edit if your backend runs on a different port
# (optional, default is http://localhost:8000)
```

### 3. Start Development Server (30 seconds)

```bash
npm run dev
```

### 4. Open Your Browser (30 seconds)

Visit: **http://localhost:4000**

You should see the AI Document Assistant dashboard!

## Test It Out

1. **Upload a Document**
   - Drag and drop a PDF/DOCX/TXT file
   - Or click "Browse Files"
   - Wait for success message

2. **Ask a Question**
   - Type your question in the text area
   - Click "Ask Question"
   - See the AI-generated answer with sources!

## What's Next?

1. **Explore the Code**: Check out the components in `app/components/`
2. **Modify Styles**: Edit `app/globals.css` or Tailwind classes
3. **Add Features**: Try implementing document deletion or search
4. **Read Full README**: See [README.md](README.md) for detailed docs

## Common Issues

### "Cannot connect to backend"
- Make sure backend is running: `http://localhost:9000/health`
- Check `.env.local` has correct API URL

### "Module not found"
```bash
rm -rf node_modules .next
npm install
npm run dev
```

### Port 3000 already in use
```bash
# Run on different port
PORT=3001 npm run dev
```

---

**That's it! You're ready to code!** 🚀
