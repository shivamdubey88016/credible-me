import { useState } from 'react'
import Head from 'next/head'
import { useRouter } from 'next/router'
import VerifyForm from '../components/VerifyForm'

export default function Verify() {
  const router = useRouter()
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (formData: {
    resumeText: string
    githubUsername: string
    linkedinUrl: string
  }) => {
    setIsSubmitting(true)
    
    try {
      const response = await fetch('http://localhost:8000/api/verify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          resume_text: formData.resumeText,
          github_username: formData.githubUsername,
          linkedin_url: formData.linkedinUrl,
        }),
      })

      if (!response.ok) {
        throw new Error('Verification failed')
      }

      const result = await response.json()
      
      // Navigate to result page with session ID
      router.push(`/result?sessionId=${result.session_id}`)
    } catch (error) {
      console.error('Error:', error)
      alert('Failed to verify credentials. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <>
      <Head>
        <title>Verify Credentials - CredibleMe</title>
        <meta name="description" content="Verify your digital credentials" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
        <div className="max-w-3xl mx-auto">
          <div className="mb-8 text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              Verify Your Credentials
            </h1>
            <p className="text-gray-600">
              Enter your information below to get your trustworthiness score
            </p>
          </div>

          <VerifyForm onSubmit={handleSubmit} isSubmitting={isSubmitting} />
        </div>
      </main>
    </>
  )
}

