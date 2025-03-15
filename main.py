from bs4 import BeautifulSoup
import requests


def fetch_article():
    from app import app, db, Article

    print("yooo we fetching da article...")
    response = requests.get("https://news.ycombinator.com/news")

    if response.status_code != 200:
        print("Error: sorry i no reach get the fetch page, status code:", response.status_code)
        return {"title": "sorry but no article was found", "link": "#", "vote": 0}

    soup = BeautifulSoup(response.text, "html.parser")
    print("Page title:", soup.title)

    topics = soup.find_all(name="span", class_="titleline")
    if not topics:
        print("Error:Sorry no topics found")
        return None

    topics_titles = []
    topic_links = []
    for topic_tag in topics:
        title = topic_tag.getText()
        topics_titles.append(title)
        anchor_tag = topic_tag.find("a")
        if anchor_tag:
            link = anchor_tag.get("href")
            topic_links.append(link)

    topics_votes = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]
    if not topics_votes:
        print("bruh no votes found, so no article. soz")
        return None

    highest_score = max(topics_votes)
    highscore_position = topics_votes.index(highest_score)

    title = topics_titles[highscore_position]
    link = topic_links[highscore_position]
    vote = highest_score

    article = {
        "title": title,
        "link": link,
        "vote": highest_score
    }
    print("✅ FETCH DEBUG:", article)

    new_article = Article(title=title, link=link, votes=vote)

    with app.app_context():
        db.session.add(new_article)
        db.session.commit()
        print(f"✅ i just saved the article yaaa: {new_article.title}")

    return article

if __name__ == "__main__":
    print("wee running main.py... wait small")
    result = fetch_article()
    print("here you go fetch_article result:", result)
