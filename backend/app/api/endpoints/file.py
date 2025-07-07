from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from backend.rag.core.processor_factory import get_processor, PROCESSOR_MAP
from backend.rag.core.embedder import DocumentEmbedder

router = APIRouter()

UPLOAD_DIR = "files"  # relative to backend directory
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="파일명이 없습니다.")
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in PROCESSOR_MAP:
        raise HTTPException(status_code=400, detail=f"지원하지 않는 파일 형식입니다: {ext}")
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    print(f"[UPLOAD] 파일 업로드 완료: {file.filename}")
    # 임베딩 처리
    try:
        print(f"[EMBEDDING] {file.filename} 임베딩 시작")
        processor = get_processor(file_location)
        text = processor.load(file_location)
        embedder = DocumentEmbedder()
        collection, _ = embedder.initialize_collection()
        chunks = embedder.text_splitter.split_text(text)
        print(f"[EMBEDDING] {file.filename} 청크 수: {len(chunks)}")
        embedder.embed_documents(chunks, collection)
        print(f"[EMBEDDING] {file.filename} 임베딩 완료")
    except Exception as e:
        print(f"[ERROR] {file.filename} 임베딩 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"임베딩 실패: {str(e)}")
    return {"filename": file.filename, "embedding": "success"} 