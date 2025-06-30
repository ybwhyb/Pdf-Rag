from rag import Config
from rag.core.pdf_processor import PDFProcessor
from rag.core.embedder import DocumentEmbedder
from rag.core.chat_manager import ChatManager
from rag.handler.singal_handler import SignalHandler
from rag.utils.logger import setup_logger

logger = setup_logger(__name__)

class RAGSystem:
    def __init__(self):
        self.config = Config.get_instance()
        self.pdf_processor = PDFProcessor()
        self.document_embedder = DocumentEmbedder()
        self.chat_manager = ChatManager()
        self.collection = None
        self.signal_handler = SignalHandler()

        # 클린업 핸들러 등록
        self.signal_handler.add_cleanup_handler(self._cleanup)

    def _cleanup(self):
        """Clean up resources before shutdown"""
        try:
            if hasattr(self, 'document_embedder') and hasattr(self.document_embedder, 'client'):
                self.document_embedder.client.close()
            logger.info("리소스 정리가 완료되었습니다.")
        except Exception as e:
            logger.error(f"리소스 정리 중 오류 발생: {str(e)}")


    def initialize(self):
        """시스템 초기화 및 필요시 임베딩 수행"""
        self.collection, is_new = self.document_embedder.initialize_collection()

        if is_new:
            logger.info("새로운 임베딩을 시작합니다...")
            raw_text = self.pdf_processor.load_pdfs()
            chunks = self.pdf_processor.split_text(raw_text)
            self.document_embedder.embed_documents(chunks, self.collection)
            logger.info("임베딩이 완료되었습니다!")
        else:
            logger.info("기존 임베딩을 사용합니다.")

    def chat_loop(self):
        """대화 루프 실행"""
        #print("RAG 챗봇을 시작합니다! 질문을 입력하세요 (종료: 'exit')")
        logger.info("RAG 챗봇을 시작합니다! 질문을 입력하세요 (종료: 'exit')")

        while True:
            query = input("\n> ")
            if query.lower() == "exit":
                #print("챗봇을 종료합니다!")
                logger.info("챗봇을 종료합니다!")
                break

            retrieved_docs = self.document_embedder.query_documents(
                query,
                self.collection
            )
            self.chat_manager.generate_answer(query, retrieved_docs)

    def run(self):
        """Run the chat loop"""
        try:
            self.initialize()
            logger.info("챗봇을 시작합니다. 종료하려면 'exit'를 입력하거나 Ctrl+C를 누르세요.")

            while self.signal_handler.is_running():
                try:
                    query = input("\n> ")
                    if query.lower() == "exit":
                        logger.info("사용자가 종료를 요청했습니다.")
                        break

                    retrieved_docs = self.document_embedder.query_documents(
                        query,
                        self.collection
                    )
                    self.chat_manager.generate_answer(query, retrieved_docs)
                except EOFError:
                    # Ctrl+D 처리
                    logger.info("\nEOF 신호를 받았습니다.")
                    break
                except KeyboardInterrupt:
                    # Ctrl+C는 signal_handler에서 처리되므로 여기서는 무시
                    continue

        except Exception as e:
            logger.error(f"실행 중 오류가 발생했습니다: {str(e)}")
            raise
        finally:
            self._cleanup()


