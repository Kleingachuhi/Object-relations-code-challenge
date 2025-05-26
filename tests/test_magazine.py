import pytest
from lib.db.connection import get_connection
from lib.models.magazine import Magazine
from lib.models.author import Author
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
    author1_id = cursor.lastrowid
    cursor.execute("INSERT INTO authors (name) VALUES ('Bob')")
    author2_id = cursor.lastrowid

    cursor.execute("INSERT INTO magazines (name, category) VALUES ('Tech Today', 'Technology')")
    magazine_id = cursor.lastrowid

    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES ('AI in 2025', ?, ?)", (author1_id, magazine_id))
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES ('Cybersecurity', ?, ?)", (author1_id, magazine_id))
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES ('Blockchain', ?, ?)", (author2_id, magazine_id))

    conn.commit()
    conn.close()
    return magazine_id

def test_contributors(setup_db):
    magazine = Magazine.find_by_id(setup_db)
    contributors = magazine.contributors()
    assert len(contributors) == 2

def test_article_titles(setup_db):
    magazine = Magazine.find_by_id(setup_db)
    titles = magazine.article_titles()
    assert "AI in 2025" in titles
    assert "Cybersecurity" in titles

def test_contributing_authors(setup_db):
    magazine = Magazine.find_by_id(setup_db)
    authors = magazine.contributing_authors()
    names = [a.name for a in authors]
    assert "Alice" in names
    assert "Bob" not in names
