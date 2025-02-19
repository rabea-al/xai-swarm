<p align="center">
  <a href="https://github.com/XpressAI/xircuits/tree/master/xai_components#xircuits-component-library-list">Component Libraries</a> •
  <a href="https://github.com/XpressAI/xircuits/tree/master/project-templates#xircuits-project-templates-list">Project Templates</a>
  <br>
  <a href="https://xircuits.io/">Docs</a> •
  <a href="https://xircuits.io/docs/Installation">Install</a> •
  <a href="https://xircuits.io/docs/category/tutorials">Tutorials</a> •
  <a href="https://xircuits.io/docs/category/developer-guide">Developer Guides</a> •
  <a href="https://github.com/XpressAI/xircuits/blob/master/CONTRIBUTING.md">Contribute</a> •
  <a href="https://www.xpress.ai/blog/">Blog</a> •
  <a href="https://discord.com/invite/vgEg2ZtxCw">Discord</a>
</p>

---

<p align="center"><i>Enhance Xircuits with Swarm-based autonomous agents! Build AI agents with tool access, memory, and task execution.</i></p>

---

## Xircuits Component Library for Swarm

This library integrates Swarm agents into Xircuits, enabling intelligent automation with tools, task execution, and workflow interactions.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Main Xircuits Components](#main-xircuits-components)
- [Try the Examples](#try-the-examples)




## Prerequisites

Before you begin, you will need the following:

1. Python 3.9+.
2. Xircuits.
3. OpenAI API Key and DeepL API Key set in a `.env` file.

## Main Xircuits Components

### SwarmAgentComponent:
Creates a Swarm agent with a name, instructions, and a set of available tools.

### SwarmRunComponent:
Runs a task using a Swarm agent and stores execution details, including tool calls and runtime.

### SwarmMakeToolbeltComponent:
Creates a toolbelt that stores agent tools for use during execution.



## Try The Examples

### Swarm Basic Agent Example

This example demonstrates how to set up a Swarm agent with a toolbelt and execute a task. The agent uses a translation tool to process text and stores the execution details.


