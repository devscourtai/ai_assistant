/**
 * Root Layout
 *
 * This is the root layout for the entire application.
 * It wraps all pages and provides:
 * - HTML structure
 * - Global styles
 * - Context providers
 * - Metadata
 */

import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { AppProvider } from './context/AppContext'

// Configure Inter font from Google Fonts
const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
})

/**
 * Application metadata
 * This affects SEO and how the app appears when shared
 */
export const metadata: Metadata = {
  title: 'AI Document Assistant',
  description: 'Ask questions about your documents using AI-powered search and retrieval',
  keywords: ['AI', 'Document', 'RAG', 'Question Answering', 'LangChain'],
}

/**
 * Root Layout Component
 *
 * The {children} prop represents the page content that will be rendered
 */
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={inter.className}>
      <body className="antialiased">
        {/* Wrap entire app with AppProvider to provide global state */}
        <AppProvider>
          {children}
        </AppProvider>
      </body>
    </html>
  )
}
