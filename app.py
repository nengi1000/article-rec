from flask import Flask, render_template
from main import fetch_article
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///articles.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(500), nullable=False)
    votes = db.Column(db.Integer, nullable=False)
    # favorite = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Article {self.title}>"

@app.route('/')
def home():
    article = fetch_article()  # Call your function
    return render_template("index.html", title=article["title"], link=article["link"], vote=article["vote"])

@app.route("/old")
def saved_articles():
    articles = Article.query.all()

    seen_links = set()
    unique_articles = []

    for article in articles:
        if article.link not in seen_links:
            unique_articles.append(article)
            seen_links.add(article.link)

    return render_template("old.html", articles=unique_articles)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    results = Article.query.filter(Article.title.ilike(f"%{query}%")).all()
    return render_template("searched.html", results=results, query=query)



if __name__ == '__main__':
    app.run(debug=True)
