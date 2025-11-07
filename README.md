# CredibleMe - Digital Credibility Verification

A privacy-friendly prototype for the **Gemini Buildathon** under **The Identity Web** theme. CredibleMe allows users to upload or link their digital credentials (Resume, GitHub, LinkedIn) and uses **Gemini 1.5 Flash** to generate a trustworthiness score and summary reasoning.

## 🎯 Project Overview

CredibleMe is a web application that analyzes the consistency between a user's resume, GitHub profile, and LinkedIn profile to generate a trustworthiness score. The application uses AI-powered analysis to verify digital credibility without storing any data in a database.

## 🏗️ System Architecture

The application follows a simple 5-layer structure with no persistent data:

1. **User Layer** – Input form for resume / GitHub / LinkedIn
2. **Frontend (HTML + Tailwind CSS)** – Handles UI and sends data to backend
3. **Backend (FastAPI)** – Receives data and queries Gemini API
4. **AI Reasoning (Gemini 1.5 Flash)** – Compares data sources, generates consistency reasoning + trust score
5. **Output Layer** – Displays the result (score + explanation + mock verification badge)

## ⚙️ Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: HTML + Jinja2 Templates + Tailwind CSS (via CDN)
- **AI Integration**: Gemini 1.5 Flash via Google AI Studio API
- **Auth**: Mock Google OAuth button (no real login)
- **Storage**: None — just in-memory (session) data

## 📁 Project Structure

```
credibleme-prototype/
├── backend/
│   ├── main.py              # FastAPI application with routes
│   ├── gemini_client.py     # Gemini API integration
│   ├── requirements.txt     # Python dependencies
│   ├── templates/           # HTML templates (Jinja2)
│   │   ├── index.html       # Landing page
│   │   ├── verify.html      # Verification form
│   │   ├── result.html      # Result display
│   │   └── error.html       # Error page
│   └── static/              # Static files (CSS/JS)
├── .env.example             # Environment variables template
└── README.md                # This file
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd credibleme-prototype/backend
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (optional)**
   ```bash
   cp ../.env.example .env
   ```
   
   Edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
   
   > **Note**: You can get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   >
   > If you don't set the API key, the app will use mock responses for testing.

5. **Run the application**
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the application**
   Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## 💻 Features

### Frontend Pages

- **`/`** - Landing page with welcome message and feature overview
- **`/verify`** - Form for submitting:
  - Resume content (text input)
  - GitHub username
  - LinkedIn URL
  - "Verify Credibility" button
- **`/result/{session_id}`** - Displays AI reasoning and trust score

### Backend Endpoints

- **`POST /verify`** - Form submission endpoint (redirects to result page)
- **`POST /api/verify`** - JSON API endpoint (returns JSON response)
- **`GET /api/result/{session_id}`** - Retrieve verification result by session ID

## 🧠 How It Works

1. **User Input**: User fills out the verification form with resume text, GitHub username, and LinkedIn URL
2. **Data Processing**: Backend receives the data and prepares it for AI analysis
3. **AI Analysis**: Gemini 1.5 Flash analyzes the consistency between:
   - Resume claims and GitHub repositories
   - Professional experience alignment with LinkedIn
   - Overall credibility indicators
4. **Result Generation**: AI returns:
   - Trust score (0-100)
   - Detailed reasoning explanation
   - Verification badge (Verified/Needs Review/Unverified)
5. **Display**: Result is shown to the user with visual indicators

## 🔒 Privacy & Security

- **No Database**: All data is processed in-memory only
- **Session-based**: Results are stored temporarily in memory
- **No Persistence**: Data is not saved to disk or database
- **Privacy-friendly**: Perfect for prototype and demonstration purposes

## 🧪 Testing Without API Key

The application works without a Gemini API key by using mock responses. This allows you to:
- Test the full application flow
- See the UI and user experience
- Develop and debug without API costs

To use real AI analysis, simply add your `GEMINI_API_KEY` to the `.env` file.

## 📝 API Response Format

The verification endpoint returns:

```json
{
  "trust_score": 87,
  "reasoning": "Resume projects match GitHub repositories and LinkedIn skills. Professional experience is consistent across all platforms.",
  "badge": "Verified",
  "session_id": "abc12345"
}
```

## 🎨 UI Features

- **Modern Design**: Clean, responsive UI using Tailwind CSS
- **Progress Indicators**: Visual trust score with progress bar
- **Color-coded Badges**: Green (Verified), Yellow (Needs Review), Red (Unverified)
- **Responsive Layout**: Works on desktop and mobile devices
- **Font Awesome Icons**: Visual icons for better UX

## 🐛 Troubleshooting

### Port Already in Use
If port 8000 is already in use, change it in `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Module Not Found
Make sure you've activated your virtual environment and installed all dependencies:
```bash
pip install -r requirements.txt
```

### API Key Issues
If you get API errors, check:
1. Your API key is correct in `.env`
2. You have internet connection
3. The API key has proper permissions

The app will automatically fall back to mock mode if the API fails.

## 📄 License

This project is built for the Gemini Buildathon - Identity Web Theme.

## 🤝 Contributing

This is a prototype project for the Gemini Buildathon. Feel free to fork and extend it!

## 📧 Support

For issues or questions, please refer to the project documentation or create an issue in the repository.

---

**Built with ❤️ for Gemini Buildathon - Identity Web Theme**

# credible-me
