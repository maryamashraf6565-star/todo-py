# Todo App

A desktop task management application built with Python and PyQt6.  
Create multiple lists, add tasks with priorities and deadlines, and persist data locally.

## Features

- ✅ Create, rename, delete todo lists
- ✅ Add tasks with:
  - Title & description
  - Priority (High/Medium/Low) with color coding
  - Deadline (date picker)
- ✅ Sort tasks by priority
- ✅ Mark tasks as done (removes from list automatically)
- ✅ Persistent storage in JSON format
- ✅ Clean PyQt6 GUI with sidebar navigation

## Project Structure
todo-py/
├── src/
│ ├── main.py # Entry point
│ ├── controllers/
│ │ └── app_controller.py # Business logic, signal handling
│ ├── models/
│ │ ├── task.py # Task class, priority constants
│ │ └── todo_list.py # TodoList class with serialization
│ └── views/
│ ├── main_windows.py # Main window (list overview)
│ ├── list_page.py # Detailed task view with sidebar
│ └── add_task_dialog.py # Dialog for new tasks
├── data/
|    └── .gitkeep
├── requirements.txt # Python dependencies
└── README.md
## File Formats

| File | Format | Description |
|------|--------|-------------|
| `*.py` | Python source code | Application logic |
| `todo_data.json` | JSON | Stores all lists and tasks in a structured format |
| `requirements.txt` | Plain text | Lists pip‑installable dependencies |

**JSON data structure example:**
```json
{
  "lists": [
    {
      "name": "Work",
      "tasks": [
        {
          "title": "Finish report",
          "description": "Quarterly summary",
          "created_at": "2025-03-15T10:30:00",
          "deadline": "2025-03-20T23:59:59",
          "priority": 2,
          "completed": false
        }
      ]
    }
  ]
}
Setup & Installation
Clone or download the repository

Install Python 3.8+ (if not already installed)

Install dependencies

bash
pip install -r requirements.txt
Run the application

bash
python src/main.py
Dependencies:
PyQt6 – GUI framework
Python standard library (json, pathlib, datetime)

Usage:
Main window: double‑click a list to open it; single‑click to select it for deletion.

List page:
Add tasks with title, description, priority, and deadline.
Use the sidebar to sort by priority or go back.
Check a task – it will disappear (marked done).

Persistent data: All changes are automatically saved to todo_data.json.

License:
MIT License – free to use, modify, and distribute.

-Author:
Maryam Ashraf


### 2. `requirements.txt`
PyQt6>=6.5.0
