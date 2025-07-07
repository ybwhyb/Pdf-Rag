from .document_processor import DocumentProcessor

class HwpProcessor(DocumentProcessor):
    """
    HWP/HWPX 파일을 처리하는 프로세서. 한글 문서에서 텍스트를 추출한다.
    """
    extension = ('.hwp', '.hwpx')

    def load(self, file_path: str) -> str:
        """
        HWP/HWPX 파일을 읽어 텍스트로 반환한다.

        Args:
            file_path (str): HWP/HWPX 파일 경로
        Returns:
            str: 추출된 텍스트
        """
        if file_path.lower().endswith('.hwp'):
            try:
                import pyhwp
                doc = pyhwp.HWPDocument(file_path)
                return doc.body_text()
            except Exception as e:
                return f"[HWP 파싱 오류] {e}"
        elif file_path.lower().endswith('.hwpx'):
            return self._parse_hwpx(file_path)
        else:
            raise ValueError("지원하지 않는 확장자입니다.")

    def _parse_hwpx(self, file_path: str) -> str:
        """
        HWPX 파일을 zip+xml로 파싱하여 텍스트를 추출한다.
        """
        import zipfile
        import xml.etree.ElementTree as ET
        try:
            with zipfile.ZipFile(file_path, 'r') as z:
                # section0.xml에 본문 텍스트가 있음
                with z.open('Contents/section0.xml') as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    texts = []
                    ns = '{http://www.hancom.co.kr/hwpml/2010/section}'
                    for para in root.iter(f'{ns}p'):
                        texts.append(''.join([t.text or '' for t in para.iter(f'{ns}t')]))
                    return '\n'.join(texts)
        except Exception as e:
            return f"[HWPX 파싱 오류] {e}" 