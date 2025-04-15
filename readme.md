# 🤖 Telegram Sports Betting Bot for Cuba 🇨🇺

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4+-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-1.73.0-blueviolet.svg)

A sophisticated Telegram bot for managing sports bets among users in Cuba, featuring AI-powered recommendations and real-time sports data.

## 🚀 Features

- 🏈 Multi-sport betting system (Baseball, Boxing, Football)
- 💳 Virtual balance management
- 🧠 AI-powered betting suggestions (OpenAI integration)
- 📊 Real-time odds and statistics
- 🔄 Transaction history tracking
- 🛡️ Admin moderation tools
- 🌐 API integration with sports data providers

## 🛠️ Tech Stack

| Component        | Technology |
|------------------|------------|
| Backend Framework | Flask      |
| Telegram API     | python-telegram-bot |
| Database ORM     | SQLAlchemy |
| AI Integration   | OpenAI     |
| HTTP Requests   | Requests   |

## � Installation

```bash
# Clone repository
git clone https://github.com/yourusername/cuba-sports-bot.git
cd cuba-sports-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Execute
gunicorn -w 4 -k gevent --reload -b 0.0.0.0:5000 api:app # Linux
waitress-serve --listen=0.0.0.0:5000 api:app # Windows