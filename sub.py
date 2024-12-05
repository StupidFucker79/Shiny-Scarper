import requests,re
from bs4 import BeautifulSoup
from urllib.parse import urljoin



def extract_hanime():
    links = []
    data = []
    category = ["new-hanime","tsundere","harem","reverse","milf","romance","school","fantasy","ahegao","public","ntr","gb","incest","uncensored","ugly-bastard"]
    url = 'https://hanimes.org/category/'
    for cate in category:
         response = requests.get(url+cate)
         if response.status_code == 200:
              soup = BeautifulSoup(response.text, 'html.parser')
              ul_elements = soup.find_all('article', class_='TPost B')
              for ul in ul_elements:
                   title = ul.find_all('h2', class_='Title')[0].get_text().strip()
                   div_tags = ul.find_all('div', class_='TPMvCn')
                   for div in div_tags:
                        link = div.find_all('a',href=True)[0]['href']
                        imgs = ul.find_all('img',src=True)
                        img = [ img['src'] for img in imgs][0]
                        links.append([title,img,link])
              for title,img,link in links:
                  response = requests.get(link)
                  if response.status_code == 200:
                      soup = BeautifulSoup(response.content, 'html.parser')
                      result = [ a['src'] for a in soup.find_all('source', src=True)]
                      print([title,img,result[0]])
                      d = [title,result[0]]
                      if d not in data:
                         data.append(d)         
                  else:
                    logger.error(f"Failed to retrieve content. Status code: {response.status_code}")
              return data
         else:
                logger.error(f"Failed to retrieve content. Status code: {response.status_code}")
                return []

async def crawl_missav(link):
    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=link)
            title = [
                unquote(i["href"].split("&text=")[-1]).replace("+", " ")
                for i in result.links.get("external", [])
                if i["text"] == "Telegram"
            ]
            videos = [
                video["src"]
                for video in result.media.get("videos", [])
                if video.get("src")
            ]
            return title[0] if title else None, videos[0] if videos else None
    except Exception as e:
        print(f"Error while crawling link {link}: {e}", exc_info=True)
        return None, None



async def extract_missav(base_url, end_page):
    results = []
    async with AsyncWebCrawler() as crawler:
        for page_num in range(1, end_page + 1):
            url = f"{base_url}?page={page_num}"
            try:
                result = await crawler.arun(
                    url=url,
                    exclude_external_links=True,
                    exclude_social_media_links=True,
                )
                videos = [
                    [img["alt"], img["src"], f"https://missav.com/en/{img['src'].split('/')[-2]}"]
                    for img in result.media.get("images", [])
                    if img["src"] and "flag" not in img["src"]
                ]
                results.extend(videos)
            except Exception as e:
                logger.error(f"Error analyzing {url}: {e}")
    return results

