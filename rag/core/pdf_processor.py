import os, pymupdf4llm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from rag.config.settings import Config


class PDFProcessor:
    def __init__(self):
        config = Config.get_instance()
        self.pdf_dir = config.PDF_DIR
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )

    def load_pdfs(self):
        """디렉토리 내의 모든 PDF 파일을 로드하고 텍스트로 변환"""
        if not os.path.exists(self.pdf_dir):
            raise FileNotFoundError(f"디렉토리를 찾을 수 없습니다: {self.pdf_dir}")

        all_text = []
        for filename in os.listdir(self.pdf_dir):
            if filename.lower().endswith('.pdf'):
                full_path = os.path.join(self.pdf_dir, filename)
                print(f"PDF 파일 로드 중: {filename}")
                pdf_data = pymupdf4llm.to_markdown(full_path)
                all_text.append("".join(pdf_data))

        return "\n\n".join(all_text)

    def split_text(self, text):
        """텍스트를 청크로 분할"""
        return self.text_splitter.split_text(text)

