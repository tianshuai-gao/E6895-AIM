# E6895-AIM

**Adaptive Intelligent Medical Multi-Agents (AIM²)**  
Foundation models have shown strong potential in clinical applications, yet their integration into real-world medical workflows remains limited by rigid prompting strategies and a lack of collaborative reasoning. We introduce \textbf{AIM\textsuperscript{2}} (\textit{Adaptive Intelligent Medical Multi-Agents}), a multi-agent framework designed to emulate dynamic clinical decision-making through structured, context-aware collaboration among large language models (LLMs). The superscript “2” reflects the system’s dual foundation in \textit{multi-modal understanding} and \textit{multi-agent coordination}. AIM\textsuperscript{2} first interprets the task complexity and clinical modality, then automatically assigns either solo or team-based agents with specialized roles and reasoning scopes. These agents engage in multi-round deliberation when appropriate, simulating multidisciplinary team (MDT) workflows common in hospitals. We evaluate AIM\textsuperscript{2} on a diverse set of multi-modal medical questions involving radiological images and free-text prompts. The results illustrate AIM\textsuperscript{2}’s capacity to adaptively balance efficiency and depth of reasoning while maintaining transparent, role-grounded interactions. This framework bridges the gap between powerful foundation models and practical, adaptive medical reasoning systems.
![workflow](https://github.com/user-attachments/assets/e4ad5614-d074-4961-85b5-9d20067b53c1)

---

## Table of Contents

1. [Features](#🌟-features)  
2. [Repository Structure](#📂-repository-structure)  
3. [Installation](#installation)  
4. [Usage](#usage)  
   1. [Command-Line Demo](#1-command-line-demo)  
   2. [Interactive Gradio Demo](#2-interactive-gradio-demo)  
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

## Examples
- Low complexity: Solo GP agent answers directly.

- Moderate complexity: 2–3 specialist agents discuss, may escalate to deep track.

- High complexity: Full MDT + Challenger, up to 4 rounds of debate.

## Testing
Run the unit tests with `pytest`:
```text
pytest -q
```
VisionExpert
- ```analyze_image``` returns a non-empty string.
- ```query_roi``` returns the stubbed answer.

DifficultyAgent
- ```classify``` correctly maps “low”, “moderate”, “high” and falls back to moderate.
- Add new tests under ```tests/``` for any additional agents or utilities you implement.

## Contributing
1. Fork the repository.
2. Create a feature branch:
```text
git checkout -b feature/your-feature-name
```
3. Commit your changes:
```text
git commit -m "Add [short description of feature]"
```
4. Push to your fork and open a Pull Request.

Please ensure that:
- Code follows PEP8 style conventions.
- Public APIs are documented with docstrings.
- New features include appropriate unit tests.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
Tianshuai Gao
- Email: tg2935@columbia.edu
- GitHub: tianshuai-gao/E6895-AIM

