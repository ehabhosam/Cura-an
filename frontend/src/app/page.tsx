"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { ErrorDisplay } from "@/components/ErrorDisplay"
import { apiRequest, AppError } from "@/lib/api"
import { Loader2, Heart, BookOpen, Sparkles } from "lucide-react"

interface TherapyResult {
  ai_response: string
  search_query: string
  results: Array<{
    id: string
    score: number
    verse_en: string
    verse_ar: string
    text?: string
  }>
}

export default function CuraanApp() {
  const [issue, setIssue] = useState("")
  const [result, setResult] = useState<TherapyResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<AppError | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!issue.trim()) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await apiRequest<TherapyResult>("/api/therapy-search", {
        method: "POST",
        body: JSON.stringify({ issue: issue.trim(), k: 3 }),
      })

      setResult(data)
    } catch (err) {
      if (err instanceof AppError) {
        setError(err)
      } else {
        setError(new AppError(
          err instanceof Error ? err.message : "Something went wrong",
          'internal_error'
        ))
      }
    } finally {
      setLoading(false)
    }
  }

  const handleNewSearch = () => {
    setIssue("")
    setResult(null)
    setError(null)
  }

  const handleTextInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setIssue(e.target.value)
    if (error) setError(null) // Clear error (if it exists) when user starts typing
  }

  return (
    <div className="min-h-screen bg-background">
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

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {!result ? (
          /* Welcome Screen */
          <div className="text-center space-y-8">
            <div className="space-y-4">
              <h2 className="text-4xl font-bold font-serif text-foreground">Find Peace in Divine Guidance</h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto leading-relaxed">
                Share what's troubling your heart, and discover healing verses from the Quran that speak directly to
                your situation. Let divine wisdom guide you toward peace and understanding.
              </p>
            </div>

            <Card className="max-w-2xl mx-auto shadow-lg border-border/50">
              <CardHeader className="text-center pb-4">
                <CardTitle className="text-xl font-serif text-foreground flex items-center justify-center gap-2">
                  <Sparkles className="w-5 h-5 text-primary" />
                  Share Your Concern
                </CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="space-y-2">
                    <Textarea
                      value={issue}
                      onChange={handleTextInputChange}
                      placeholder="Describe what's weighing on your heart... (e.g., 'I feel anxious about my future', 'I'm struggling with loneliness', 'I need guidance and peace')"
                      className="min-h-32 resize-none border-border/50 focus:border-primary/50 focus:ring-primary/20"
                      disabled={loading}
                    />
                  </div>

                  {error && (
                    <ErrorDisplay
                      error={error}
                    />
                  )}                  <Button
                    type="submit"
                    disabled={!issue.trim() || loading}
                    className="w-full h-12 text-base font-medium bg-primary hover:bg-primary/90 text-primary-foreground"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Finding Guidance...
                      </>
                    ) : (
                      <>
                        <Heart className="w-4 h-4 mr-2" />
                        Seek Divine Guidance
                      </>
                    )}
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>
        ) : (
          /* Results Screen */
          <div className="space-y-8">
            <div className="text-center">
              <Button
                onClick={handleNewSearch}
                variant="outline"
                className="mb-6 border-primary/20 text-primary hover:bg-primary/5 bg-transparent"
              >
                ← Start New Search
              </Button>
              <h2 className="text-3xl font-bold font-serif text-foreground mb-2">Divine Guidance for Your Heart</h2>
              <p className="text-muted-foreground">
                Here are verses that speak to your concern: "{result.search_query}"
              </p>
            </div>

            {/* AI Response */}
            <Card className="shadow-lg border-primary/10 bg-gradient-to-br from-primary/5 to-accent/5">
              <CardHeader>
                <CardTitle className="text-xl font-serif text-foreground flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-primary" />
                  Healing Message
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-foreground leading-relaxed text-lg">{result.ai_response}</p>
              </CardContent>
            </Card>

            {/* Quranic Verses */}
            <div className="space-y-6">
              <h3 className="text-2xl font-bold font-serif text-foreground text-center">Verses for Reflection</h3>

              {result.results.map((verse, index) => (
                <Card key={verse.id} className="shadow-md border-border/50 hover:shadow-lg transition-shadow">
                  <CardHeader className="pb-4">
                    <CardTitle className="text-lg font-serif text-foreground flex items-center justify-between">
                      <span className="flex items-center gap-2">
                        <BookOpen className="w-4 h-4 text-primary" />
                        {verse.id}
                      </span>
                      <span className="text-sm font-normal text-muted-foreground">
                        Relevance: {(verse.score * 100).toFixed(0)}%
                      </span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {/* Arabic Text */}
                    <div className="text-right p-4 bg-muted/30 rounded-lg">
                      <p className="text-xl leading-loose text-foreground font-medium" dir="rtl">
                        {verse.verse_ar}
                      </p>
                    </div>

                    {/* English Translation */}
                    <div className="p-4 bg-card rounded-lg border border-border/30">
                      <p className="text-foreground leading-relaxed">{verse.verse_en || verse.text}</p>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Reflection Prompt */}
            <Card className="shadow-lg border-accent/20 bg-gradient-to-br from-accent/5 to-primary/5">
              <CardContent className="pt-6">
                <div className="text-center space-y-3">
                  <Heart className="w-8 h-8 text-primary mx-auto" />
                  <h4 className="text-lg font-serif font-semibold text-foreground">Take a Moment to Reflect</h4>
                  <p className="text-muted-foreground leading-relaxed">
                    Let these divine words settle in your heart. Consider how they apply to your situation and what
                    guidance they offer for your path forward.
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-border bg-card/30 mt-16">
        <div className="container mx-auto px-4 py-8 text-center">
          <p className="text-muted-foreground text-sm">
            May you find peace, guidance, and healing through divine wisdom.
          </p>
        </div>
      </footer>
    </div>
  )
}
