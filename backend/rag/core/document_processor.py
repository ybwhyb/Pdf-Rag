from abc import ABC, abstractmethod
import os

class DocumentProcessor(ABC):
    """
    문서 프로세서의 추상 클래스.
    단일 파일 로드 및 디렉토리 내 일괄 로드 인터페이스를 제공한다.
    """
    extension = None  # str, tuple, list 모두 지원

    @abstractmethod
    def load(self, file_path: str) -> str:
        """
        문서를 읽어 텍스트로 반환한다.

        Args:
            file_path (str): 문서 파일 경로
        Returns:
            str: 추출된 텍스트
        """
        pass

    def load_files(self, directory: str) -> dict:
        """
        디렉토리 내 지원 확장자 파일을 모두 읽어 dict로 반환한다.

        Args:
            directory (str): 디렉토리 경로
        Returns:
            dict: 파일명과 추출 텍스트 매핑
        """
        result = {}
        if not self.extension:
            raise NotImplementedError("확장자(extension) 속성을 지정해야 합니다.")
        exts = self.extension if isinstance(self.extension, (tuple, list)) else [self.extension]
        for fname in os.listdir(directory):
            if any(fname.lower().endswith(ext) for ext in exts):
                path = os.path.join(directory, fname)
                result[fname] = self.load(path)
        return result 