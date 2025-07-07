from .pdf_processor import PdfProcessor
from .txt_processor import TxtProcessor
from .ppt_processor import PptProcessor
from .xls_processor import XlsProcessor
from .hwp_processor import HwpProcessor

PROCESSOR_MAP = {
    '.pdf': PdfProcessor,
    '.txt': TxtProcessor,
    '.ppt': PptProcessor,
    '.pptx': PptProcessor,
    '.xls': XlsProcessor,
    '.xlsx': XlsProcessor,
    '.hwp': HwpProcessor,
    '.hwpx': HwpProcessor,
}

def get_processor(file_path: str):
    ext = file_path.lower().split('.')[-1]
    ext = f'.{ext}'
    processor_cls = PROCESSOR_MAP.get(ext)
    if not processor_cls:
        raise ValueError(f"지원하지 않는 확장자: {ext}")
    return processor_cls() 