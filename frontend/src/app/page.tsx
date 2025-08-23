import type React from "react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Heart, BookOpen, Sparkles } from "lucide-react"
import { redirect } from "next/navigation"

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
  async function submitFormAction(formData: FormData) {
    "use server"
    const issue = formData.get("issue") as string
    if (!issue?.trim()) return

    // navigate to results page /<issue>
    redirect(`/${encodeURIComponent(issue.trim())}`)
  }

  return (
    <div className="min-h-screen bg-background">
      <main className="container mx-auto px-4 py-8 max-w-4xl">
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
              <form action={submitFormAction} className="space-y-6">
                <div className="space-y-2">
                  <Textarea
                    name="issue"
                    placeholder="Describe what's weighing on your heart... (e.g., 'I feel anxious about my future', 'I'm struggling with loneliness', 'I need guidance and peace')"
                    className="min-h-32 resize-none border-border/50 focus:border-primary/50 focus:ring-primary/20"
                  />
                </div>

                <Button
                  type="submit"
                  className="w-full bg-primary hover:bg-primary/90 text-primary-foreground"
                >
                  <Heart className="w-4 h-4 mr-2" />
                  Find Cure
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
