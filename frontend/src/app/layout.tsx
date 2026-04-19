import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'StyleStep AI (2026 Edition)',
  description: 'Professional-grade fashion coordination powered by CAM16-UCS Color Science.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-black text-white font-sans selection:bg-primary/30">
        {children}
      </body>
    </html>
  )
}
