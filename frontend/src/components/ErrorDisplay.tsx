import { AppError } from "@/lib/api"

interface ErrorDisplayProps {
    error: AppError
}

export function ErrorDisplay({ error }: ErrorDisplayProps) {
    const getErrorConfig = () => {
        switch (error.type) {
            case 'validation_error':
                return {
                    title: 'Input Validation Error',
                    bgColor: 'bg-red-50/100',
                    borderColor: 'border-red-200',
                    iconColor: 'text-red-400',
                    titleColor: 'text-red-800',
                    messageColor: 'text-red-700',
                    buttonColor: 'text-red-800 hover:text-red-900',
                }
            case 'service_error':
                return {
                    title: 'Service Unavailable',
                    bgColor: 'bg-orange-50',
                    borderColor: 'border-orange-200',
                    iconColor: 'text-orange-400',
                    titleColor: 'text-orange-800',
                    messageColor: 'text-orange-700',
                    buttonColor: 'text-orange-800 hover:text-orange-900',
                }
            default:
                return {
                    title: 'Error',
                    bgColor: 'bg-gray-50',
                    borderColor: 'border-gray-200',
                    iconColor: 'text-gray-400',
                    titleColor: 'text-gray-800',
                    messageColor: 'text-gray-700',
                    buttonColor: 'text-gray-800 hover:text-gray-900',
                }
        }
    }

    const config = getErrorConfig()

    return (
        <div className={`${config.bgColor} border ${config.borderColor} rounded-lg p-4 mb-4`}>
            <div className="flex items-center justify-center">
                <div className="flex-shrink-0">
                    <svg className={`h-5 w-5 ${config.iconColor}`} viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                </div>
                <div className="ml-3 flex-1">
                    <h3 className={`text-sm font-medium ${config.titleColor}`}>
                        {config.title}
                    </h3>
                    <p className={`text-sm ${config.messageColor} mt-1`}>
                        {error.message}
                    </p>
                </div>
            </div>
        </div>
    )
}