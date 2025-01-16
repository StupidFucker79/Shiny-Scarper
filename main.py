import asyncio
import os
import random
import requests
from bs4 import BeautifulSoup
import logging
import subprocess
import json
from sub import * 

feed_filename = "./generated_pages/links.txt"





def upload(file_path):
  try:
     url = "https://bashupload.com"
     result = subprocess.run(['curl', '-T', file_path, url], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
     print(result.stdout.decode())
  except subprocess.CalledProcessError as e:
     print("Error:", e.stderr.decode())



async def fetch_all():
    existing_links = set()
    if os.path.exists(feed_filename):
        with open(feed_filename, 'r') as feed:
            existing_links = set(line.strip().split('|-|')[-1] for line in feed)  
    new_links = []
    mislinks = await extract_missav("https://missav.ws/dm561/en/uncensored-leak", end_page=2)
    for link in mislinks:
        if link[-1] not in existing_links:  # Check if link is new
            src_result = await crawl_missav(link[-1])  # Await the coroutine
            src = src_result[-1]  # Access the last element of the returned result
            link.append(src)
            new_links.append(link)
    vids = extract_hanime()
    for vid in vids:
        if vid[-1] not in existing_links:
            new_links.append(vid)
    vids = extract_htv()
    for vid in vids:
        if vid[-1] not in existing_links:
            new_links.append(vid)
    return new_links

async def main():
    new_links = await fetch_all()
    all_links = set()
    if os.path.exists(feed_filename):
        with open(feed_filename, 'r') as feed:
            all_links = set(feed.read().splitlines())
    for i,link in enumerate(new_links):
        all_links.add(str(i) + " ".join(link) + "\n")
    with open(feed_filename, 'w+') as feed:
        for link in all_links:
            feed.write(link + "\n")
  


if __name__ == "__main__":
    asyncio.run(main())
