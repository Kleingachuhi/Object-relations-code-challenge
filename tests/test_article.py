import pytest
from lib.db.connection import get_connection
from lib.models.article import Article

@pytest.fixture
def setup_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
    DELETE FROM articles;
    DELETE FROM authors;
    DELETE FROM magazines;
    """)
    cursor.execute("INSERT INTO authors (name) VALUES ('Alice')")
    author_id = cursor.lastrowid
    cursor.execute("INSERT INTO magazines (name, category) VALUES ('Science Weekly', 'Science')")
    magazine_id = cursor.lastrowid
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES ('Dark Matter', ?, ?)", (author_id, magazine_id))

    conn.commit()
    conn.close()
    return author_id, magazine_id

def test_find_article(setup_db):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM articles WHERE title='Dark Matter'")
    article_id = cursor.fetchone()["id"]
    article = Article.find_by_id(article_id)
    assert article.title == "Dark Matter"
