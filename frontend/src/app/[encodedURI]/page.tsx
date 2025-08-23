import type React from "react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { ErrorDisplay } from "@/components/ErrorDisplay"
import { apiRequest, AppError } from "@/lib/api"
import { Loader2, Heart, BookOpen, Sparkles } from "lucide-react"
import { Suspense } from "react"
import Link from "next/link"
import StartNewSearch from "@/components/StartNewSearch"

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

export default async function CuraanApp({
    params,
}: {
    params: Promise<{ encodedURI: string }>
}) {

    const { encodedURI } = await params
    const issue = decodeURIComponent(encodedURI || "")

    let result: TherapyResult

    try {
        const requestObj = {
            method: "POST",
            body: JSON.stringify({ issue: issue.trim(), k: 3 }),
        }
        result = await apiRequest<TherapyResult>("http://localhost:3000/api/therapy-search", requestObj)
    } catch (error) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-background">
                <div className="text-center space-y-4">
                    <ErrorDisplay
                        error={
                            error instanceof AppError
                                ? error
                                : new AppError(
                                    error instanceof Error
                                        ? error.message
                                        : "Something went wrong",
                                    'internal_error'
                                )
                        }
                    />
                    <StartNewSearch />
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-background">
            <Suspense fallback={<VersesLoading />} >
                <main className="container mx-auto px-4 py-8 max-w-4xl">
                    <div className="space-y-8">
                        <div className="text-center">
                            <StartNewSearch />
                            <h2 className="text-3xl font-bold font-serif text-foreground mb-2">Divine Guidance for Your Heart</h2>
                            {/* <p className="text-muted-foreground">
                            Here are verses that speak to your concern: "{result.search_query}"
                        </p> */}
                        </div>

                        {/* AI Response
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
                        </Card> */}

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
                </main>
            </Suspense>
        </div>
    )
}

const VersesLoading = () => (
    <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center space-y-4">
            <Loader2 className="w-10 h-10 text-primary animate-spin mx-auto" />
            <p className="text-lg text-muted-foreground">Finding the perfect cure for you...</p>
        </div>
    </div>
)