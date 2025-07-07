from collections import deque
import ollama

class ChatManager:
    def __init__(self):
        from backend.rag.config.settings import Config
        config = Config.get_instance()
        self.model_name = config.LLM_MODEL
        self._system_msg = {"role": "system", "content": ""}
        self.queue = deque(maxlen=config.MAX_HISTORY)
        self.set_system_prompt()


    def set_system_prompt(self):
        """시스템 프롬프트 설정"""
        self._system_msg = {
            "role": "system",
            "content": (
                "가장 마지막 'user'의 'content'에 대해 답변한다. "
                "질문에 답할 때는 'system' 메시지 중 '문서 내용'에 명시된 부분을 우선 참고하여 정확히 답한다. "
                "개행은 문장이 끝날때와 서로 다른 주제나 항목을 구분할 때 사용하며, 불필요한 개행은 넣지 않는다."
            )
        }

    def generate_prompt(self, retrieved_docs):
        """프롬프트 생성"""
        docs = "\n".join(retrieved_docs)
        return [
            self._system_msg,
            {
                "role": "system",
                "content": f"문서 내용: {docs}\n질문에 대한 답변은 문서 내용을 기반으로 정확히 제공하시오."
            }
        ] + list(self.queue)

    def append_message(self, content, role="user"):
        """메시지 추가"""
        self.queue.append({"role": role, "content": content})

    def generate_answer(self, query, retrieved_docs):
        """답변 생성"""
        self.append_message(query)

        print("답변: ", end="", flush=True)
        full_answer = ""

        msg = self.generate_prompt(retrieved_docs)

        for response in ollama.chat(
                model=self.model_name,
                messages=msg,
                stream=True
        ):
            chunk = response["message"]["content"]
            print(chunk, end="", flush=True)
            full_answer += chunk

        self.append_message(full_answer, role="assistant")
        return full_answer
