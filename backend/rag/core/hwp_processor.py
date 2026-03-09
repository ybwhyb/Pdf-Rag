from .document_processor import DocumentProcessor


class HwpProcessor(DocumentProcessor):
    """
    HWP/HWPX 파일을 처리하는 프로세서.
    한글 문서(.hwp, .hwpx)에서 텍스트를 추출한다.
    """

    extension = ('.hwp', '.hwpx')

    def load(self, file_path: str) -> str:
        """
        HWP/HWPX 파일을 읽어 텍스트로 반환한다.

        Args:
            file_path (str): 파일 경로

        Returns:
            str: 추출된 텍스트
        """

        file_path = file_path.lower()

        if file_path.endswith('.hwp'):
            return self._parse_hwp(file_path)

        if file_path.endswith('.hwpx'):
            return self._parse_hwpx(file_path)

        raise ValueError("지원하지 않는 확장자입니다.")

    def _parse_hwp(self, file_path: str) -> str:
        """
        HWP 파일 파싱
        """
        try:
            import pyhwp

            doc = pyhwp.HWPDocument(file_path)
            return doc.body_text()

        except ImportError:
            return "[HWP 파싱 오류] pyhwp 라이브러리가 설치되지 않았습니다."

        except Exception as e:
            return f"[HWP 파싱 오류] {e}"

    def _parse_hwpx(self, file_path: str) -> str:
        """
        HWPX 파일을 zip + xml 구조로 파싱하여 텍스트 추출
        """

        import zipfile
        import xml.etree.ElementTree as ET

        texts = []

        try:
            with zipfile.ZipFile(file_path, 'r') as z:

                # section xml 파일 찾기
                section_files = [
                    name for name in z.namelist()
                    if name.startswith("Contents/section") and name.endswith(".xml")
                ]

                if not section_files:
                    return "[HWPX 파싱 오류] section XML을 찾을 수 없습니다."

                for section in sorted(section_files):

                    with z.open(section) as f:

                        tree = ET.parse(f)
                        root = tree.getroot()

                        # namespace 자동 추출
                        ns = ""
                        if root.tag.startswith("{"):
                            ns = root.tag.split("}")[0] + "}"

                        # 문단 단위 텍스트 추출
                        for para in root.iter(f"{ns}p"):

                            line = "".join(
                                (t.text or "")
                                for t in para.iter(f"{ns}t")
                            )

                            if line.strip():
                                texts.append(line)

        except zipfile.BadZipFile:
            msg = "[HWPX 파싱 오류] 잘못된 HWPX(zip) 파일입니다."
            print(msg)
            return msg

        except Exception as e:
            return f"[HWPX 파싱 오류] {e}"

        return "\n".join(texts)