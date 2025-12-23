**Ao3 Tag Block Generator**

A small prototype CLI to parse comma-separated tag lists and generate css code that can be pasted into an Ao3 site skin to use as a tag blocklist.

**Quick Start**
- **Create a virtual env & activate (PowerShell):**
```
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```
- **Install editable (recommended):**
```
python -m pip install -e .
```

**Run the CLI**
- Using the installed package:
```
python -m ao3tagblockgenerator --tags "tag1, tag2"
```
or as a positional argument:
```
python -m ao3tagblockgenerator "tag1, tag2, tag3"
```

- Without installing (one-off), set `PYTHONPATH` to include `src`:
```
$env:PYTHONPATH = '.\\src'; python -m ao3tagblockgenerator --tags "tag1, tag2"
```

**Run tests**
- Install test deps and run `pytest`:
```
pip install -r requirements.txt
pytest -q
```

**Project layout**
- `src/ao3tagblockgenerator/` — package source
- `tests/` — pytest tests
- `pyproject.toml` — build metadata / editable install support
- `requirements.txt` — test dependencies (pytest)

**Notes & Next Steps**
- Current behavior: the CLI prints out css code that you can paste into an Ao3 skin.
- Next work: 
  - Add option for partial match instead of default exact matching
- See `LICENSE` for licensing.
