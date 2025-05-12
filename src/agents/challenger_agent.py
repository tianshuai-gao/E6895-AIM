import json
from typing import List, Dict, Any

class ChallengerAgent:
    def __init__(self, vlm_model, vlm_tokenizer):
        self.model = vlm_model
        self.tokenizer = vlm_tokenizer
        self.system_prompt = """
You are the Challenger Agent. Critically examine experts' opinions and the image to raise one structured doubt.
Output JSON with fields: agreement, cot, doubts, query_roi.
"""

        self.history: List[Dict[str, Any]] = [
            {"role": "system", "content": self.system_prompt}
        ]

    def respond(
        self,
        round_number: int,
        image: Any,
        expert_opinions: Dict[str, str],
        moderator_feedback: str
    ) -> Dict[str, Any]:
        opinions = "\n".join(f"{k}: {v}" for k, v in expert_opinions.items())
        user_msg = {
            "role": "user",
            "content": [image,
                f"Round: {round_number}\nOpinions:\n{opinions}"
                f"\nFeedback: {moderator_feedback}\nPlease output JSON."
            ]
        }
        res = self.model.chat(
            image=image,
            msgs=[user_msg],
            tokenizer=self.tokenizer,
            system_prompt=self.system_prompt,
            sampling=True,
            temperature=0.7,
            stream=False
        )
        raw = "".join(c.text for c in res) if isinstance(res, list) else res
        data = json.loads(raw.strip())
        return data
