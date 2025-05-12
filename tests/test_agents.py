# tests/test_agents.py

import pytest
import torch
from PIL import Image

# Import your agents from the source package
from src.agents.vision_expert    import VisionExpert
from src.agents.difficulty_agent import DifficultyAgent

# —— Stub classes to simulate model behavior ———————————

class DummyResponse:
    """A simple container for a .text attribute."""
    def __init__(self, text):
        self.text = text

class DummyVLMModel:
    """Stub for a vision-language model with a .chat(...) method."""
    def chat(self, image, msgs, tokenizer, system_prompt, sampling, temperature, stream):
        # Always return a list of DummyResponse for testing
        return [DummyResponse("Dummy imaging report")]

class DummyVLMTokenizer:
    """Stub tokenizer for the vision model (unused in these tests)."""
    pass

class DummyLLMModel:
    """Stub for a causal LLM with a .generate(...) method."""
    def __init__(self):
        self.device = torch.device("cpu")

    def generate(self, input_ids, max_new_tokens, do_sample, temperature, pad_token_id):
        # Append one token (pad_token_id) to simulate generation
        return torch.cat([input_ids, torch.tensor([[pad_token_id]])], dim=1)

class DummyLLMTokenizer:
    """Stub tokenizer for the LLM, with chat-template support."""
    eos_token_id = 0

    def apply_chat_template(self, messages, tokenize, add_generation_prompt):
        # Simply concatenate message contents into a single prompt string
        return "\n".join(m["content"] for m in messages)

    def __call__(self, prompt, return_tensors):
        # Return a dummy tensor for input_ids
        return {"input_ids": torch.tensor([[1, 2, 3]])}

    def decode(self, gen_ids, skip_special_tokens):
        # Default decoding returns "moderate"
        return "moderate"

# —— Tests for VisionExpert —————————————————————————

def test_analyze_image_returns_string():
    """VisionExpert.analyze_image should return a string report."""
    model     = DummyVLMModel()
    tokenizer = DummyVLMTokenizer()
    expert    = VisionExpert(model, tokenizer)

    img    = Image.new("RGB", (10, 10))
    report = expert.analyze_image(img, "Find any abnormalities?")
    assert isinstance(report, str)
    assert "Dummy imaging report" in report

def test_query_roi_returns_expected_answer():
    """VisionExpert.query_roi should return the stubbed ROI answer."""
    class ROIModel(DummyVLMModel):
        def chat(self, *args, **kwargs):
            return [DummyResponse("ROI answer")]

    model     = ROIModel()
    tokenizer = DummyVLMTokenizer()
    expert    = VisionExpert(model, tokenizer)

    img = Image.new("RGB", (5, 5))
    result = expert.query_roi(img, "What is seen in the corner?")
    assert result == "ROI answer"

# —— Tests for DifficultyAgent ———————————————————————

def test_classify_returns_low_when_decode_low(monkeypatch):
    """If the tokenizer.decode returns 'low', classify() should map to 'low'."""
    model     = DummyLLMModel()
    tokenizer = DummyLLMTokenizer()
    agent     = DifficultyAgent(model, tokenizer)

    # Patch decode to return "low"
    monkeypatch.setattr(tokenizer, "decode", lambda ids, skip_special_tokens: "low")
    level = agent.classify("Sample question?", "Sample report")
    assert level == "low"

@pytest.mark.parametrize("stub_reply, expected_level", [
    ("low",      "low"),
    ("moderate", "moderate"),
    ("high",     "high"),
    ("unexpected", "moderate"),  # fallback to moderate
])
def test_classify_various_mappings(monkeypatch, stub_reply, expected_level):
    """Test mapping of various decode outputs to complexity levels."""
    model     = DummyLLMModel()
    tokenizer = DummyLLMTokenizer()
    agent     = DifficultyAgent(model, tokenizer)

    # Patch decode to return the parametrized stub_reply
    monkeypatch.setattr(tokenizer, "decode", lambda ids, skip_special_tokens: stub_reply)
    level = agent.classify("Any question?", "Any report")
    assert level == expected_level

