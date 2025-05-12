from typing import Dict, Any
from agents.vision_expert import VisionExpert
from agents.difficulty_agent import DifficultyAgent
from agents.recruiter import Recruiter
from agents.expert_agent import ExpertAgent
from agents.challenger_agent import ChallengerAgent
from agents.moderator_agent import ModeratorAgent

class DiscussionEngine:
    def __init__(self, image, question, llm_model, llm_tokenizer, vlm_model, vlm_tokenizer):
        self.image = image
        self.question = question
        self.vision = VisionExpert(vlm_model, vlm_tokenizer)
        self.difficulty = DifficultyAgent(llm_model, llm_tokenizer)
        self.recruiter = Recruiter(llm_model, llm_tokenizer)
        self.challenger = ChallengerAgent(vlm_model, vlm_tokenizer)
        self.moderator = ModeratorAgent(llm_model, llm_tokenizer)

        # Pre‐discussion
        self.report = self.vision.analyze_image(image, question)
        self.diff   = self.difficulty.classify(question, self.report)
        self.team   = self.recruiter.recruit(self.diff, question, self.report)

        # Instantiate expert agents
        self.experts = {
            f"E{i+1}_{info['role'].replace(' ', '')}":
            ExpertAgent(
                role=info['role'], dept=info['dept'], duty=info['duty'],
                llm_model=llm_model, llm_tokenizer=llm_tokenizer,
                participants=[], question=question, report=self.report
            )
            for i, info in enumerate(self.team)
        }
        everyone = list(self.experts.keys()) + ["VisionExpert","Challenger","Moderator"]
        for agent in self.experts.values():
            agent.participants = everyone

        # Track settings
        if self.diff == "low":
            self.max_rounds, self.allow_escalate = 2, False
        elif self.diff == "moderate":
            self.max_rounds, self.allow_escalate = 2, True
        else:
            self.max_rounds, self.allow_escalate = 4, False

    def run(self) -> Any:
        feedback = ""
        for r in range(1, self.max_rounds+1):
            # Experts
            opinions = {aid: ag.respond(r, feedback) for aid, ag in self.experts.items()}
            # Challenger
            chal = self.challenger.respond(r, self.image, opinions, feedback)
            # Moderator summary
            summary = self.moderator.summarize_opinions(
                self.question, self.report, opinions, chal, r
            )
            analysis = self.moderator.analyze_summary(summary, self.question)
            if self.moderator.decide_convergence(analysis):
                return self.moderator.generate_final_answer(
                    self.question, summary, analysis["analysis"]
                )
            feedback = self.moderator.generate_feedback(summary, analysis["analysis"])
        return self.moderator.generate_final_answer(
            self.question, summary, analysis["analysis"]
        )
