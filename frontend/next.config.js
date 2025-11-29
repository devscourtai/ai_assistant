/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable React strict mode for better error handling during development
  reactStrictMode: true,

  // Disable the X-Powered-By header for security
  poweredByHeader: false,

  // Optionally add environment variables
  env: {
    // Backend API URL - change this to match your backend
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  }
}

module.exports = nextConfig
