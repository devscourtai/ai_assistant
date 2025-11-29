# AI Document Assistant - Frontend

A clean, minimal, visually appealing frontend for the AI Document Assistant. Built with Next.js, TailwindCSS, and ShadCN components for a modern, enterprise SaaS experience.

Perfect for workshops and learning modern React patterns!

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [How It Works](#how-it-works)
- [Component Guide](#component-guide)
- [State Management](#state-management)
- [Styling](#styling)
- [API Integration](#api-integration)
- [Customization](#customization)

---

## Features

- **Document Upload**: Drag-and-drop or click to upload PDF, DOCX, TXT files
- **Question Answering**: Ask questions in natural language
- **Real-time Answers**: Get AI-generated responses with source citations
- **Document Management**: View all uploaded documents
- **Clean UI**: Modern, minimalist design with smooth animations
- **Responsive**: Works perfectly on desktop, tablet, and mobile
- **Type-Safe**: Full TypeScript support
- **State Management**: Simple Context API (no Redux complexity)

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Next.js 14** | React framework with App Router |
| **TypeScript** | Type safety and better DX |
| **TailwindCSS** | Utility-first CSS framework |
| **ShadCN UI** | Beautiful, accessible component library |
| **Context API** | Global state management |
| **Axios** | HTTP client for API calls |
| **Lucide Icons** | Beautiful, consistent icons |

---

## Project Structure

```
frontend/
├── app/
│   ├── components/          # React components
│   │   ├── ui/             # ShadCN UI components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   └── textarea.tsx
│   │   ├── UploadDocument.tsx   # Document upload component
│   │   ├── AskQuestion.tsx      # Question asking component
│   │   └── DocumentList.tsx     # Document list component
│   │
│   ├── context/            # State management
│   │   └── AppContext.tsx  # Global app state
│   │
│   ├── services/           # API communication
│   │   └── api.ts          # Backend API calls
│   │
│   ├── lib/                # Utilities
│   │   └── utils.ts        # Helper functions
│   │
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page
│   └── globals.css         # Global styles
│
├── public/                 # Static assets
├── package.json            # Dependencies
├── tsconfig.json           # TypeScript config
├── tailwind.config.ts      # Tailwind config
├── next.config.js          # Next.js config
└── README.md               # This file
```

---

## Setup

### Prerequisites

- Node.js 18+ installed
- Backend API running (see backend README)
- npm or yarn package manager

### Installation

1. **Navigate to frontend directory**

```bash
cd frontend
```

2. **Install dependencies**

```bash
npm install
# or
yarn install
```

3. **Set up environment variables**

```bash
# Copy example file
cp .env.example .env.local

# Edit .env.local if your backend runs on a different port
# Default: NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Running the Application

### Development Mode

```bash
npm run dev
# or
yarn dev
```

The app will be available at: **http://localhost:3000**

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

### Linting

```bash
npm run lint
```

---

## How It Works

### User Flow

```
1. User opens dashboard → sees clean interface

2. User uploads document
   ↓
   UploadDocument component → API call → Backend processes
   ↓
   Success message → DocumentList updates

3. User asks question
   ↓
   AskQuestion component → API call → Backend RAG pipeline
   ↓
   Answer displayed with sources → Retrieved chunks shown
```

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Next.js Frontend                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐ │
│  │   Upload    │      │     Ask     │      │  Document   │ │
│  │  Component  │      │  Component  │      │    List     │ │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘ │
│         │                     │                     │        │
│         └─────────────┬───────┴─────────────────────┘        │
│                       │                                       │
│                ┌──────▼──────┐                               │
│                │  App Context │ (Global State)               │
│                └──────┬──────┘                               │
│                       │                                       │
│                ┌──────▼──────┐                               │
│                │ API Service  │ (Axios)                      │
│                └──────┬──────┘                               │
└───────────────────────┼──────────────────────────────────────┘
                        │
                ┌───────▼──────┐
                │   FastAPI    │
                │   Backend    │
                └──────────────┘
```

---

## Component Guide

### 1. UploadDocument Component

**Location**: `app/components/UploadDocument.tsx`

**Features**:
- Drag and drop file upload
- Click to browse files
- File type validation (PDF, DOCX, TXT)
- File size validation (max 10MB)
- Upload progress indication
- Success/error messages
- Disabled state during upload

**Usage**:
```tsx
<UploadDocument />
```

**Key Functions**:
- `handleUpload()`: Validates and uploads file
- `handleDrop()`: Handles drag-and-drop events
- Uses `uploadFile()` from Context API

---

### 2. AskQuestion Component

**Location**: `app/components/AskQuestion.tsx`

**Features**:
- Textarea for question input
- Submit button with loading state
- Answer display with formatting
- Source citations with similarity scores
- Tool call information (if enabled)
- Error handling

**Usage**:
```tsx
<AskQuestion />
```

**Key Functions**:
- `handleSubmit()`: Submits question to backend
- `handleClear()`: Clears current answer
- Uses `submitQuestion()` from Context API

---

### 3. DocumentList Component

**Location**: `app/components/DocumentList.tsx`

**Features**:
- Displays all uploaded documents
- Shows filename, chunks, upload date
- Empty state when no documents
- Auto-refreshes on new uploads
- Status badges

**Usage**:
```tsx
<DocumentList />
```

**Key Functions**:
- `refreshStats()`: Fetches document count
- Uses `documents` and `totalDocuments` from Context API

---

### 4. UI Components (ShadCN)

**Location**: `app/components/ui/`

These are reusable, styled components:

**Button**:
```tsx
<Button variant="default">Click me</Button>
<Button variant="outline" size="sm">Small</Button>
```

**Card**:
```tsx
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>
    Content here
  </CardContent>
</Card>
```

**Input**:
```tsx
<Input
  type="text"
  placeholder="Enter text..."
  value={value}
  onChange={(e) => setValue(e.target.value)}
/>
```

**Textarea**:
```tsx
<Textarea
  rows={4}
  placeholder="Enter question..."
/>
```

---

## State Management

### Context API

The app uses React Context API for global state management. This is simpler than Redux and perfect for smaller applications.

**Location**: `app/context/AppContext.tsx`

**What it manages**:
- List of uploaded documents
- Current question and answer
- Loading states (uploading, asking)
- Error messages

**Using the Context**:

```tsx
import { useApp } from '@/app/context/AppContext'

function MyComponent() {
  // Access state and actions
  const {
    documents,
    totalDocuments,
    currentAnswer,
    isUploading,
    isAsking,
    uploadFile,
    submitQuestion,
  } = useApp()

  // Use in your component
  return (
    <button onClick={() => uploadFile(file)} disabled={isUploading}>
      Upload
    </button>
  )
}
```

**Key Actions**:
- `uploadFile(file)`: Upload a document
- `submitQuestion(question)`: Ask a question
- `refreshStats()`: Refresh document count
- `clearAnswer()`: Clear current answer
- `clearErrors()`: Clear error messages

---

## Styling

### Tailwind CSS

The app uses Tailwind CSS for styling with a custom configuration.

**Key Features**:
- Custom color scheme defined in `globals.css`
- Utility classes for common patterns
- Responsive design built-in
- Dark mode support (optional)

**Common Patterns**:

```tsx
// Card with shadow
<div className="rounded-lg border bg-card shadow-medium">

// Centered flex container
<div className="flex items-center justify-center gap-2">

// Responsive grid
<div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

// Hover effects
<div className="hover:bg-accent transition-colors">
```

### Custom Utilities

**Location**: `globals.css`

```css
.shadow-soft     /* Subtle shadow */
.shadow-medium   /* Medium shadow */
.glass-effect    /* Glass morphism */
.gradient-bg     /* Gradient background */
```

---

## API Integration

### API Service

**Location**: `app/services/api.ts`

This file handles all backend communication using Axios.

**Available Functions**:

1. **Upload Document**
```typescript
import { uploadDocument } from '@/app/services/api'

const response = await uploadDocument(file)
// Returns: { filename, chunks_created, document_id }
```

2. **Ask Question**
```typescript
import { askQuestion } from '@/app/services/api'

const response = await askQuestion({
  question: "What is the refund policy?",
  max_results: 4,
  use_tool_calling: false
})
// Returns: { answer, retrieved_chunks, tool_calls, tokens_used }
```

3. **Get Statistics**
```typescript
import { getStats } from '@/app/services/api'

const stats = await getStats()
// Returns: { total_documents, table_name }
```

4. **Health Check**
```typescript
import { checkHealth } from '@/app/services/api'

const isHealthy = await checkHealth()
// Returns: boolean
```

### Error Handling

All API calls include automatic error handling:
- Network errors are caught and logged
- Server errors are extracted and displayed
- Errors are stored in Context API for UI display

---

## Customization

### Changing Colors

Edit `app/globals.css`:

```css
:root {
  --primary: 222.2 47.4% 11.2%;    /* Your primary color */
  --secondary: 210 40% 96.1%;      /* Your secondary color */
  /* ... other colors */
}
```

### Changing API URL

Edit `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://your-backend-url:8000
```

### Adding New Components

1. Create component file in `app/components/`
2. Follow existing patterns
3. Use ShadCN UI components for consistency
4. Access Context API with `useApp()` hook
5. Export and import in `page.tsx`

### Modifying Layout

Edit `app/page.tsx` to change the dashboard layout:

```tsx
// Current: 2-column layout (2/3 + 1/3)
<div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
  <div className="lg:col-span-2">
    {/* Left side */}
  </div>
  <div className="lg:col-span-1">
    {/* Right side */}
  </div>
</div>
```

---

## Troubleshooting

### "Cannot connect to backend"

1. Check if backend is running: `http://localhost:8000/health`
2. Verify `NEXT_PUBLIC_API_URL` in `.env.local`
3. Check CORS settings in backend

### "Module not found"

```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules
npm install

# Restart dev server
npm run dev
```

### "Tailwind classes not working"

1. Check `tailwind.config.ts` content paths
2. Restart dev server
3. Clear browser cache

### Type Errors

```bash
# Regenerate TypeScript types
npm run build
```

---

## Learning Resources

### Next.js
- [Next.js Documentation](https://nextjs.org/docs)
- [Next.js App Router](https://nextjs.org/docs/app)
- [React Server Components](https://nextjs.org/docs/getting-started/react-essentials)

### TailwindCSS
- [Tailwind Documentation](https://tailwindcss.com/docs)
- [Tailwind UI Components](https://tailwindui.com)

### ShadCN
- [ShadCN UI Documentation](https://ui.shadcn.com)
- [Component Examples](https://ui.shadcn.com/docs/components)

### React Patterns
- [React Context API](https://react.dev/reference/react/useContext)
- [React Hooks](https://react.dev/reference/react)

---

## Next Steps

### For Workshop Participants

1. **Understand the Flow**
   - Follow a document upload from start to finish
   - Trace how state updates across components
   - See how API calls work

2. **Modify and Experiment**
   - Change colors and styling
   - Add new UI components
   - Implement additional features

3. **Add Features**
   - Document deletion
   - Edit uploaded documents
   - Search/filter documents
   - Conversation history
   - Settings page

4. **Performance Optimization**
   - Add loading skeletons
   - Implement pagination
   - Cache API responses
   - Optimize re-renders

---

## Summary

You now have a **complete, working frontend** that demonstrates:

✅ Modern React with Next.js 14
✅ TypeScript for type safety
✅ Context API for state management
✅ TailwindCSS for styling
✅ ShadCN for beautiful components
✅ Clean, maintainable code
✅ Responsive design
✅ API integration

**This is production-ready code used in real SaaS applications!**

---

**Ready to build? Run `npm run dev` and start coding!** 🚀
