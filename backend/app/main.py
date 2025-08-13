from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from extractor import extract_order_info_from_file
from schemas import OrdersResponse
import uvicorn

app = FastAPI(title="JP Order Extractor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract", response_model=OrdersResponse)
async def extract(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="PDF 파일만 업로드 해주세요.")
    try:
        orders = extract_order_info_from_file(file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"처리 중 오류: {e}")

    return JSONResponse({"orders": orders})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
