# E6895-AIM

**Adaptive Intelligent Medical Multi-Agents (AIM²)**  
Adaptive Intelligent Medical Multi-Agents: a dynamic multi-agent LLM framework simulating clinical MDT workflows for medical decision-making
![workflow](https://github.com/user-attachments/assets/e4ad5614-d074-4961-85b5-9d20067b53c1)

---

## Table of Contents

1. [Features](#features)  
2. [Repository Structure](#repository-structure)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Configuration](#configuration)  
6. [Examples](#examples)  
7. [Testing](#testing)  
8. [Contributing](#contributing)  
9. [License](#license)  
10. [Contact](#contact)  

---

## 🌟 Features

- **Vision Expert**  
  Extracts structured imaging findings and generates a professional report.  
- **Difficulty Triage**  
  Classifies case complexity into `low` / `moderate` / `high`.  
- **Adaptive Recruitment**  
  Builds a GP, Expert Team, or full MDT + Challenger based on complexity.  
- **Multi-Round Deliberation**  
  Experts and a Challenger agent debate under a Moderator’s guidance.  
- **Transparent Audit Trail**  
  Outputs include final answer, chain-of-thoughts, and timestamped logs.  

---

## 📂 Repository Structure

```text
E6895-AIM/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── utils.py                 # helpers (HF login, model loading)
│   ├── app.py                   # Gradio interface
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── vision_expert.py     # Define VisionExpert
│   │   ├── difficulty_agent.py  # Define DifficultyAgent
│   │   ├── recruiter.py         # Define Recruiter
│   │   ├── expert_agent.py      # Define ExpertAgent
│   │   ├── challenger_agent.py  # Define ChallengerAgent
│   │   └── moderator_agent.py   # Define ModeratorAgent
│   │
│   └── engine/
│       ├── __init__.py
│       └── discussion_engine.py # Define DiscussionEngine
│
└── tests/
    └── test_agents.py           # pytest unit tests
```

## Installation

1. Clone the repository
```text
git clone https://github.com/tianshuai-gao/E6895-AIM.git
cd E6895-AIM
```

2. Create a virtual environment
```text
python3 -m venv .venv
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate       # Windows
```

3.Install dependencies
```text
pip install -r requirements.txt
```

4. Login to Hugging Face
```text
huggingface-cli login
```

## Usage
1. Command-Line Demo
```text
python src/app.py \
  --image-path ./data/sample_mri.jpg \
  --question "Is there evidence of hemorrhage?"
```

This will print:
- Imaging report
- Complexity label
- Recruited team
- Multi-round discussion logs
- Final answer

2. Interactive Gradio Demo
```text
python -m src.app
```
Then open your browser at http://localhost:7860 to:
- Upload an image
- Enter a clinical question
- Step through each discussion round interactively

## Configuration
All key settings live in `src/utils.py` or can be overridden via environment variables:
```text
# src/utils.py (example)
MODEL_LLMT = "ContactDoctor/Bio-Medical-Llama-3-8B"
MODEL_VLM = "ContactDoctor/Bio-Medical-MultiModal-Llama-3-8B-V1"
QUANTIZATION:
  load_in_4bit: true
  compute_dtype: float16

# You can also set:
export AIM_LLMT_MODEL="gpt-4o-mini"
export AIM_VLM_MODEL="openai/gpt-4o-vision-preview"
```

Adjust `max_rounds` per complexity:
| Complexity | Max Rounds | Allow Escalation? |
|------------|------------|-------------------|
| low        | 2          | No                |
| moderate   | 2 (→4)     | Yes               |
| high       | 4          | No                |

Examples
- Low complexity
Solo GP agent answers directly.

- Moderate complexity
2–3 specialist agents discuss, may escalate to deep track.

- High complexity
Full MDT + Challenger, up to 4 rounds of debate.
