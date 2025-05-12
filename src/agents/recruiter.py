import re, json
from transformers import PreTrainedModel, PreTrainedTokenizer

class Recruiter:
    def __init__(self, llm_model: PreTrainedModel, tokenizer: PreTrainedTokenizer):
        self.model = llm_model
        self.tokenizer = tokenizer
        self.device = llm_model.device
        self.system_content = """
You are a medical team recruiter. Based on Case Question, Imaging Report, and Complexity (low/moderate/high),
assemble a JSON array of {"role","dept","duty"} following prescribed rules for each level.
Respond with JSON only.
Valid departments: [Cardiology, Pulmonology, …, Pathology, …].
"""

    def recruit(self, difficulty: str, question: str, report: str) -> list[dict]:
        user_content = f"Complexity: {difficulty}\nQuestion: {question}\nReport: {report}"
        messages = [
            {"role": "system", "content": self.system_content},
            {"role": "user",   "content": user_content}
        ]
        prompt = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        out = self.model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,
            temperature=0.0,
            pad_token_id=self.tokenizer.eos_token_id
        )
        raw = self.tokenizer.decode(out[0], skip_special_tokens=True)
        m = re.search(r'(\[.*\])', raw, re.S)
        try:
            return json.loads(m.group(1)) if m else []
        except json.JSONDecodeError:
            return []
