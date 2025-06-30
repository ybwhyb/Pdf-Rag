import os
from dotenv import load_dotenv
from pathlib import Path

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """환경 변수 로드 및 설정"""
        project_root = Path(__file__).parent.parent.parent
        env_path = project_root / '.env'
        load_dotenv(dotenv_path=env_path)

        # 파일 경로 설정
        self.PDF_DIR = os.getenv('PDF_DIR')
        self.CHROMA_DB_DIR = os.getenv('CHROMA_DB_DIR', '../../chroma_db')

        # 모델 설정
        self.EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'intfloat/multilingual-e5-small')
        self.LLM_MODEL = os.getenv('LLM_MODEL', 'exaone3.5:latest')

        # 청크 설정
        self.CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1500))
        self.CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 150))

        # 검색 설정
        self.TOP_K = int(os.getenv('TOP_K', 2))
        self.BATCH_SIZE = int(os.getenv('BATCH_SIZE', 100))

        # 대화 설정
        self.MAX_HISTORY = int(os.getenv('MAX_HISTORY', 10))

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Config()
        return cls._instance


