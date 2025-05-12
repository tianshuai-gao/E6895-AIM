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
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── __init__.py
│   │
│   ├── data/
│   │   └── (如果有本地测试数据、示例图片等，放这里)
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── vision_expert.py      # 定义 VisionExpert
│   │   ├── difficulty_agent.py   # 定义 DifficultyAgent
│   │   ├── recruiter.py          # 定义 Recruiter
│   │   ├── expert_agent.py       # 定义 ExpertAgent
│   │   ├── challenger_agent.py   # 定义 ChallengerAgent
│   │   └── moderator_agent.py    # 定义 ModeratorAgent
│   │
│   ├── engine/
│   │   ├── __init__.py
│   │   └── discussion_engine.py  # 定义 DiscussionEngine
│   │
│   ├── app.py                    # Gradio 接口：start_discussion, next_round_step
│   └── utils.py                  # 任何共用 helper，比如登录 HuggingFace、加载模型等
│
└── tests/
    └── test_agents.py           # 单元测试例子

