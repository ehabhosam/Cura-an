/**
 * Standard API response types and error handling utilities
 */

export interface APIError {
    message: string
    type: 'validation_error' | 'internal_error' | 'service_error' | 'not_found'
    details?: Record<string, any>
}

export interface APIResponse<T = any> {
    success: boolean
    message: string
    data?: T
    error?: APIError
}

export class AppError {
    constructor(
        public message: string,
        public type: APIError['type'],
        public details?: Record<string, any>
    ) { }

    isValidationError(): boolean {
        return this.type === 'validation_error'
    }

    isInternalError(): boolean {
        return this.type === 'internal_error'
    }

    isServiceError(): boolean {
        return this.type === 'service_error'
    }
}

/**
 * Parse API response and throw AppError if failed
 */
export async function handleAPIResponse<T>(response: Response): Promise<T> {
    const data: APIResponse<T> = await response.json()

    if (!data.success && data.error) {
        throw new AppError(data.error.message, data.error.type, data.error.details)
    }

    if (!data.success) {
        throw new AppError('Unknown error occurred', 'internal_error')
    }

    return data.data as T
}

/**
 * Fetch wrapper that handles API responses consistently
 */
export async function apiRequest<T>(
    url: string,
    options?: RequestInit
): Promise<T> {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options?.headers,
            },
            ...options,
        })

        return await handleAPIResponse<T>(response)
    } catch (error) {
        if (error instanceof AppError) {
            throw error
        }

        // Network or other errors
        throw new AppError(
            error instanceof Error ? error.message : 'Network error occurred',
            'internal_error'
        )
    }
}
