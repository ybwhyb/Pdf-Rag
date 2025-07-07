from .document_processor import DocumentProcessor
import pandas as pd

class XlsProcessor(DocumentProcessor):
    """
    XLS/XLSX 파일을 처리하는 프로세서. 엑셀 문서에서 텍스트를 추출한다.
    """
    extension = ('.xls', '.xlsx')
    def load(self, file_path: str) -> str:
        """
        XLS/XLSX 파일을 읽어 텍스트로 반환한다.

        Args:
            file_path (str): XLS/XLSX 파일 경로
        Returns:
            str: 추출된 텍스트
        """
        dfs = pd.read_excel(file_path, sheet_name=None)
        text = []
        for sheet, df in dfs.items():
            text.append(f"[Sheet: {sheet}]")
            text.append(df.to_string(index=False))
        return "\n".join(text) 