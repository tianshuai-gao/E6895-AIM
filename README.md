# E6895-AIM

**Adaptive Intelligent Medical Multi-Agents (AIM²)**  
Adaptive Intelligent Medical Multi-Agents: a dynamic multi-agent LLM framework simulating clinical MDT workflows for medical decision-making
![workflow](https://github.com/user-attachments/assets/e4ad5614-d074-4961-85b5-9d20067b53c1)

---

## 📖 Table of Contents

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

E6895-AIM/
- LICENSE  
- README.md  
- requirements.txt  
- .gitignore  

- src/  
  - __init__.py  
  - data/ (put sample images or test data here)  
  - agents/  
    - __init__.py  
    - vision_expert.py     # defines VisionExpert  
    - difficulty_agent.py  # defines DifficultyAgent  
    - recruiter.py         # defines Recruiter  
    - expert_agent.py      # defines ExpertAgent  
    - challenger_agent.py  # defines ChallengerAgent  
    - moderator_agent.py   # defines ModeratorAgent  
  - engine/  
    - __init__.py  
    - discussion_engine.py # defines DiscussionEngine  
  - app.py                 # Gradio interface: start_discussion, next_round_step  
  - utils.py               # shared helpers (HuggingFace login, model loading, etc.)

- tests/  
  - test_agents.py         # unit test examples  

