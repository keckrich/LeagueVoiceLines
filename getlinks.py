import requests
from bs4 import BeautifulSoup

def scrape_links(url, output_file):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', class_='category-page__member-link')
    
    with open(output_file, 'w', encoding='utf-8') as file:
        for link in links:
            href = link.get('href')
            if href:
                file.write(f"https://leagueoflegends.fandom.com{href}\n")
                print(f"Saved: https://leagueoflegends.fandom.com{href}")

if __name__ == "__main__":
    url = "https://leagueoflegends.fandom.com/wiki/Category:LoL_Champion_audio"
    output_file = "champion_audio_links.txt"
    scrape_links(url, output_file)
    print(f"Links saved to {output_file}")
