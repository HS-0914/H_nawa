import asyncio
from contextlib import asynccontextmanager
import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crawler import crawler_danawa

# 크롤링 대상
urls = [
    "https://shop.danawa.com/virtualestimate/?controller=estimateMain&methods=index&marketPlaceSeq=16",
    "https://www.compuzone.co.kr/online/online_main.htm?bannerid=GNBBannerOnlineMain",
]

categorys = ["CPU", "쿨러", "메인보드", "메모리", "그래픽카드", "SSD", "HDD", "케이스", "파워"]

selectors_list = [
    {
        "button": ".pd_list_area > .pd_list:nth-child(1) dd > a",
        "item": "#estimateMainProduct .scroll_box > .tbl_list tr",
        "title": ".title_price > .subject > a",
        "price": ".low_price > span",
        "link": ".title_price > .subject > a",
        "href": "https://shop.danawa.com/pc/?controller=estimateDeal&methods=productInformation&productSeq="
    },
    {
        "button": ".category_sub li",
        "item": "#sr_list_item_tb tr",
        "title": "td.name > .imgbox > b",
        "price": "td.Sblack11 > span",
        "link": "td.name > .imgbox",
        "href": "https://www.compuzone.co.kr/product/product_detail.htm?opt_chk=Y&ProductNo="
    }
]

DATA_DIR = "saved_data"
os.makedirs(DATA_DIR, exist_ok=True)


# 🛠 크롤링 작업 함수
async def crawl_all():
    while True:
        print("크롤링 시작...")
        for i in range(len(urls)):
            for category in categorys:
                parts = crawler_danawa(urls[i], category, selectors_list[i])
                file_path = os.path.join(DATA_DIR, f"{category}_{i}.json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(parts, f, ensure_ascii=False, indent=4)
                print(f"{category} 저장 완료")
        print("크롤링 종료. 10분 뒤 다시 크롤링")
        await asyncio.sleep(60 * 30)  # 30분마다 크롤링 반복


# 🛠 lifespan 핸들러 (서버 시작/종료 관리)
@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(crawl_all())  # 서버 시작하면 크롤링 시작
    yield
    # 서버 종료 시 특별한 작업이 필요하면 여기 추가

app = FastAPI(lifespan=lifespan)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 🛠 부품 가져오기 API
@app.get("/parts/{category}")
def get_parts(category: str):
    results = []

    # 저장된 모든 사이트의 해당 카테고리 파일을 모아서 반환
    for i in range(len(urls)):
        file_path = os.path.join(DATA_DIR, f"{category}_{i}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                parts = json.load(f)
                results.extend(parts)

    return {"category": category, "data": results}


# 🛠 기본 페이지
@app.get("/")
def read_root():
    return {"message": "PC 부품 크롤링 API입니다."}

# 	playwright install
