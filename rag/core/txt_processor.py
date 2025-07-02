from .document_processor import DocumentProcessor

class TxtProcessor(DocumentProcessor):
    """
    TXT 파일을 처리하는 프로세서. 텍스트 파일에서 텍스트를 추출한다.
    """
    extension = ('.txt',)
    def load(self, file_path: str) -> str:
        """
        TXT 파일을 읽어 텍스트로 반환한다.

        Args:
            file_path (str): TXT 파일 경로
        Returns:
            str: 추출된 텍스트
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read() 