# AI Linter

Linter for rules written in plain English text. Document guidelines for a codebase, project, or company and lint with it.

**The project is under development.**

## What is this?

AI Linter is a project that uses Large Language Models(LLM) to lint code from semantic-based rules aka rules in plain English text for any programming language without the need for implementation. However, this project aims to achieve more than that.

### The problem

An AI coding assistant relies on its training data from different codebases, which may not be related to the developer's specific codebase opinions and guidelines. Additionally, there is currently no known AI review assistant (at least the author of this project doesn't know any) that seeks the developer's opinion directly. Instead, existing models attempt to predict the developer's opinion by training on external and unrelated code.

### The goal

AI Linter aims to be a next-generation, developer-centric tool. Next-generation tools should provide more human-friendly, easier, and faster ways to assist developers. AI Linter achieves this by offering a powerful method to define rules using natural language, without requiring any implementation.

## So what do you have for me?

The project is currently under development, with only the author working on it. New opinions and contributions are welcome. Feel free to contact [contact him](https://github.com/renancleyson-dev) for further discussions.

Currently, there's only a CLI application that can handle some naming convention rules in Python using GPT3.5, An OpenAI API key is required. It prints a fix suggestion and the violations along with the corresponding code locations. It uses something around $0.01 for 5 rules linting 1 source code file with 90 lines which is very expensive(imagine that on a codebase or running continuously with that file). 

#### Based on the progress made so far, the goals for the first release are as follows:

  - AI Linter should handle rules that are genuinely useful for developers, such as best practices.
  - Improve token usage and performance (maybe changing the model or limiting it to code review purposes only).
  - Support mainstream programming languages like JavaScript, C, C#, C++, Rust, Java, Ruby, etc.

#### Roadmap

Here's the plan for what is coming soon:
  - Improve code querying and target extraction. Something essential for AI Linter is to be able to extract the targets from the rules and search code related to it, but this is something that still needs some work.
  - Improve code evaluation from AI with more strict queries and better reasoning from prompts.
  - Support useful and common use cases. This is when we finally can see some evaluations about how precise, performant, and expensive AI Linter will be.
  - Change the configuration file format. Currently, the format is JSON but it's not ideal to write rules, mainly the extensive ones that may require examples.
  - Add some caching for the rules evaluation process since the rules don't change frequently and it would reduce the token usage and improve performance a lot.
  - Use [tree-sitter's incremental parsing](https://tree-sitter.github.io/tree-sitter) and create a process for incremental linting.
  - Add support for more programming languages.
  - Create extensions for IDEs and code editors.
  - Add usage for CI pipelines.

## Evaluation

TODO

## Development
### Setup

Feel free to setup with your own tools. The standard way is with `pip-tools` and `venv`:
```
  git clone github.com/renancleyson-dev/ai-linter/
  cd ai-linter/
  python -m venv .venv
  source .venv/bin/activate

  pip install pip-tools
  pip-sync
```
### Initialize the linter

The command below creates a `.ai-linter.json` file. Fill it with some rules, such as `{ "condition": "classes should be snake-case" }`.
```
  python -m ai_linter.cli init --path=/path/to/project
```

### Run the linter

Go to the project and run any of the commands below.
```
  python -m ai_linter.cli run --path=/path/to/a/project/file
  python -m ai_linter.cli run --path=/path/to/a/project/folder
  python -m ai_linter.cli run
```
