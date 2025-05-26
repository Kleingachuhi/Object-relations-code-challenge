import pytest
from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine
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
    cursor.execute("INSERT INTO magazines (name, category) VALUES ('Tech Today', 'Technology')")
    magazine_id = cursor.lastrowid

    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES ('AI in 2025', ?, ?)", (author_id, magazine_id))

    conn.commit()
    conn.close()
    return author_id, magazine_id

def test_author_articles(setup_db):
    author_id, _ = setup_db
    author = Author.find_by_id(author_id)
    articles = author.articles()
    assert len(articles) == 1
    assert articles[0].title == "AI in 2025"


def test_author_magazines(setup_db):
    author_id, _ = setup_db
    author = Author.find_by_id(author_id)
    magazines = author.magazines()
    assert len(magazines) == 1
    assert magazines[0].name == "Tech Today"


def test_add_article(setup_db):
    author_id, magazine_id = setup_db
    author = Author.find_by_id(author_id)
    magazine = Magazine.find_by_id(magazine_id)

    article = author.add_article(magazine, "Quantum Computing")
    assert article.title == "Quantum Computing"
    assert article.author_id == author.id

def test_topic_areas(setup_db):
    author_id, _ = setup_db
    author = Author.find_by_id(author_id)
    categories = author.topic_areas()
    assert categories == ["Technology"]
