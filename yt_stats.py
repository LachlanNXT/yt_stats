import requests
from bs4 import BeautifulSoup
import re
import json

def get_youtube_video_info(video_url):
    # Fetch the HTML content of the YouTube video page
    response = requests.get(video_url)
    if response.status_code != 200:
        raise Exception(f"Failed to load page: {response.status_code}")
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the title
    title = soup.find('meta', {'name': 'title'})['content']
    
    # Extract the tags
    tags = [meta['content'] for meta in soup.find_all('meta', {'property': 'og:video:tag'})]
     
    # Find the script tag containing ytInitialData
    script_tag = soup.find('script', string=re.compile(r'ytInitialData'))

    # Extract the JSON data using a regular expression
    if script_tag:
        script_content = script_tag.string
        json_data_match = re.search(r'ytInitialData\s*=\s*({.*?});', script_content, re.DOTALL)
        if json_data_match:
            json_data = json_data_match.group(1)
            yt_initial_data = json.loads(json_data)
            game_title = yt_initial_data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][1]["videoSecondaryInfoRenderer"]["metadataRowContainer"]["metadataRowContainerRenderer"]["rows"][0]["richMetadataRowRenderer"]["contents"][0]["richMetadataRenderer"]["title"]["simpleText"]
            game_year = yt_initial_data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][1]["videoSecondaryInfoRenderer"]["metadataRowContainer"]["metadataRowContainerRenderer"]["rows"][0]["richMetadataRowRenderer"]["contents"][0]["richMetadataRenderer"]["subtitle"]["simpleText"]
    
    return {
        'title': title,
        'tags': tags,
        'game_title': game_title,
        'game_year': game_year
    }

# Example usage
video_url = 'https://www.youtube.com/watch?v=tFp6D74ZVVY'
info = get_youtube_video_info(video_url)
print(f"Title: {info['title']}")
print(f"Tags: {', '.join(info['tags'])}")
print(f"Game Title: {info['game_title']}")
print(f"Game Year: {info['game_year']}")
