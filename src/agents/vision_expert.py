from PIL import Image
import json
from transformers import BitsAndBytesConfig
from torch import Tensor

class VisionExpert:
    def __init__(self, vlm_model, vlm_tokenizer):
        self.model = vlm_model
        self.tokenizer = vlm_tokenizer

    def analyze_image(self, image: Image.Image, question: str) -> str:
        system_prompt = (
            "You are a board-certified medical vision expert.\n"
            f"Examine the following image with question: {question}\n"
            "Produce a professional imaging report including global impression, key findings, notable regions, and suggestions."
        )
        user_msg = {
            "role": "user",
            "content": [image, "Please follow the system prompt exactly."]
        }
        res = self.model.chat(
            image=image,
            msgs=[user_msg],
            tokenizer=self.tokenizer,
            system_prompt=system_prompt,
            sampling=True,
            temperature=0.7,
            stream=False
        )
        report = "".join(chunk.text for chunk in res) if isinstance(res, list) else res
        return report.strip()

    def query_roi(self, image: Image.Image, question: str) -> str:
        system_prompt = (
            "You are a medical vision expert. Answer concisely based solely on the image."
        )
        user_msg = {"role": "user", "content": [image, f"Question: {question}"]}
        res = self.model.chat(
            image=image,
            msgs=[user_msg],
            tokenizer=self.tokenizer,
            system_prompt=system_prompt,
            sampling=True,
            temperature=0.7,
            stream=False
        )
        answer = "".join(c.text for c in res) if isinstance(res, list) else res
        return answer.strip()
