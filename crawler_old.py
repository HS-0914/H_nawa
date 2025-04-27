"""
주어진 URL에서 부품 목록을 크롤링합니다.

Args:
    url (str): 크롤링할 페이지 URL
    selectors (dict): 부품의 item, title, price, link 선택자 정보
    limit (int): 가져올 최대 부품 수 (기본 10개)

Returns:
    list: 부품 정보 리스트 (name, price, link)
"""
import requests
from bs4 import BeautifulSoup

def crawl_pc_parts(url: str, selectors: dict, limit: int = 10):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    try:
        res = requests.get(url, headers=headers)

        '''
        if res.status_code != 200:
          raise Exception(f"요청 실패: {res.status_code}")
        '''
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"요청 에러 발생: {e}")
        return []  # 실패하면 빈 리스트 반환


    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select(selectors["item"])
    
    results = []

    for item in items[:limit]:
        try:
            name = item.select_one(selectors["title"]).text.strip()
            price_raw = item.select_one(selectors["price"]).text.strip()
            price = int(''.join(filter(str.isdigit, price_raw)))  # 숫자만 남기고 정수 변환
            link_tag = item.select_one(selectors["link"])
            link = link_tag["href"] if link_tag and "href" in link_tag.attrs else "N/A"

            results.append({
                "name": name,
                "price": price,
                "link": link
            })
        except Exception as e:
            print(f"크롤링 실패: {e}")
            continue

    return results
