/**
 * App Context - Global State Management
 *
 * This file implements React Context API for managing global application state.
 * It's a simple alternative to Redux, perfect for smaller applications.
 *
 * What it manages:
 * - List of uploaded documents
 * - Current question and answer
 * - Loading states
 * - Error messages
 *
 * Why use Context API?
 * - Share state between components without prop drilling
 * - Centralized state management
 * - Easy to understand for beginners
 * - No external libraries needed
 */

'use client'

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react'
import { Document, AskResponse, uploadDocument, askQuestion, getStats } from '../services/api'

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

/**
 * Shape of our global application state
 */
interface AppState {
  // Documents
  documents: Document[]
  totalDocuments: number

  // Current question/answer
  currentQuestion: string
  currentAnswer: AskResponse | null

  // Loading states
  isUploading: boolean
  isAsking: boolean

  // Error messages
  uploadError: string | null
  askError: string | null
}

/**
 * Actions available in the context
 * These are functions that components can call to modify state
 */
interface AppContextType extends AppState {
  // Document actions
  uploadFile: (file: File) => Promise<void>
  refreshStats: () => Promise<void>

  // Question actions
  submitQuestion: (question: string, maxResults?: number, useToolCalling?: boolean) => Promise<void>
  clearAnswer: () => void

  // UI actions
  clearErrors: () => void
}

// ============================================================================
// CREATE CONTEXT
// ============================================================================

/**
 * Create the context with undefined as initial value
 * We'll provide the actual value in the Provider component
 */
const AppContext = createContext<AppContextType | undefined>(undefined)

// ============================================================================
// PROVIDER COMPONENT
// ============================================================================

/**
 * AppProvider component
 *
 * This wraps your entire application and provides the state to all children.
 * Place this in your root layout.tsx file.
 *
 * Usage:
 * ```tsx
 * <AppProvider>
 *   <YourApp />
 * </AppProvider>
 * ```
 */
export function AppProvider({ children }: { children: ReactNode }) {
  // ========================================
  // STATE
  // ========================================

  // Document state
  const [documents, setDocuments] = useState<Document[]>([])
  const [totalDocuments, setTotalDocuments] = useState(0)

  // Question/Answer state
  const [currentQuestion, setCurrentQuestion] = useState('')
  const [currentAnswer, setCurrentAnswer] = useState<AskResponse | null>(null)

  // Loading states
  const [isUploading, setIsUploading] = useState(false)
  const [isAsking, setIsAsking] = useState(false)

  // Error states
  const [uploadError, setUploadError] = useState<string | null>(null)
  const [askError, setAskError] = useState<string | null>(null)

  // ========================================
  // ACTIONS
  // ========================================

  /**
   * Upload a file
   *
   * This function:
   * 1. Sets loading state
   * 2. Calls API to upload file
   * 3. Updates documents list
   * 4. Handles errors
   */
  const uploadFile = useCallback(async (file: File) => {
    try {
      // Clear previous errors
      setUploadError(null)

      // Set loading state
      setIsUploading(true)

      // Call API
      const response = await uploadDocument(file)

      // Add uploaded document to list
      const newDoc: Document = {
        document_id: response.document_id,
        filename: response.filename,
        chunks_created: response.chunks_created,
        uploaded_at: new Date().toISOString(),
      }

      setDocuments(prev => [newDoc, ...prev])

      // Refresh total count
      await refreshStats()

    } catch (error) {
      console.error('Upload failed:', error)
      setUploadError(error instanceof Error ? error.message : 'Upload failed')
      throw error
    } finally {
      setIsUploading(false)
    }
  }, [])

  /**
   * Refresh document statistics
   *
   * Fetches the latest document count from the backend
   */
  const refreshStats = useCallback(async () => {
    try {
      const stats = await getStats()
      setTotalDocuments(stats.total_documents)
    } catch (error) {
      console.error('Failed to fetch stats:', error)
    }
  }, [])

  /**
   * Submit a question
   *
   * This function:
   * 1. Sets loading state
   * 2. Calls RAG API
   * 3. Stores answer
   * 4. Handles errors
   */
  const submitQuestion = useCallback(async (
    question: string,
    maxResults: number = 4,
    useToolCalling: boolean = false
  ) => {
    try {
      // Clear previous errors
      setAskError(null)

      // Set loading state
      setIsAsking(true)

      // Store question
      setCurrentQuestion(question)

      // Call API
      const response = await askQuestion({
        question,
        max_results: maxResults,
        use_tool_calling: useToolCalling,
      })

      // Store answer
      setCurrentAnswer(response)

    } catch (error) {
      console.error('Question failed:', error)
      setAskError(error instanceof Error ? error.message : 'Failed to get answer')
      throw error
    } finally {
      setIsAsking(false)
    }
  }, [])

  /**
   * Clear current answer
   */
  const clearAnswer = useCallback(() => {
    setCurrentQuestion('')
    setCurrentAnswer(null)
    setAskError(null)
  }, [])

  /**
   * Clear all error messages
   */
  const clearErrors = useCallback(() => {
    setUploadError(null)
    setAskError(null)
  }, [])

  // ========================================
  // CONTEXT VALUE
  // ========================================

  /**
   * Combine all state and actions into context value
   */
  const contextValue: AppContextType = {
    // State
    documents,
    totalDocuments,
    currentQuestion,
    currentAnswer,
    isUploading,
    isAsking,
    uploadError,
    askError,

    // Actions
    uploadFile,
    refreshStats,
    submitQuestion,
    clearAnswer,
    clearErrors,
  }

  // ========================================
  // RENDER
  // ========================================

  return (
    <AppContext.Provider value={contextValue}>
      {children}
    </AppContext.Provider>
  )
}

// ============================================================================
// CUSTOM HOOK
// ============================================================================

/**
 * useApp Hook
 *
 * Custom hook to access the app context from any component.
 * This provides a clean API and ensures context is used correctly.
 *
 * Usage in components:
 * ```tsx
 * function MyComponent() {
 *   const { documents, uploadFile, isUploading } = useApp()
 *
 *   return (
 *     <button onClick={() => uploadFile(file)} disabled={isUploading}>
 *       Upload
 *     </button>
 *   )
 * }
 * ```
 */
export function useApp() {
  const context = useContext(AppContext)

  // Throw error if hook is used outside provider
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider')
  }

  return context
}

/**
 * Export context for advanced usage if needed
 */
export { AppContext }
