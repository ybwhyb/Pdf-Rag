import sys

from backend.rag.core.rag_system import RAGSystem
from backend.rag.utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    try:
        rag = RAGSystem()
        rag.run()
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)
#
# if __name__ == "__main__":
#     main()
