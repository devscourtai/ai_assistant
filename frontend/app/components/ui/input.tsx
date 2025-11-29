/**
 * Input Component
 *
 * A styled input field component that matches our design system.
 *
 * Usage:
 * ```tsx
 * <Input
 *   type="text"
 *   placeholder="Enter your question..."
 *   value={value}
 *   onChange={(e) => setValue(e.target.value)}
 * />
 * ```
 */

import * as React from "react"
import { cn } from "@/app/lib/utils"

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

/**
 * Input component
 * Styled text input with focus states and proper spacing
 */
const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          // Base styles
          "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm",
          // Focus styles
          "ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
          // Disabled styles
          "disabled:cursor-not-allowed disabled:opacity-50",
          // Placeholder styles
          "placeholder:text-muted-foreground",
          // File input styles
          "file:border-0 file:bg-transparent file:text-sm file:font-medium",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"

export { Input }
