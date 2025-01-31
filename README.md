# 📌 TO-DO Telegram Bot

🚀 A powerful and easy-to-use Telegram bot for managing your to-do list, built with Aiogram 3.

## ✨ Features

✅ Add, remove, and list tasks effortlessly  
✅ Mark tasks as completed with a single command  
✅ Persistent storage using SQLite – your tasks are safe!  
✅ Inline buttons for intuitive task management  
✅ Fast and lightweight – perfect for personal use!

---

## 🛠 Installation

### 📦 Using Docker

1. Clone the repository:
   ```sh
   git clone https://github.com/crissyro/TO-DO-telegram-bot.git
   cd TO-DO-telegram-bot
   ```
2. Build and run the Docker container:
   ```sh
   docker build -t todo-bot .
   docker run -d --name todo-bot -v $(pwd)/todo.db:/app/todo.db todo-bot
   ```

### 🏗 Manual Setup

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Set up environment variables (if needed):
   ```sh
   export BOT_TOKEN=your_telegram_bot_token
   ```
3. Run the bot:
   ```sh
   python bot.py
   ```

---

## 🎯 Usage

🔹 `/add <task>` – Add a new task  
🔹 `/list` – Show all tasks  
🔹 `/done <task>` – Mark a task as completed  
🔹 `/remove <task>` – Remove a task  
🔹 `/help` – Show available commands  

---

## 📋 Requirements

- 🐍 Python 3.12
- 🤖 Aiogram 3
- 🗄 SQLite (built-in database)

---

## 🤝 Contributing

We welcome contributions! Please check out [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to get started.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

💡 **Created with ❤️ to help you stay organized!**
