/**
 * AskQuestion Component
 *
 * Allows users to ask questions about their uploaded documents.
 * Displays AI-generated answers with source citations.
 *
 * Features:
 * - Text input for questions
 * - Real-time answer display
 * - Shows retrieved document chunks (sources)
 * - Displays similarity scores
 * - Optional tool calling demonstration
 * - Loading states
 * - Error handling
 */

'use client'

import React, { useState } from 'react'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from './ui/card'
import { Button } from './ui/button'
import { Textarea } from './ui/textarea'
import { AlertModal } from './ui/alert-modal'
import { useApp } from '../context/AppContext'
import {
  MessageSquare,
  Send,
  Loader2,
  FileText,
  Sparkles,
  AlertCircle,
  Zap,
} from 'lucide-react'

export function AskQuestion() {
  // Access global state and actions
  const {
    currentQuestion,
    currentAnswer,
    isAsking,
    askError,
    submitQuestion,
    clearAnswer,
    totalDocuments,
  } = useApp()

  // Local state for the input field
  const [question, setQuestion] = useState('')
  const [showNoDocumentsModal, setShowNoDocumentsModal] = useState(false)

  /**
   * Handle form submission
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // Validate input
    if (!question.trim()) {
      alert('Please enter a question')
      return
    }

    // Check if documents exist
    if (totalDocuments === 0) {
      setShowNoDocumentsModal(true)
      return
    }

    try {
      // Submit question
      await submitQuestion(question, 4, false)
      // Keep question in input for reference
    } catch (error) {
      // Error is handled in context
      console.error('Question failed:', error)
    }
  }

  /**
   * Handle clear button
   */
  const handleClear = () => {
    setQuestion('')
    clearAnswer()
  }

  return (
    <div className="space-y-8">
      {/* Question Input Card - Premium Design */}
      <Card className="shadow-large border-border/50 hover:shadow-enterprise transition-all duration-300 bg-white">
        <CardHeader className="space-y-2">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center">
              <MessageSquare className="h-5 w-5 text-primary" />
            </div>
            <div>
              <CardTitle className="text-xl font-semibold">Ask a Question</CardTitle>
              <CardDescription className="text-sm">
                Query your documents with natural language
              </CardDescription>
            </div>
          </div>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Question Input - Premium Textarea */}
            <div>
              <Textarea
                placeholder="Example: What is the refund policy for returns?"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                rows={4}
                disabled={isAsking}
                className="resize-none border-border focus:border-primary focus:ring-primary/20 rounded-xl text-base shadow-soft"
              />
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3">
              <Button
                type="submit"
                disabled={isAsking || !question.trim()}
                size="lg"
                className="flex-1 font-medium shadow-medium hover:shadow-large transition-all"
              >
                {isAsking ? (
                  <>
                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                    AI is thinking...
                  </>
                ) : (
                  <>
                    <Send className="mr-2 h-5 w-5" />
                    Ask Question
                  </>
                )}
              </Button>

              {(currentAnswer || askError) && (
                <Button
                  type="button"
                  variant="outline"
                  size="lg"
                  onClick={handleClear}
                  disabled={isAsking}
                  className="px-6 font-medium shadow-soft hover:shadow-medium transition-all"
                >
                  Clear
                </Button>
              )}
            </div>
          </form>

          {/* Error Message - Premium Alert */}
          {askError && (
            <div className="mt-5 flex items-start gap-3 p-4 rounded-xl bg-destructive/5 border border-destructive/20 fade-in">
              <div className="h-8 w-8 rounded-lg bg-destructive/10 flex items-center justify-center flex-shrink-0">
                <AlertCircle className="h-5 w-5 text-destructive" />
              </div>
              <div className="flex-1 pt-0.5">
                <p className="text-sm font-medium text-destructive">
                  Unable to Process Question
                </p>
                <p className="text-sm text-destructive/80 mt-1">{askError}</p>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Answer Card - Premium Design with Gradient Border */}
      {currentAnswer && !askError && (
        <Card className="shadow-enterprise border-2 border-primary/30 bg-gradient-to-br from-white to-primary/5 fade-in">
          <CardHeader className="space-y-3">
            <div className="flex items-start gap-3">
              <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-primary to-primary-hover flex items-center justify-center flex-shrink-0 shadow-medium">
                <Sparkles className="h-5 w-5 text-white" />
              </div>
              <div className="flex-1">
                <CardTitle className="text-xl font-semibold text-foreground">AI Answer</CardTitle>
                {currentQuestion && (
                  <CardDescription className="text-base text-foreground/70 mt-1.5 leading-relaxed">
                    <span className="font-medium">Q:</span> {currentQuestion}
                  </CardDescription>
                )}
              </div>
            </div>
          </CardHeader>

          <CardContent className="space-y-6">
            {/* AI Answer - Premium Box */}
            <div className="relative">
              <div className="absolute -inset-1 bg-gradient-to-r from-primary/20 to-primary/5 rounded-2xl blur-sm"></div>
              <div className="relative p-6 rounded-2xl bg-white border border-primary/20 shadow-medium">
                <p className="text-base leading-relaxed text-foreground whitespace-pre-wrap">
                  {currentAnswer.answer}
                </p>
              </div>
            </div>

            {/* Token Usage Badge */}
            {currentAnswer.tokens_used && (
              <div className="flex justify-end">
                <span className="inline-flex items-center px-3 py-1.5 rounded-lg bg-muted/50 border border-border text-xs font-medium text-muted-foreground">
                  ~{currentAnswer.tokens_used} tokens used
                </span>
              </div>
            )}

            {/* Tool Calls - Premium Display */}
            {currentAnswer.tool_calls && currentAnswer.tool_calls.length > 0 && (
              <div className="space-y-3">
                <h4 className="text-sm font-semibold text-foreground flex items-center gap-2">
                  <div className="h-5 w-5 rounded bg-primary/10 flex items-center justify-center">
                    <Zap className="h-3 w-3 text-primary" />
                  </div>
                  Function Calls
                </h4>
                {currentAnswer.tool_calls.map((call, idx) => (
                  <div
                    key={idx}
                    className="p-4 rounded-xl bg-gradient-to-br from-accent/30 to-accent/10 border border-primary/20 fade-in"
                  >
                    <p className="font-semibold text-sm text-primary mb-2">
                      {call.tool_name}
                    </p>
                    <p className="text-sm text-foreground/80">
                      <span className="font-medium">Result:</span> {JSON.stringify(call.result)}
                    </p>
                  </div>
                ))}
              </div>
            )}

            {/* Retrieved Chunks - Premium Source Cards */}
            {currentAnswer.retrieved_chunks.length > 0 && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-semibold text-foreground flex items-center gap-2">
                    <div className="h-6 w-6 rounded-lg bg-primary/10 flex items-center justify-center">
                      <FileText className="h-3.5 w-3.5 text-primary" />
                    </div>
                    Source Documents
                  </h4>
                  <span className="text-xs font-medium text-muted-foreground px-2.5 py-1 rounded-lg bg-muted/50 border border-border">
                    {currentAnswer.retrieved_chunks.length} {currentAnswer.retrieved_chunks.length === 1 ? 'source' : 'sources'}
                  </span>
                </div>

                <div className="space-y-3">
                  {currentAnswer.retrieved_chunks.map((chunk, idx) => (
                    <div
                      key={idx}
                      className="group p-5 rounded-xl border border-border bg-white hover:border-primary/30 hover:shadow-medium transition-all duration-200"
                    >
                      {/* Source Header */}
                      <div className="flex items-start justify-between gap-3 mb-3">
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-semibold text-foreground truncate">
                            {chunk.metadata.source || 'Unknown source'}
                          </p>
                          {chunk.metadata.page && (
                            <p className="text-xs text-muted-foreground mt-0.5">
                              Page {chunk.metadata.page}
                            </p>
                          )}
                        </div>

                        {/* Similarity Score Badge */}
                        {chunk.similarity_score !== undefined && (
                          <div className="flex-shrink-0">
                            <span className="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold bg-primary/10 text-primary border border-primary/20">
                              {(chunk.similarity_score * 100).toFixed(0)}% match
                            </span>
                          </div>
                        )}
                      </div>

                      {/* Source Content */}
                      <div className="text-sm text-muted-foreground leading-relaxed pl-3 border-l-2 border-primary/20">
                        {chunk.content.length > 300
                          ? chunk.content.slice(0, 300) + '...'
                          : chunk.content
                        }
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* No Documents Alert Modal */}
      <AlertModal
        isOpen={showNoDocumentsModal}
        onClose={() => setShowNoDocumentsModal(false)}
        title="No Documents Uploaded"
        message="Please upload at least one document before asking questions"
        variant="warning"
      />
    </div>
  )
}
