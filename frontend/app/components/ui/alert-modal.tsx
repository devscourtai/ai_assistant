'use client'

import React from 'react'
import { AlertCircle, X } from 'lucide-react'
import { Button } from './button'

interface AlertModalProps {
  isOpen: boolean
  onClose: () => void
  title?: string
  message: string
  variant?: 'info' | 'warning' | 'error'
}

export function AlertModal({
  isOpen,
  onClose,
  title = 'Alert',
  message,
  variant = 'warning',
}: AlertModalProps) {
  if (!isOpen) return null

  const variantStyles = {
    info: 'bg-blue-50 border-blue-200 text-blue-800',
    warning: 'bg-amber-50 border-amber-200 text-amber-800',
    error: 'bg-red-50 border-red-200 text-red-800',
  }

  const iconStyles = {
    info: 'text-blue-600',
    warning: 'text-amber-600',
    error: 'text-red-600',
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative z-10 w-full max-w-md mx-4">
        <div className="bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b">
            <h3 className="text-lg font-semibold">{title}</h3>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
              aria-label="Close"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Content */}
          <div className="p-6">
            <div
              className={`flex items-start gap-3 p-4 rounded-lg border ${variantStyles[variant]}`}
            >
              <AlertCircle
                className={`h-5 w-5 flex-shrink-0 mt-0.5 ${iconStyles[variant]}`}
              />
              <p className="text-sm leading-relaxed">{message}</p>
            </div>
          </div>

          {/* Footer */}
          <div className="flex justify-end gap-2 p-4 border-t bg-gray-50">
            <Button onClick={onClose}>OK</Button>
          </div>
        </div>
      </div>
    </div>
  )
}
