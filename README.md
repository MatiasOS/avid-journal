# AViD Journal

**Automated Verification in Demonstrations** - The first fully automated mathematics journal.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## 🎯 Vision

AViD Journal accepts `.tex` files, formalizes proofs in Lean 4, verifies correctness, checks novelty against Mathlib and ArXiv corpus, and auto-publishes if valid.

This is critical infrastructure for AI-driven mathematical research — when AIs discover theorems autonomously, they'll need automated verification and review.

---

## 🏗️ Architecture

```
.tex Paper
    │
    ▼
┌─────────────────────────┐
│ PARSER                  │  → Extract mathematical blocks
│ src/parser/             │     (theorems, lemmas, definitions)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ FORMALIZATION           │  → Translate to Lean 4
│ src/formalization/      │     (Numina-Lean-Agent)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ VERIFICATION            │  → Prove correctness
│ Lean 4 Compiler         │     (formal verification)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ NOVELTY CHECK           │  → Check if new
│ src/novelty/            │     • Mathlib (via Numina/LeanDex)
│                         │     • ArXiv corpus
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ DECISION                │  → Accept / Reject
│ src/journal/            │     + Citation report
└─────────────────────────┘
```

---

## 📁 Project Structure

```
avid-journal/
│
├── examples/               # LaTeX de ejemplo públicos (+ README índice)
│   ├── tiny_even_numbers/paper.tex
│   └── thesis_ayrton_porto/paper.tex
│
├── src/
│   ├── parser/              # LaTeX parsing
│   │   ├── latex_parser.py
│   │   └── parse_tex.py
│   │
│   ├── novelty/             # Novelty detection
│   │   ├── arxiv_search.py      # ArXiv paper search
│   │   ├── paper_extractor.py   # PDF download & extraction
│   │   ├── theorem_extractor.py # Extract theorems from text
│   │   └── comparator.py        # Theorem comparison (LLM judge)
│   │
│   ├── formalization/       # Lean 4 formalization
│   │   ├── numina_interface.py  # Numina-Lean-Agent wrapper
│   │   ├── lean_project.py      # Lean project manager
│   │   └── orchestrator.py      # Main orchestration
│   │
│   ├── database/            # Data persistence
│   │   └── db.py
│   │
│   └── web/                 # Web interface (future)
│       └── (pending)
│
├── tests/                   # Testing
│   ├── test_parser.py
│   ├── test_novelty.py
│   └── golden_datasets/
│       └── boolean_algebra.json
│
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md
│   ├── PROGRESS.md
│   └── API.md
│
├── examples/                # Example papers
│   └── boolean_algebra_sample.tex
│
├── .gitignore
├── requirements.txt
├── setup.py                 # Package setup
└── README.md               # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Lean 4 (for formalization)
- Claude API key (for LLM judge)

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/avid-journal.git
cd avid-journal

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt
```

### Usage

**1. Parse a LaTeX paper:**
```bash
python src/parser/parse_tex.py paper.tex --stats
```

**2. Check novelty (ArXiv search):**
```bash
python src/novelty/arxiv_search.py "Boolean algebra isomorphism" --top-k 10
```

**3. Full pipeline (future):**
```bash
python src/journal/process_paper.py paper.tex -o report.json
```

---

## 📊 Current Status

**Last Updated:** February 20, 2025

### ✅ Completed

- [x] LaTeX parser with dependency graph extraction
- [x] Database schema with topological sorting
- [x] Numina-Lean-Agent integration structure
- [x] Lean project manager (Paper.lean generation)

### ⏳ In Progress

- [ ] **ArXiv paper search** (Semantic Scholar API) ← **CURRENT FOCUS**
- [ ] PDF extraction and theorem extraction
- [ ] Theorem comparison (LLM-as-judge)

### 🔜 Planned

- [ ] Web interface for paper submission
- [ ] Quality assessment module
- [ ] Full end-to-end pipeline
- [ ] Deployment infrastructure

See [PROGRESS.md](docs/PROGRESS.md) for detailed roadmap.

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Test parser
python tests/test_parser.py

# Test novelty check with golden dataset
python tests/test_novelty.py --dataset tests/golden_datasets/boolean_algebra.json
```

---

## 📖 Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design and components
- [Progress](docs/PROGRESS.md) - Development roadmap and status
- [API](docs/API.md) - Module interfaces and usage

### Lean formalization pipeline (Claude Code + Mathlib)

**Git/GitHub first-time setup (Spanish, submodule Mathlib vs Numina):** **[docs/GIT_Y_GITHUB_DESDE_CERO.md](docs/GIT_Y_GITHUB_DESDE_CERO.md)**

**Git/GitHub desde cero** (commits, push, Mathlib sin subir, Numina como submódulo): **[docs/GIT_Y_GITHUB_DESDE_CERO.md](docs/GIT_Y_GITHUB_DESDE_CERO.md)**

**PowerShell: errores `lean_project`, identidad y submódulo Numina:** **[docs/PASOS_PUSH_WINDOWS.md](docs/PASOS_PUSH_WINDOWS.md)**

Step-by-step setup (Spanish): **[docs/GUIA_INSTALACION_Y_USO.md](docs/GUIA_INSTALACION_Y_USO.md)** — installing Lean/elan, Lake/Mathlib, Python, Claude CLI, running the orchestrator, repo layout, editing prompts, and publishing to GitHub.

**Worked examples (LaTeX sources + checked-in Lean):** see **[examples/README.md](examples/README.md)** — tiny even-numbers paper and thesis excerpt project.

---

## 🤝 Contributing

This project is currently in early development. Contributions welcome once we reach v0.1.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Numina-Lean-Agent** - Autoformalization framework
- **LeanDex** - Semantic search over Mathlib
- **Lean Community** - For Mathlib and the Lean ecosystem
- **MerLean** - Inspiration for autoformalization pipeline

---

## 📧 Contact

Ayrton Porto  
Website: https://ayrtonporto.github.io/  
Project: AViD Journal

---

**Note:** This is research software in active development. Not production-ready.
