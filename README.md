# 🎂 Birthday Reminder

If u don't like upset your friends and prefer privacy, this repo is for u :D

> ![Example](https://github.com/Collappo/Birthday-Reminder/blob/main/.docs/example.png)
> What it looks like? - example image.

## ✨ Features

- Upcomming birthdays indicator
- TUI
- Stores data in a local CSV file
- Fast and lightweight with modern Python tools
<!-- - Add, edit, and delete birthdays -->
<!-- - Automatic reminders via notifications -->

---

## 🛠️ Installation

> ***Python version: 3.12 or higher***

### Setup Project

1. Clone the repository:

   ```console
   git clone https://github.com/yourusername/birthday-reminder.git
   cd birthday-reminder
   ```

2. Install ***uv***:

   ```console
   pip install uv
   ```

   https://docs.astral.sh/uv/getting-started/installation/

3. Build project:

   ```console
   uv tool install --editable .
   uv tool update-shell
   ```

4. If you have problems, install locally:

   ```console
   uv sync
   ```

---

## Usage

### Windows

Run the application using global command:
```console
birthdays
```

else locally:

```console
$ .venv\Scripts\activate.bat
$ uv run main.py
```

<!-- ### Linux/macOS

Run the application with uv:

```bash
$ uv run main.py
``` -->

---

## 📄 License

This project is licensed under the MIT License.
