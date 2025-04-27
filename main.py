from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정 (HTML 파일에서 API 접근 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 나중에 배포할 때는 origin 제한 필요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "PC 부품 크롤링 API입니다."}

# 부품 목록 가져오기용 엔드포인트 (나중에 연결할 예정)
@app.get("/parts/{category}")
def get_parts(category: str):
    return {"category": category, "data": []}


# 	playwright install