import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class DifficultyAgent:
    def __init__(self, llm_model, llm_tokenizer):
        self.model = llm_model
        self.tokenizer = llm_tokenizer
        self.device = self.model.device
        self.system_content = (
            "You are a clinical triage expert. Assign one word: low, moderate, or high.\n"
            "Output exactly one word, no extra text."
        )

    def classify(self, question: str, report: str) -> str:
        messages = [
            {"role": "system",  "content": self.system_content},
            {"role": "user",    "content": f"Question: {question}\nReport:\n{report}\nAnswer:"}
        ]
        prompt = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        out = self.model.generate(
            **inputs,
            max_new_tokens=5,
            do_sample=False,
            temperature=0.0,
            pad_token_id=self.tokenizer.eos_token_id
        )
        result = self.tokenizer.decode(out[0, inputs["input_ids"].shape[-1]:],
                                       skip_special_tokens=True).strip().lower()
        for lvl in ("low", "moderate", "high"):
            if result.startswith(lvl):
                return lvl
        return "moderate"

