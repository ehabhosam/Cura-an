import Link from "next/link";
import { Button } from "./ui/button";

export default function StartNewSearch() {
    return <Link href="/" className="inline-block mb-4">
        <Button
            variant="outline"
            className="mb-6 border-primary/20 text-primary hover:bg-primary/5 bg-transparent"
        >
            ← Start New Search
        </Button>
    </Link>
}