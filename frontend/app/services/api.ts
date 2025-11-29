/**
 * API Service
 *
 * This file handles all communication with the FastAPI backend.
 * It provides clean, typed functions for:
 * - Uploading documents
 * - Asking questions
 * - Fetching statistics
 *
 * Using axios for HTTP requests with proper error handling.
 */

import axios, { AxiosError } from 'axios'

// ============================================================================
// CONFIGURATION
// ============================================================================

/**
 * Base URL for the backend API
 * This can be changed in next.config.js or via environment variables
 */
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

/**
 * Create axios instance with default configuration
 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  // Timeout after 60 seconds (useful for large file uploads)
  timeout: 60000,
})

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

/**
 * Document interface
 * Represents an uploaded document in our system
 */
export interface Document {
  document_id: string
  filename: string
  chunks_created: number
  uploaded_at: string  // ISO date string
}

/**
 * Upload response from backend
 */
export interface UploadResponse {
  message: string
  filename: string
  chunks_created: number
  document_id: string
}

/**
 * Retrieved chunk from vector search
 */
export interface RetrievedChunk {
  content: string
  metadata: {
    source: string
    page?: number
    chunk_index?: number
    [key: string]: any
  }
  similarity_score?: number
}

/**
 * Tool call information (for function calling demo)
 */
export interface ToolCall {
  tool_name: string
  arguments: Record<string, any>
  result: any
}

/**
 * Ask question request
 */
export interface AskRequest {
  question: string
  max_results?: number
  use_tool_calling?: boolean
}

/**
 * Ask question response
 */
export interface AskResponse {
  answer: string
  retrieved_chunks: RetrievedChunk[]
  tool_calls?: ToolCall[]
  tokens_used?: number
}

/**
 * Collection statistics
 */
export interface CollectionStats {
  total_documents: number
  table_name: string
}

/**
 * API Error response
 */
export interface APIError {
  error: string
  detail?: string
}

// ============================================================================
// API FUNCTIONS
// ============================================================================

/**
 * Upload a document to the backend
 *
 * This function:
 * 1. Creates a FormData object with the file
 * 2. Sends it to the /upload/ endpoint
 * 3. Returns the upload response
 *
 * @param file - The file to upload (PDF, DOCX, or TXT)
 * @returns Promise with upload response
 * @throws Error if upload fails
 */
export async function uploadDocument(file: File): Promise<UploadResponse> {
  try {
    // Create FormData to send file
    const formData = new FormData()
    formData.append('file', file)

    // Make API request
    const response = await apiClient.post<UploadResponse>('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      // Progress tracking (optional, can be used for progress bars)
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          )
          console.log(`Upload progress: ${percentCompleted}%`)
        }
      },
    })

    return response.data
  } catch (error) {
    handleAPIError(error, 'Failed to upload document')
    throw error  // Re-throw for component error handling
  }
}

/**
 * Ask a question about uploaded documents
 *
 * This function:
 * 1. Sends the question to the /ask/ endpoint
 * 2. Backend performs RAG (retrieval-augmented generation)
 * 3. Returns answer with source documents
 *
 * @param request - Question and options
 * @returns Promise with answer and retrieved documents
 * @throws Error if request fails
 */
export async function askQuestion(request: AskRequest): Promise<AskResponse> {
  try {
    const response = await apiClient.post<AskResponse>('/ask/', {
      question: request.question,
      max_results: request.max_results || 4,
      use_tool_calling: request.use_tool_calling || false,
    })

    return response.data
  } catch (error) {
    handleAPIError(error, 'Failed to get answer')
    throw error
  }
}

/**
 * Get collection statistics
 *
 * Fetches information about uploaded documents
 *
 * @returns Promise with collection stats
 * @throws Error if request fails
 */
export async function getStats(): Promise<CollectionStats> {
  try {
    const response = await apiClient.get<CollectionStats>('/upload/stats')
    return response.data
  } catch (error) {
    handleAPIError(error, 'Failed to fetch statistics')
    throw error
  }
}

/**
 * Check if the backend API is healthy
 *
 * @returns Promise<boolean> - true if healthy, false otherwise
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const response = await apiClient.get('/health')
    return response.status === 200
  } catch (error) {
    console.error('Health check failed:', error)
    return false
  }
}

// ============================================================================
// ERROR HANDLING
// ============================================================================

/**
 * Handle API errors consistently
 *
 * This function:
 * 1. Extracts error message from axios error
 * 2. Logs it to console
 * 3. Could be extended to show toast notifications
 *
 * @param error - The error object from axios
 * @param defaultMessage - Fallback message if error parsing fails
 */
function handleAPIError(error: unknown, defaultMessage: string): void {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<APIError>

    if (axiosError.response) {
      // Server responded with error status
      const errorData = axiosError.response.data
      console.error('API Error:', errorData)

      // You could show a toast notification here
      // toast.error(errorData.error || defaultMessage)
    } else if (axiosError.request) {
      // Request made but no response received
      console.error('Network Error:', axiosError.message)
      // toast.error('Network error. Please check your connection.')
    } else {
      // Something else happened
      console.error('Error:', axiosError.message)
      // toast.error(defaultMessage)
    }
  } else {
    // Non-axios error
    console.error('Unexpected error:', error)
    // toast.error(defaultMessage)
  }
}

/**
 * Export API client for advanced usage if needed
 */
export { apiClient }
