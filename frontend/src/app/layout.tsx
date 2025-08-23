import type React from "react"
import type { Metadata } from "next"
import { Playfair_Display, Source_Sans_3 } from "next/font/google"
import "./globals.css"
import { BookOpen } from "lucide-react"

const playfair = Playfair_Display({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-playfair",
})

const sourceSans = Source_Sans_3({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-source-sans",
})

export const metadata: Metadata = {
  title: "Cura'an - Spiritual Healing & Guidance",
  description: "Find peace and guidance through Quranic verses tailored to your personal struggles",
  generator: "v0.app",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className={`${playfair.variable} ${sourceSans.variable} antialiased`}>
      <body className="min-h-screen bg-background">
        {/* Header */}
        <header className="border-b border-border bg-card/50 backdrop-blur-sm">
          <div className="container mx-auto px-4 py-6">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-full bg-primary/10">
                <BookOpen className="w-5 h-5 text-primary" />
              </div>
              <div>
                <h1 className="text-2xl font-bold font-serif text-foreground">Cura'an</h1>
                <p className="text-sm text-muted-foreground">Spiritual Healing & Guidance</p>
              </div>
            </div>
          </div>
        </header>
        {children}
        {/* Footer */}
        <footer className="border-t border-border bg-card/30 mt-16">
          <div className="container mx-auto px-4 py-8 text-center">
            <p className="text-muted-foreground text-sm">
              May you find peace, guidance, and healing through divine wisdom.
            </p>
          </div>
        </footer>
      </body>
    </html>
  )
}
