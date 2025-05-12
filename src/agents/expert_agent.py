import json
from typing import List, Dict, Any

class ExpertAgent:
    def __init__(
        self,
        role: str,
        dept: str,
        duty: str,
        llm_model,
        llm_tokenizer,
        participants: List[str],
        question: str,
        report: str
    ):
        self.role = role
        self.dept = dept
        self.duty = duty
        self.model = llm_model
        self.tokenizer = llm_tokenizer
        self.device = llm_model.device
        self.participants = participants
        self.question = question
        self.report = report
        self.history: List[Dict[str, str]] = [
            {"role": "system", "content":
                f"You are {self.role} ({self.dept}). Duty: {self.duty}."
            },
            {"role": "user", "content":
                f"Round: 1\nQuestion: {self.question}\nReport:\n{self.report}"
            }
        ]

    def respond(self, round_number: int, moderator_feedback: str) -> Dict[str, Any]:
        self.history.append({
            "role": "user",
            "content": f"Round: {round_number}\nFeedback: {moderator_feedback}"
        })
        prompt = self.tokenizer.apply_chat_template(
            self.history, tokenize=False, add_generation_prompt=True
        )
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        out = self.model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,
            temperature=0.0,
            pad_token_id=self.tokenizer.eos_token_id
        )
        raw = self.tokenizer.decode(out[0, inputs["input_ids"].shape[-1]:],
                                    skip_special_tokens=True).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = {"cot": "", "final_opinion": raw}
        self.history.append({"role": "assistant", "content": json.dumps(data)})
        return data
