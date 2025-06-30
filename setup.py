from setuptools import setup, find_packages

setup(
    name="docling",
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
    author="Your Name",
    author_email="your.email@example.com",
    description="Document-based QA system using RAG",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
)