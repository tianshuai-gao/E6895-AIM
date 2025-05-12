import torch
from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import os

def load_models():
    bnb = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.float16,
    )
    device = "cuda" if torch.cuda.is_available() else "cpu"

    vlm_model = AutoModel.from_pretrained(
        "ContactDoctor/Bio-Medical-MultiModal-Llama-3-8B-V1",
        quantization_config=bnb,
        device_map="auto",
        trust_remote_code=True
    )
    vlm_tokenizer = AutoTokenizer.from_pretrained(
        "ContactDoctor/Bio-Medical-MultiModal-Llama-3-8B-V1",
        trust_remote_code=True
    )
    llm_model = AutoModelForCausalLM.from_pretrained(
        "ContactDoctor/Bio-Medical-Llama-3-8B",
        quantization_config=bnb,
        device_map={"": device},
        torch_dtype=torch.bfloat16,
        trust_remote_code=True
    )
    llm_tokenizer = AutoTokenizer.from_pretrained(
        "ContactDoctor/Bio-Medical-Llama-3-8B", trust_remote_code=True
    )
    return llm_model, llm_tokenizer, vlm_model, vlm_tokenizer
