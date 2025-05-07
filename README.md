# 🧠 Auto Index Bot

A powerful and lightweight Telegram bot built with **Pyrogram** that automatically indexes files (like anime episodes or documents), allows users to search by filename, and provides a simple admin control system. Ideal for content-based Telegram channels (especially anime!).

---

## ✨ Features

- 📁 **Auto File Indexing** — Instantly indexes all files sent to the bot.
- 🔍 **Search System** — Users can search indexed files by name.
- 👮‍♂️ **Admin Panel** — Add/remove admins, control banned users.
- 📊 **Stats Command** — View file count, user stats, admin list.
- 🔐 **Ban System** — Block abusive users quickly.
- ⚡ **MongoDB Backend** — Stable, fast, and scalable.

---

## 🛠 Requirements

- Python 3.9+
- Telegram Bot Token
- MongoDB (Atlas or local)
- Pyrogram v2.x
- TgCrypto

---

## 🔧 Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/FraxxShadow/auto-index-bot.git
   cd Auto-Index-Bot
2. **Install Requirements**
   ```bash
   pip install -r requirements.txt
3. **Configure config.py**
   ```bash
   nano config.py
4. **Run the Bot**
   ```bash
   python3 main.py

# 📂 Project Structure
```bash
auto-index-bot/
│
├── main.py          # Bot logic and handlers
├── config.py        # Configuration values
├── database.py      # MongoDB interaction
├── requirements.txt # Python dependencies
└── README.md        # Project info
