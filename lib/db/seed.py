from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

alice = Author(name="Alice Smith")
alice.save()

bob = Author(name="Bob Johnson")
bob.save()

tech = Magazine(name="Tech Today", category="Technology")
tech.save()

fashion = Magazine(name="Style Weekly", category="Fashion")
fashion.save()


article1 = Article(title="AI in 2025", author_id=alice.id, magazine_id=tech.id)
article1.save()

article2 = Article(title="Neural Networks Explained", author_id=alice.id, magazine_id=tech.id)
article2.save()

article3 = Article(title="Top 10 Fashion Trends", author_id=bob.id, magazine_id=fashion.id)
article3.save()

article4 = Article(title="Virtual Reality", author_id=bob.id, magazine_id=tech.id)
article4.save()

print("Seeded database with test data.")
