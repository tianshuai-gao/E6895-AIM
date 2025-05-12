import json
from typing import List, Dict, Any

class ModeratorAgent:
    def __init__(self, llm_model, llm_tokenizer):
        self.model = llm_model
        self.tokenizer = llm_tokenizer
        self.system_prompt = (
            "You are Moderator Agent. Guide experts and challenger through rounds, summarize and decide convergence."
        )
        self.history: List[Dict[str, Any]] = [
            {"role": "system", "content": self.system_prompt}
        ]

    def _chat(self, user_prompt: str) -> str:
        msgs = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user",   "content": user_prompt}
        ]
        prompt = self.tokenizer.apply_chat_template(
            msgs, tokenize=False, add_generation_prompt=True
        )
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        out = self.model.generate(
            **inputs,
            max_new_tokens=512,
            do_sample=False,
            temperature=0.0,
            pad_token_id=self.tokenizer.eos_token_id
        )
        return self.tokenizer.decode(
            out[0, inputs["input_ids"].shape[-1]:],
            skip_special_tokens=True
        ).strip()

    def summarize_opinions(
        self,
        question: str,
        report: str,
        expert_opinions: Dict[str, Any],
        challenger_feedback: Dict[str, Any],
        round_number: int
    ) -> str:
        experts_text = "\n".join(
            f"- {k}: {v.get('final_opinion', '')}" if isinstance(v, dict) else f"- {k}: {v}"
            for k, v in expert_opinions.items()
        )
        user_prompt = (
            f"Round {round_number}\nQuestion: {question}\nReport:\n{report}\n"
            f"Experts:\n{experts_text}\nChallenger:\n{challenger_feedback}\n"
            "Write a concise medical summary."
        )
        summary = self._chat(user_prompt)
        return summary

    def analyze_summary(self, summary: str, question: str) -> Dict[str, Any]:
        user_prompt = (
            f"Summary:\n{summary}\n"
            f"Question: {question}\n"
            "Output JSON: {\"analysis\":[...],\"queries\":[...],\"converged\":true/false}"
        )
        raw = self._chat(user_prompt)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"analysis": [], "queries": [], "converged": False}

    def decide_convergence(self, analysis: Dict[str, Any]) -> bool:
        return analysis.get("converged", False)

    def generate_final_answer(self, question: str, summary: str, analysis: List[str]) -> str:
        user_prompt = (
            f"Finalize based on summary and analysis:\nQuestion: {question}\n"
            f"Summary:\n{summary}\nAnalysis:\n" + "\n".join(analysis)
        )
        return self._chat(user_prompt)

    def generate_feedback(self, summary: str, analysis: List[str]) -> str:
        user_prompt = (
            f"Summary:\n{summary}\nAnalysis:\n" + "\n".join(analysis) +
            "\nProvide feedback for next round."
        )
        return self._chat(user_prompt)
