import { Loader2 } from "lucide-react";

export default function Loading() {
    return (
        <div className="min-h-screen flex items-center justify-center bg-background">
            <div className="text-center space-y-4">
                <Loader2 className="w-10 h-10 text-primary animate-spin mx-auto" />
                <p className="text-lg text-muted-foreground">Finding the perfect cure for you...</p>
            </div>
        </div>
    )
}
