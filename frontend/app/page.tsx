/**
 * Home Page / Dashboard
 * Enterprise-Grade UI with Modern SaaS Design
 *
 * Features:
 * - Premium header with glass-morphism
 * - Hero section with gradient background
 * - Clean grid layout with proper spacing
 * - Modern card designs with shadows
 * - Responsive across all devices
 */

'use client'

import { Brain, Github, Sparkles, Zap, Shield } from 'lucide-react'
import { UploadDocument } from './components/UploadDocument'
import { AskQuestion } from './components/AskQuestion'
import { DocumentList } from './components/DocumentList'

export default function Home() {
  return (
    <div className="min-h-screen gradient-bg">
      {/* Premium Header with Glass Effect */}
      <header className="border-b border-border/40 bg-white/70 backdrop-blur-xl sticky top-0 z-50 shadow-soft">
        <div className="container mx-auto px-4 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            {/* Brand Identity */}
            <div className="flex items-center gap-3 group">
              <div className="h-11 w-11 rounded-xl bg-gradient-to-br from-primary to-primary-hover flex items-center justify-center shadow-medium hover-scale">
                <Brain className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold tracking-tight text-foreground">
                  AI Document Assistant
                </h1>
                <p className="text-xs text-muted-foreground font-medium">
                  Powered by Devscourt AI
                </p>
              </div>
            </div>

            {/* Navigation Links */}
            <div className="flex items-center gap-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-smooth rounded-lg hover:bg-muted/50"
              >
                <Github className="h-4 w-4" />
                <span className="hidden sm:inline">GitHub</span>
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section with Gradient */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 gradient-bg-alt opacity-50"></div>
        <div className="relative container mx-auto px-4 lg:px-8 py-16 lg:py-20">
          <div className="max-w-4xl mx-auto text-center fade-in">
            <div className="inline-flex items-center gap-2 px-4 py-2 mb-6 rounded-full bg-primary/10 border border-primary/20 text-primary text-sm font-medium">
              <Sparkles className="h-4 w-4" />
              <span>Enterprise RAG Platform</span>
            </div>

            <h2 className="text-4xl lg:text-5xl font-bold tracking-tight text-foreground mb-6 leading-tight">
              Transform Documents into
              <span className="block mt-2 bg-gradient-to-r from-primary to-primary-hover bg-clip-text text-transparent">
                Actionable Insights
              </span>
            </h2>

            <p className="text-lg text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              Upload your documents and leverage AI-powered retrieval-augmented generation
              to get accurate answers with source citations in seconds.
            </p>

            {/* Feature Pills */}
            <div className="flex flex-wrap items-center justify-center gap-6 mt-10">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <div className="h-8 w-8 rounded-lg bg-primary/10 flex items-center justify-center">
                  <Zap className="h-4 w-4 text-primary" />
                </div>
                <span className="font-medium">Lightning Fast</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <div className="h-8 w-8 rounded-lg bg-success/10 flex items-center justify-center">
                  <Shield className="h-4 w-4 text-success" />
                </div>
                <span className="font-medium">Secure & Private</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <div className="h-8 w-8 rounded-lg bg-warning/10 flex items-center justify-center">
                  <Brain className="h-4 w-4 text-warning" />
                </div>
                <span className="font-medium">AI-Powered</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content Area */}
      <main className="container mx-auto px-4 lg:px-8 py-12 lg:py-16">
        {/* Primary Grid Layout */}

        {/* Interactive Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 lg:gap-10">
          {/* Primary Content - Upload and Questions */}
          <div className="lg:col-span-2 space-y-8">
            <UploadDocument />
            <AskQuestion />
          </div>

          {/* Sidebar - Document Management */}
          <div className="lg:col-span-1 slide-in-right">
            <DocumentList />
          </div>
        </div>

        {/* How It Works - Modern Step Cards */}
        <section className="mt-20 lg:mt-24">
          <div className="text-center mb-12">
            <h3 className="text-2xl lg:text-3xl font-bold text-foreground mb-3">
              How It Works
            </h3>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Get started in three simple steps and unlock the power of AI-driven document intelligence
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
            {/* Step 1 - Upload */}
            <div className="group relative">
              <div className="p-8 rounded-2xl bg-white border border-border shadow-medium hover:shadow-large transition-all duration-300 h-full">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <span className="text-2xl font-bold text-primary">1</span>
                </div>
                <h4 className="text-lg font-semibold text-foreground mb-3">
                  Upload Documents
                </h4>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  Upload PDF, DOCX, or TXT files. Documents are automatically processed,
                  chunked, and embedded for semantic search.
                </p>
              </div>
            </div>

            {/* Step 2 - Ask */}
            <div className="group relative">
              <div className="p-8 rounded-2xl bg-white border border-border shadow-medium hover:shadow-large transition-all duration-300 h-full">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <span className="text-2xl font-bold text-primary">2</span>
                </div>
                <h4 className="text-lg font-semibold text-foreground mb-3">
                  Ask Questions
                </h4>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  Type natural language questions. Advanced RAG retrieves relevant
                  context and generates accurate answers.
                </p>
              </div>
            </div>

            {/* Step 3 - Get Answers */}
            <div className="group relative">
              <div className="p-8 rounded-2xl bg-white border border-border shadow-medium hover:shadow-large transition-all duration-300 h-full">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <span className="text-2xl font-bold text-primary">3</span>
                </div>
                <h4 className="text-lg font-semibold text-foreground mb-3">
                  Get Insights
                </h4>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  Receive intelligent answers with source citations, similarity scores,
                  and exact document references.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Tech Stack Badge */}
        <section className="mt-16 lg:mt-20">
          <div className="p-8 rounded-2xl bg-white/60 backdrop-blur-sm border border-border/50 shadow-soft">
            <div className="flex flex-col items-center justify-center gap-6">
              <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">
                Built with Enterprise-Grade Technologies
              </p>
              <div className="flex flex-wrap items-center justify-center gap-4 lg:gap-6">
                {['Next.js', 'FastAPI', 'LangChain', 'OpenRouter', 'Supabase', 'PostgreSQL', 'TailwindCSS'].map((tech) => (
                  <div
                    key={tech}
                    className="px-4 py-2 rounded-lg bg-white border border-border text-sm font-medium text-foreground shadow-soft hover:shadow-medium transition-smooth hover:-translate-y-0.5"
                  >
                    {tech}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Premium Footer */}
      <footer className="border-t border-border/50 bg-white/80 backdrop-blur-sm mt-20">
        <div className="container mx-auto px-4 lg:px-8 py-10">
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-4">
              <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-primary to-primary-hover flex items-center justify-center">
                <Brain className="h-4 w-4 text-white" />
              </div>
              <span className="font-semibold text-foreground">AI Document Assistant</span>
            </div>

            <p className="text-sm text-muted-foreground mb-3">
              Built for the AI Engineering Workshop • Powered by Devscourt AI
            </p>

            <div className="flex items-center justify-center gap-6 text-sm">
              <a
                href="https://python.langchain.com/docs/get_started/introduction"
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-primary transition-colors font-medium"
              >
                Learn about RAG
              </a>
              <span className="text-border">•</span>
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-primary transition-colors font-medium"
              >
                View Source
              </a>
              <span className="text-border">•</span>
              <a
                href="#"
                className="text-muted-foreground hover:text-primary transition-colors font-medium"
              >
                Documentation
              </a>
            </div>

            <p className="mt-6 text-xs text-muted-foreground">
              © 2025 Devscourt AI. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
