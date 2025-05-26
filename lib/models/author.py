from lib.db.connection import get_connection
from lib.models.article import Article
from lib.models.magazine import Magazine


class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()

        if self.id is None:
            cursor.execute(
                "INSERT INTO authors (name) VALUES (?)",
                (self.name,)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE authors SET name = ? WHERE id = ?",
                (self.name, self.id)
            )

        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()

        return cls(row["name"], row["id"]) if row else None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()

        return cls(row["name"], row["id"]) if row else None

    def articles(self):
        from lib.models.article import Article
        return Article.find_by_author(self.id)

    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()

        from lib.models.magazine import Magazine
        return [Magazine(row["name"], row["category"], row["id"]) for row in rows]

    def topic_areas(self):
        """Returns unique list of categories of magazines the author has contributed to."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()

        return [row["category"] for row in rows]

    def add_article(self, magazine, title):
        """Creates and saves a new Article for this author and given magazine."""
        article = Article(title=title, author_id=self.id, magazine_id=magazine.id)
        article.save()
        return article

    def __repr__(self):
        return f"<Author {self.name} (id={self.id})>"