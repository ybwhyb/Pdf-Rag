from setuptools import setup, find_packages

setup(
    name="PDF-Rag",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv>=1.0.0",
        "sentence-transformers",
        "chromadb",
        "pymupdf4llm",
        "langchain",
        "ollama",
    ],
    author="ybsong",
    author_email="ybwhyb@gmail.com",
    description="Document-based QA system using RAG",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
)