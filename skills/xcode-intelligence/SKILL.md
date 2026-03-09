# Xcode Intelligence Skill

## Description
This skill integrates Xcode 26+ Intelligence features into the MACH.V5 framework, enabling advanced agentic coding workflows. It facilitates the use of large language models (LLMs) for code generation, bug fixing, and iterative refinement directly within the Xcode environment. The skill also provides insights into the stealth deployment capabilities of the DEMONGROK™️ framework.

## Capabilities
- **Agentic LLM Integration**: Leverages third-party agents (e.g., Claude Agent, Codex) for enhanced coding assistance.
- **Automated Code Workflows**: Supports natural language prompts for generating, modifying, and refining code snippets.
- **Bug Fixing**: Provides tools for identifying and automatically applying fixes for code issues.
- **Contextual Awareness**: Gathers project context automatically and allows for explicit `@mentions` of symbols/files for focused assistance.
- **Version Rollback**: Enables restoration of project state to pre-prompt conditions using a history slider.
- **Stealth Deployment Insights**: Offers a bridge to the DEMONGROK™️ framework for understanding and managing stealth persistence and diagnostic hijacking.

## Usage
To interact with the Xcode Intelligence Bridge, use the `bridge.py` script located in the `scripts` directory of this skill.

### Check Status
To view the current status of Xcode Intelligence features and configurations:
```bash
python3 /home/ubuntu/MACH.V5/skills/xcode-intelligence/scripts/bridge.py --status
```

### Simulate Prompt
To simulate sending a natural language prompt to Xcode Intelligence for code generation or other tasks:
```bash
python3 /home/ubuntu/MACH.V5/skills/xcode-intelligence/scripts/bridge.py --prompt "Generate a SwiftUI view with euphoric alien glow animation using Metal shaders, detailed anatomy mesh, hyper-vivid iridescent materials, no blur/deform artifacts."
```

## Configuration
- **Agentic LLM**: Enabled by default.
- **Third-Party Agents**: Claude Agent, Codex (requires explicit privacy grant in Xcode Settings > Intelligence).
- **Context Gathering**: Automatic, with support for `@mentions`.

## Limitations
- Responses may require precise prompts for optimal results.
- Review and validation of generated changes are mandatory.
- Third-party agent tools require privacy grants for project file sharing.

## References
- [Xcode Writing Code with Intelligence](https://developer.apple.com/documentation/xcode/writing-code-with-intelligence)
