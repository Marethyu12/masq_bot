import requests

from bs4 import BeautifulSoup
from summa import summarizer

def format(paragraphs):
    max_chars_per_line = 72
    formatted = ""
    
    for paragraph in paragraphs:
        words = paragraph.split()
        counter = 0
        words_str = " ".join(words)
        length = len(words_str)
        
        for idx, ch in enumerate(words_str):
            formatted += ch
            counter += 1
            
            if ch == " " and counter == 1:
                formatted = formatted[:-1]
                counter = 0
            
            if counter % (max_chars_per_line - 1) == 0:
                if ch.isalpha() and (idx + 1 < length and words_str[idx + 1] != " "):
                    formatted += "-"
                
                formatted += "\n"
                counter = 0
        
        formatted += "\n\n"
    
    return formatted

def get_content(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    
    content = soup.find(class_="main-content")
    
    headline = content.find("h1", {"itemprop" : "headline"}).get_text()
    author = content.find("span", {"itemprop" : "author"}).get_text()
    when = content.find(class_="p-published-time").get_text()
    
    text = content.find("div", {"itemprop" : "articleBody"})
    paragraphs = []
    
    for paragraph in text.find_all("p"):
        paragraphs.append(paragraph.get_text()[1:])
    
    formatted = format(paragraphs)
    
    content = ""
    
    content += "-" * 72 + "\n"
    content += "**HEADLINE:** " + headline + "\n**AUTHOR:** " + author + "\n**WHEN:** " + when + "\n\n"
    content += "**FULL ARTICLE:**\n"
    content += formatted + "\n"
    content += "**SUMMARY:**"
    content += summarizer.summarize(formatted.replace("\n", " ").replace("-", "")) + "\n"
    
    content += "-" * 72 + "\n\n"
    
    return content