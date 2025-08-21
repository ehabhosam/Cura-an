import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
    try {
        const body = await request.json()
        const { issue, k = 3 } = body

        if (!issue || typeof issue !== "string") {
            return NextResponse.json({ error: "Issue is required and must be a string" }, { status: 400 })
        }

        // Forward the request to the Python Flask backend
        const response = await fetch("http://localhost:5000/api/therapy-search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ issue: issue.trim(), k }),
        })

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}))
            return NextResponse.json({ error: errorData.error || "Backend service unavailable" }, { status: response.status })
        }

        const data = await response.json()
        return NextResponse.json(data)
    } catch (error) {
        console.error("Therapy search error:", error)
        return NextResponse.json({ error: "Internal server error" }, { status: 500 })
    }
}
