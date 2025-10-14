from bs4 import BeautifulSoup
import requests

# Fetch Hacker News front page
response = requests.get("https://news.ycombinator.com/news")
response.raise_for_status()  # to handle HTTP errors safely

web_page = response.text
soup = BeautifulSoup(web_page, "html.parser")

# Extract article titles and links
articles = soup.find_all(name="span", class_="titleline")
article_texts = [tag.getText() for tag in articles]
article_links = [tag.find("a").get("href") for tag in articles]

# Extract upvote counts
article_upvotes = [
  int(score.getText().split()[0]) 
  for score in soup.find_all(name="span", class_="score")
]

# Find article with highest upvotes
largest_number = max(article_upvotes)
largest_index = article_upvotes.index(largest_number)

print(article_texts[largest_index])
print(article_links[largest_index])
