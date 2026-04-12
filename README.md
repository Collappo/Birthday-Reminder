# 🎂 Birthday Reminder

If u don't like upset your friends and prefer privacy, this repo is for u :D

[Example](.docs\example.png)

## ✨ Features

- Upcomming birthdays indicator
- CLI
- Stores data in a local CSV file
- Fast and lightweight with modern Python tools
<!-- - Add, edit, and delete birthdays -->
<!-- - Automatic reminders via notifications -->

---

## 🛠️ Installation

> ***Python version: 3.12 or higher***

### Setup Project

Optional way, install fast uv:

```bash
$ pip install uv
```

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/birthday-reminder.git
   cd birthday-reminder
   ```

2. Install dependencies:
   ```bash
   # if you have uv
   $ uv sync

   # or

   $ pip install .
   ```

---

## Usage

### Windows

Run the application using this script, if you have *uv*:
```console
$ birthdays
```

else:

```console
$ .venv\Scripts\activate.bat
$ python main.py
```

### Linux/macOS

Run the application with uv:

```bash
$ uv run main.py
```

---

## 📄 License

This project is licensed under the MIT License.