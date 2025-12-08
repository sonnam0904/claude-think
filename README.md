# Claude Think Tool - Dify Plugin

Multi-step thinking tool for Dify Node Agents based on Claude's think tool research.

## 📋 Overview

This plugin provides a "think" tool that enables Dify Node Agents to perform structured multi-step reasoning, creating richer context for better decision-making. Based on research from Claude showing 54% improvement in complex scenarios (τ-Bench).

## ✨ Features

- **Multi-Step Thinking**: Allows Node Agents to perform structured reasoning across multiple steps
- **Context Accumulation**: Automatically accumulates thoughts across tool calls in a session
- **Domain-Specific Prompts**: Pre-built templates for different domains (airline, retail, coding)
- **Zero Configuration**: No credentials required, works out of the box

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- Dify Plugin CLI (dify-plugin-daemon)

### Installation

1. **Install Dify Plugin CLI**:

```bash
# macOS (Brew - Recommended)
brew tap langgenius/dify
brew install dify

# Linux
# Download from https://github.com/langgenius/dify-plugin-daemon/releases
chmod +x dify-plugin-linux-amd64
sudo mv dify-plugin-linux-amd64 /usr/local/bin/dify
```

2. **Clone and Setup**:

```bash
cd claude-think-plugin
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure Environment**:

```bash
cp .env.example .env
# Edit .env with your Dify remote debug credentials
```

4. **Run Plugin**:

```bash
python -m main
```

## 📚 Documentation

- [PROJECT-PLAN.md](./PROJECT-PLAN.md) - Project planning and roadmap
- [INSTRUCTIONS.md](./INSTRUCTIONS.md) - Technical documentation and architecture
- [claude-think-tool.md](./claude-think-tool.md) - Original Claude research paper

## 🏗️ Project Structure

```
claude-think-plugin/
├── provider/          # Tool Provider implementation
├── tools/             # Tool implementations
├── src/               # Core source code
├── _assets/           # Static assets
├── tests/             # Test suite
├── main.py            # Plugin entry point
└── plugin.yaml        # Plugin metadata
```

## 🧪 Testing

```bash
pytest
```

## 📖 Usage

Once installed, the think tool will be available to Node Agents in Dify. Agents can call it like any other tool:

```
think(thought="Analyze the user request and list required information")
```

The tool automatically accumulates thoughts in the session context, allowing agents to reference previous reasoning steps.

## 🔧 Development

See [INSTRUCTIONS.md](./INSTRUCTIONS.md) for detailed development guide.

## 📄 License

MIT

## 🙏 Acknowledgments

- Based on Claude's think tool research (Anthropic)
- Built for Dify platform

---

**Version**: 0.1.0  
**Status**: Development (Phase 1)

