import os, chromadb
from sentence_transformers import SentenceTransformer
from backend.rag.core.processor_factory import PROCESSOR_MAP
from backend.rag.config.settings import Config
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentEmbedder:
    def __init__(self):
        config = Config.get_instance()
        os.environ["ANONYMIZED_TELEMETRY"] = "False"
        self.embedder = SentenceTransformer(config.EMBEDDING_MODEL)
        self.client = chromadb.PersistentClient(path=config.CHROMA_DB_DIR)
        self.batch_size = config.BATCH_SIZE
        self.top_k = config.TOP_K
        self.chunk_size = config.CHUNK_SIZE
        self.chunk_overlap = config.CHUNK_OVERLAP
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

    def initialize_collection(self, collection_name="rag_collection"):
        """컬렉션 초기화 또는 가져오기"""
        try:
            collection = self.client.get_collection(collection_name)
            return collection, False  # 기존 컬렉션 존재
        except:
            collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            return collection, True  # 새 컬렉션 생성됨

    def embed_documents(self, chunks, collection, batch_size=100):
        """문서 청크를 임베딩하고 저장"""
        total_chunks = len(chunks)

        for i in range(0, total_chunks, batch_size):
            batch_chunks = chunks[i:i + batch_size]
            batch_embeddings = self.embedder.encode(batch_chunks, convert_to_tensor=False)

            collection.add(
                ids=[f"chunk_{j + 1}" for j in range(i, i + len(batch_chunks))],
                embeddings=[emb.tolist() for emb in batch_embeddings],
                metadatas=[{"text": chunk} for chunk in batch_chunks],
            )

            print(f"임베딩 진행률: {min((i + batch_size) * 100 / total_chunks, 100):.1f}%")

    def embed_all_documents(self, directory, collection_name="rag_collection"):
        collection, _ = self.initialize_collection(collection_name)
        all_chunks = []
        for ext, processor_cls in PROCESSOR_MAP.items():
            processor = processor_cls()
            if hasattr(processor, "load_files"):
                try:
                    files = processor.load_files(directory)
                    for fname, text in files.items():
                        # 텍스트를 청크로 분할
                        chunks = self.text_splitter.split_text(text)
                        all_chunks.extend(chunks)
                except Exception as e:
                    print(f"{ext} 처리 중 오류: {e}")
        self.embed_documents(all_chunks, collection, batch_size=self.batch_size)

    def query_documents(self, query, collection):
        """쿼리에 대한 관련 문서 검색"""
        query_embedding = self.embedder.encode(query, convert_to_tensor=False)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=self.top_k
        )

        if not results["metadatas"]:
            return ["관련 문서를 찾을 수 없습니다."]

        return [doc["text"] for doc in results["metadatas"][0]]

