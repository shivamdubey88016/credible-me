import Head from 'next/head'
import Link from 'next/link'

export default function Home() {
  return (
    <>
      <Head>
        <title>CredibleMe - Verify Your Digital Credibility</title>
        <meta name="description" content="Privacy-friendly credential verification using AI" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4">
        <div className="max-w-4xl w-full text-center">
          {/* Hero Section */}
          <div className="mb-12">
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-4">
              Welcome to <span className="text-primary-600">CredibleMe</span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-700 mb-8">
              Verify your digital credibility with AI-powered analysis
            </p>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-12">
              Upload your resume, connect your GitHub and LinkedIn profiles, and get an instant 
              trustworthiness score powered by Gemini AI. Privacy-friendly, no database required.
            </p>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="text-4xl mb-4">📄</div>
              <h3 className="text-xl font-semibold mb-2">Resume Analysis</h3>
              <p className="text-gray-600">
                Upload or paste your resume for comprehensive analysis
              </p>
            </div>
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="text-4xl mb-4">🔗</div>
              <h3 className="text-xl font-semibold mb-2">Profile Integration</h3>
              <p className="text-gray-600">
                Connect your GitHub and LinkedIn profiles seamlessly
              </p>
            </div>
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-xl font-semibold mb-2">AI-Powered</h3>
              <p className="text-gray-600">
                Powered by Gemini 1.5 Flash for accurate verification
              </p>
            </div>
          </div>

          {/* CTA Button */}
          <div className="flex justify-center gap-4">
            <Link
              href="/verify"
              className="bg-primary-600 hover:bg-primary-700 text-white font-semibold py-4 px-8 rounded-lg text-lg shadow-lg transform transition hover:scale-105"
            >
              Get Started →
            </Link>
          </div>

          {/* Info Section */}
          <div className="mt-16 bg-white/80 rounded-lg p-6 max-w-2xl mx-auto">
            <h2 className="text-2xl font-semibold mb-4">How It Works</h2>
            <ol className="text-left space-y-3 text-gray-700">
              <li className="flex items-start">
                <span className="font-bold text-primary-600 mr-2">1.</span>
                <span>Enter your resume content, GitHub username, and LinkedIn URL</span>
              </li>
              <li className="flex items-start">
                <span className="font-bold text-primary-600 mr-2">2.</span>
                <span>Our AI analyzes consistency across all your credentials</span>
              </li>
              <li className="flex items-start">
                <span className="font-bold text-primary-600 mr-2">3.</span>
                <span>Receive a trust score and detailed reasoning report</span>
              </li>
            </ol>
          </div>
        </div>
      </main>
    </>
  )
}

