import os, pymupdf4llm
from rag.config.settings import Config
from .document_processor import DocumentProcessor


class PdfProcessor(DocumentProcessor):
    """
    PDF 파일을 처리하는 프로세서. PDF 문서에서 텍스트를 추출한다.
    """
    extension = ('.pdf',)

    def __init__(self):
        """
        PdfProcessor를 config와 함께 초기화한다.
        """
        config = Config.get_instance()
        self.pdf_dir = config.PDF_DIR or 'files'

    def load(self, file_path: str) -> str:
        """
        PDF 파일을 읽어 텍스트로 반환한다.

        Args:
            file_path (str): PDF 파일 경로
        Returns:
            str: 추출된 텍스트
        """
        pdf_data = pymupdf4llm.to_markdown(file_path)
        return "".join(pdf_data)

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

