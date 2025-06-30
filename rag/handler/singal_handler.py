import signal, sys
from typing import Callable
from rag.utils.logger import  setup_logger

logger = setup_logger(__name__)

class SignalHandler:
    def __init__(self):
        self._running = True
        self._cleanup_handlers = []
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """시그널"""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        # SIGKILL cannot be caught, so we don't handle it

    def _signal_handler(self, signum, frame):
        """종료 시그널"""
        signal_name = signal.Signals(signum).name
        logger.info(f"\n프로그램 종료 신호를 받았습니다 ({signal_name})...")
        self._running = False
        self._execute_cleanup()

    def is_running(self) -> bool:
        """상태체크"""
        return self._running

    def add_cleanup_handler(self, handler: Callable):
        """강제 종료 핸들러 추가"""
        self._cleanup_handlers.append(handler)

    def _execute_cleanup(self):
        """모든 핸들러 clean"""
        for handler in self._cleanup_handlers:
            try:
                handler()
            except Exception as e:
                logger.error(f"Cleanup handler failed: {str(e)}")

        logger.info("프로그램을 종료합니다...")
        sys.exit(0)

