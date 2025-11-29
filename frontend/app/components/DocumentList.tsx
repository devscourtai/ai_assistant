/**
 * DocumentList Component
 *
 * Displays a list of uploaded documents with their metadata.
 * Shows document name, chunks created, and upload date.
 *
 * Features:
 * - Displays documents in a clean card layout
 * - Shows empty state when no documents
 * - Automatically refreshes when new documents are uploaded
 */

'use client'

import React, { useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { useApp } from '../context/AppContext'
import { formatDate } from '../lib/utils'
import { FileText, Package } from 'lucide-react'

export function DocumentList() {
  // Access global state and actions from context
  const { documents, totalDocuments, refreshStats } = useApp()

  // Fetch stats when component mounts
  useEffect(() => {
    refreshStats()
  }, [refreshStats])

  return (
    <Card className="shadow-large border-border/50 hover:shadow-enterprise transition-all duration-300 bg-white sticky top-24">
      {/* Card Header - Premium Design */}
      <CardHeader className="space-y-3">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center">
            <Package className="h-5 w-5 text-primary" />
          </div>
          <div className="flex-1">
            <CardTitle className="text-xl font-semibold">Documents</CardTitle>
            <CardDescription className="text-sm">
              {totalDocuments === 0
                ? 'No documents yet'
                : `${totalDocuments} ${totalDocuments === 1 ? 'document' : 'documents'} uploaded`
              }
            </CardDescription>
          </div>
        </div>

        {/* Stats Badge */}
        {totalDocuments > 0 && (
          <div className="pt-2 border-t border-border/50">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-accent/50 border border-primary/20">
              <div className="h-2 w-2 rounded-full bg-success animate-pulse"></div>
              <span className="text-xs font-medium text-foreground">Collection Active</span>
            </div>
          </div>
        )}
      </CardHeader>

      {/* Card Content */}
      <CardContent>
        {/* Empty State - Premium Design */}
        {documents.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <div className="h-20 w-20 rounded-2xl bg-gradient-to-br from-muted to-muted/50 flex items-center justify-center mb-5">
              <FileText className="h-10 w-10 text-muted-foreground/40" />
            </div>
            <h3 className="font-semibold text-base text-foreground mb-2">No Documents Yet</h3>
            <p className="text-sm text-muted-foreground max-w-[250px] leading-relaxed">
              Upload your first document to start building your AI knowledge base
            </p>
          </div>
        ) : (
          /* Document List - Premium Cards */
          <div className="space-y-2.5 max-h-[600px] overflow-y-auto pr-1">
            {documents.map((doc) => (
              <div
                key={doc.document_id}
                className="group relative flex items-start gap-3 p-4 rounded-xl border border-border bg-white hover:border-primary/30 hover:shadow-medium transition-all duration-200 card-hover"
              >
                {/* File Icon with Gradient */}
                <div className="flex-shrink-0">
                  <div className="h-11 w-11 rounded-xl bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center group-hover:scale-105 transition-transform">
                    <FileText className="h-5 w-5 text-primary" />
                  </div>
                </div>

                {/* Document Info */}
                <div className="flex-1 min-w-0">
                  {/* Filename with truncation */}
                  <h4 className="font-semibold text-sm text-foreground truncate mb-1">
                    {doc.filename}
                  </h4>

                  {/* Metadata Pills */}
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-muted/50 text-muted-foreground border border-border/50">
                      {doc.chunks_created} {doc.chunks_created === 1 ? 'chunk' : 'chunks'}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {formatDate(doc.uploaded_at)}
                    </span>
                  </div>
                </div>

                {/* Status Badge - Premium */}
                <div className="flex-shrink-0">
                  <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-success/10 text-success border border-success/20">
                    <div className="h-1.5 w-1.5 rounded-full bg-success"></div>
                    Ready
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
