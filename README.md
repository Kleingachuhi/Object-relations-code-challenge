Here is your finalized `README.md`:

---

# 📰 Articles Management System

## Overview

A simple Python-based system for managing relationships between **Authors**, **Articles**, and **Magazines**, backed by a **SQLite** database.

## Features

* Create and manage authors, magazines, and articles
* Track which authors contributed to which magazines
* Explore relationships:

  * All articles by an author
  * All magazines an author has contributed to
  * All contributing authors for a magazine
* Full test coverage with `pytest`

## Technologies

* Python 3
* SQLite3
* Pytest

---

## 🛠️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/object-relations-code-challenge.git
cd object-relations-code-challenge
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### 3. Install dependencies

```bash
pip install pytest
```

---

## 🗃️ Database Setup

### Create database schema:

```bash
sqlite3 articles.db < lib/db/schema.sql
```

### Seed sample data:

```bash
PYTHONPATH=. python lib/db/seed.py
```

---

## 💡 Usage Examples

### Author Operations

```python
from lib.models.author import Author

author = Author(name="Jane Doe")
author.save()

jane = Author.find_by_name("Jane Doe")
articles = jane.articles()
magazines = jane.magazines()
```

### Magazine Operations

```python
from lib.models.magazine import Magazine

mag = Magazine(name="Tech Weekly", category="Technology")
mag.save()

tech = Magazine.find_by_name("Tech Weekly")
articles = tech.articles()
authors = tech.contributors()
```

### Article Operations

```python
from lib.models.article import Article

article = Article(title="Python Tips", author_id=1, magazine_id=1)
article.save()

found = Article.find_by_title("Python Tips")
```

---

## ✅ Running Tests

Run the test suite using:

```bash
pytest
```

---

## 📁 Project Structure

```
object-relations-code-challenge/
├── lib/
│   ├── models/
│   │   ├── author.py
│   │   ├── article.py
│   │   └── magazine.py
│   ├── db/
│   │   ├── connection.py
│   │   ├── schema.sql
│   │   └── seed.py
├── scripts/
│   └── setup_db.py
├── tests/
│   ├── test_author.py
│   ├── test_article.py
│   └── test_magazine.py
```

---

## 📄 License

This project is licensed under the **MIT License**.

---

