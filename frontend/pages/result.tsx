import { useEffect, useState } from 'react'
import Head from 'next/head'
import { useRouter } from 'next/router'
import Link from 'next/link'
import ResultCard from '../components/ResultCard'

interface VerificationResult {
  trust_score: number
  reasoning: string
  badge: string
  session_id?: string
}

export default function Result() {
  const router = useRouter()
  const { sessionId } = router.query
  const [result, setResult] = useState<VerificationResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchResult = async () => {
      if (!sessionId) {
        setError('No session ID provided')
        setLoading(false)
        return
      }

      try {
        const response = await fetch(
          `http://localhost:8000/api/result/${sessionId}`
        )

        if (!response.ok) {
          throw new Error('Failed to fetch result')
        }

        const data = await response.json()
        setResult(data)
      } catch (err) {
        setError('Failed to load verification result')
        console.error('Error:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchResult()
  }, [sessionId])

  if (loading) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your results...</p>
        </div>
      </main>
    )
  }

  if (error || !result) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4">
        <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
          <div className="text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Error</h1>
          <p className="text-gray-600 mb-6">{error || 'Result not found'}</p>
          <Link
            href="/verify"
            className="bg-primary-600 hover:bg-primary-700 text-white font-semibold py-2 px-6 rounded-lg inline-block"
          >
            Try Again
          </Link>
        </div>
      </main>
    )
  }

  return (
    <>
      <Head>
        <title>Verification Result - CredibleMe</title>
        <meta name="description" content="Your credential verification results" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="mb-8 text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              Verification Complete
            </h1>
            <p className="text-gray-600">
              Your digital credibility analysis results
            </p>
          </div>

          <ResultCard result={result} />

          <div className="mt-8 text-center">
            <Link
              href="/verify"
              className="text-primary-600 hover:text-primary-700 font-semibold"
            >
              ← Verify Another Profile
            </Link>
          </div>
        </div>
      </main>
    </>
  )
}

