/**
 * UploadDocument Component
 *
 * Allows users to upload documents (PDF, DOCX, TXT) via:
 * - Click to browse files
 * - Drag and drop
 *
 * Features:
 * - Visual feedback during drag
 * - File type validation
 * - Upload progress indication
 * - Success/error messages
 * - Disabled state during upload
 */

'use client'

import React, { useState, useRef, DragEvent, ChangeEvent } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { useApp } from '../context/AppContext'
import { Upload, FileText, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react'

// Allowed file types
const ALLOWED_TYPES = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'application/msword',
  'text/plain',
]

const ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.doc', '.txt']

export function UploadDocument() {
  // Access global state and actions
  const { uploadFile, isUploading, uploadError } = useApp()

  // Local state for drag/drop and success message
  const [isDragging, setIsDragging] = useState(false)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)

  // Ref for hidden file input
  const fileInputRef = useRef<HTMLInputElement>(null)

  /**
   * Validate file type
   */
  const isValidFileType = (file: File): boolean => {
    const extension = '.' + file.name.split('.').pop()?.toLowerCase()
    return ALLOWED_TYPES.includes(file.type) || ALLOWED_EXTENSIONS.includes(extension)
  }

  /**
   * Handle file upload
   */
  const handleUpload = async (file: File) => {
    // Clear previous messages
    setSuccessMessage(null)

    // Validate file type
    if (!isValidFileType(file)) {
      alert('Invalid file type. Please upload PDF, DOCX, or TXT files.')
      return
    }

    // Validate file size (max 10MB)
    const maxSize = 10 * 1024 * 1024 // 10MB
    if (file.size > maxSize) {
      alert('File too large. Maximum size is 10MB.')
      return
    }

    try {
      // Call upload function from context
      await uploadFile(file)

      // Show success message
      setSuccessMessage(`Successfully uploaded ${file.name}`)

      // Clear success message after 5 seconds
      setTimeout(() => {
        setSuccessMessage(null)
      }, 5000)

    } catch (error) {
      // Error is handled in context and shown via uploadError
      console.error('Upload failed:', error)
    }
  }

  /**
   * Handle file input change (browse button)
   */
  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      handleUpload(file)
    }

    // Reset input value to allow uploading the same file again
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  /**
   * Handle drag enter
   */
  const handleDragEnter = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  /**
   * Handle drag leave
   */
  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  /**
   * Handle drag over
   */
  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
  }

  /**
   * Handle drop
   */
  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)

    // Get dropped file
    const file = e.dataTransfer.files?.[0]
    if (file) {
      handleUpload(file)
    }
  }

  /**
   * Trigger file input click
   */
  const handleBrowseClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <Card className="shadow-large border-border/50 hover:shadow-enterprise transition-all duration-300 bg-white">
      {/* Card Header */}
      <CardHeader className="space-y-2">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center">
            <Upload className="h-5 w-5 text-primary" />
          </div>
          <div>
            <CardTitle className="text-xl font-semibold">Upload Document</CardTitle>
            <CardDescription className="text-sm">
              Drag & drop or browse to upload PDF, DOCX, or TXT files
            </CardDescription>
          </div>
        </div>
      </CardHeader>

      {/* Card Content */}
      <CardContent>
        {/* Hidden file input */}
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,.doc,.txt"
          onChange={handleFileChange}
          className="hidden"
        />

        {/* Premium Drop Zone */}
        <div
          onDragEnter={handleDragEnter}
          onDragLeave={handleDragLeave}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          className={`
            relative border-2 border-dashed rounded-2xl p-10 text-center
            transition-all duration-300 ease-out group
            ${isDragging
              ? 'border-primary bg-gradient-to-br from-primary/5 to-primary/10 scale-[1.01] shadow-lg'
              : 'border-border hover:border-primary/50 hover:bg-accent/30'
            }
            ${isUploading ? 'opacity-60 pointer-events-none' : 'cursor-pointer'}
          `}
          onClick={!isUploading ? handleBrowseClick : undefined}
        >
          {/* Icon with gradient background */}
          <div className="flex justify-center mb-6">
            <div className={`
              h-16 w-16 rounded-2xl flex items-center justify-center transition-all duration-300
              ${isDragging
                ? 'bg-gradient-to-br from-primary to-primary-hover shadow-lg scale-110'
                : 'bg-gradient-to-br from-muted to-muted/50 group-hover:from-primary/10 group-hover:to-primary/5'
              }
            `}>
              {isUploading ? (
                <Loader2 className="h-8 w-8 text-primary animate-spin" />
              ) : (
                <Upload className={`h-8 w-8 transition-colors ${isDragging ? 'text-white' : 'text-primary'}`} />
              )}
            </div>
          </div>

          {/* Text with better typography */}
          <div className="space-y-3">
            <p className="text-base font-semibold text-foreground">
              {isUploading
                ? 'Processing your document...'
                : isDragging
                ? 'Drop it like it\'s hot!'
                : 'Drop your document here'
              }
            </p>
            {!isUploading && (
              <p className="text-sm text-muted-foreground font-medium">
                or click anywhere to browse
              </p>
            )}
          </div>

          {/* Supported formats with pills */}
          <div className="mt-6 flex items-center justify-center gap-2 flex-wrap">
            {['PDF', 'DOCX', 'TXT'].map((format) => (
              <span
                key={format}
                className="px-3 py-1 rounded-lg bg-muted/50 text-xs font-medium text-muted-foreground border border-border/50"
              >
                {format}
              </span>
            ))}
            <span className="px-3 py-1 rounded-lg bg-accent/50 text-xs font-medium text-accent-foreground border border-primary/20">
              Max 10MB
            </span>
          </div>
        </div>

        {/* Success Message - Modern Alert */}
        {successMessage && !uploadError && (
          <div className="mt-5 flex items-start gap-3 p-4 rounded-xl bg-success/5 border border-success/20 fade-in">
            <div className="h-8 w-8 rounded-lg bg-success/10 flex items-center justify-center flex-shrink-0">
              <CheckCircle2 className="h-5 w-5 text-success" />
            </div>
            <div className="flex-1 pt-0.5">
              <p className="text-sm font-medium text-success">Upload Successful</p>
              <p className="text-sm text-success/80 mt-0.5">{successMessage}</p>
            </div>
          </div>
        )}

        {/* Error Message - Modern Alert */}
        {uploadError && (
          <div className="mt-5 flex items-start gap-3 p-4 rounded-xl bg-destructive/5 border border-destructive/20 fade-in">
            <div className="h-8 w-8 rounded-lg bg-destructive/10 flex items-center justify-center flex-shrink-0">
              <AlertCircle className="h-5 w-5 text-destructive" />
            </div>
            <div className="flex-1 pt-0.5">
              <p className="text-sm font-medium text-destructive">Upload Failed</p>
              <p className="text-sm text-destructive/80 mt-0.5">{uploadError}</p>
            </div>
          </div>
        )}

        {/* Premium Browse Button */}
        <div className="mt-6">
          <Button
            variant="outline"
            size="lg"
            className="w-full font-medium shadow-soft hover:shadow-medium transition-all hover:-translate-y-0.5"
            onClick={handleBrowseClick}
            disabled={isUploading}
          >
            {isUploading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Uploading Document...
              </>
            ) : (
              <>
                <FileText className="mr-2 h-5 w-5" />
                Select Files to Upload
              </>
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
