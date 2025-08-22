import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
    try {
        const body = await request.json()
        const { issue, k = 3 } = body

        if (!issue || typeof issue !== "string") {
            return NextResponse.json({
                success: false,
                error: {
                    message: "Issue is required and must be a string",
                    type: "validation_error"
                }
            }, { status: 400 })
        }

        // Forward the request to the Python Flask backend
        const response = await fetch("http://localhost:5000/api/therapy-search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ issue: issue.trim(), k }),
        })

        const data = await response.json()

        // Flask now returns consistent response structure, just pass it through
        return NextResponse.json(data, { status: response.status })

    } catch (error) {
        console.error("Therapy search error:", error)
        return NextResponse.json({
            success: false,
            error: {
                message: "Internal server error",
                type: "internal_error"
            }
        }, { status: 500 })
    }
}