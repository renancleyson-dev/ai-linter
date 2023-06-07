# AI Linter
Linter for rules written in semantic text.

## Development
### Setup

Feel free to setup with your own tools.

The standard way to setup is with `pip-tools` and `venv`:
```
  git clone github.com/renancleyson-dev/ai-linter/
  cd ai-linter/
  python -m venv .venv
  source .venv/bin/activate

  pip install pip-tools
  pip-sync
```
### Initialize the CLI with a project
```
  python -m ai_linter.cli init --path=/path/to/project
```
A .ai-linter.json file will be created, fill some rules there.
### Run the linter
```
  python -m ai_linter.cli run --path=/path/to/project
```
