# 📬 Email Automation System

Automated daily email summarizer using **LangChain**, **Gemini**, and **Twilio WhatsApp API**.

## 🚀 Overview

This AI-powered assistant fetches your latest emails, summarizes them using Google’s Gemini model, and delivers them as a neatly formatted WhatsApp message — every day, fully automated.

### 🔧 Features

- 🔐 Authenticates with Gmail via OAuth
- 📥 Extracts unread emails
- 🧠 Summarizes content using Gemini Flash
- 📲 Sends summary to WhatsApp using Twilio
- ⚙️ Modular LangChain agent-based design

## 🧠 Tech Stack

- **LangChain** – For agent orchestration  
- **Gemini Flash API** – For fast, concise summarization  
- **Gmail API** – For secure email access  
- **Twilio WhatsApp API** – For message delivery  
- **Python** – Core logic  

## 🛠️ Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/vishnutej05/Email-AI-Agent.git
   cd Email-AI-Agent
2. **Install dependencies**
   ```bash
    pip install -r requirements.txt
3. **Configure .env**
   ```bash
    GOOGLE_CREDENTIALS_PATH=credentials.json
    GEMINI_API_KEY=your_gemini_api_key
    TWILIO_ACCOUNT_SID=your_twilio_sid
    TWILIO_AUTH_TOKEN=your_twilio_token
    TWILIO_FROM=whatsapp:+14155238886
    TWILIO_TO=whatsapp:+91xxxxxxxxxx
4. **Run the agent**
    ```bash
    python email_whatsapp_agent.py


**📚 Structure**
  ```bash
    📁 Email-AI-Agent
    ├── email_whatsapp_agent.py      # Main script
    ├── agents/
    │   ├── extract.py               # Gmail extraction agent
    │   ├── summarize.py             # Gemini summarization agent
    │   └── send.py                  # WhatsApp sender agent
    ├── creds/                       # Gmail OAuth tokens
    ├── .env                         # Environment variables
    └── requirements.txt             # Python dependencie
