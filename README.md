or as a positional argument:
**Ao3 Tag Block Generator**

A small prototype CLI that parses comma-separated tag lists and prints a CSS rule you can paste into an AO3 site skin to hide matching blurb elements.

This README documents the current behavior of the tool (encoding rules and examples) so the produced CSS selectors match AO3 tag hrefs.

**Encoding / transformation behavior**
- The CLI percent-encodes each tag using UTF-8 (via `urllib.parse.quote`). This makes non-ASCII characters and reserved URL characters safe for use inside the CSS attribute selector (e.g. `é` → `%C3%A9`).
- After percent-encoding, a small set of substitutions are applied so the selectors match AO3's tag URLs more closely:
  - `%2F` (slash) → `*s*`
  - `%26` (ampersand) → `*a*`
  - `%2E` or literal `.` → `*d*`
  - `%3F` (question mark) → `*q*`
  - `%23` (hash) → `*h*`
  - `%28`/`%29` → `(` / `)` (parentheses restored)
  - `%3A` → `:` (colon restored)
  - `%40` → `@` (at-sign restored)

Note: these substitutions are intentionally limited — the percent-encoding step preserves all other characters, and the substitutions are applied so the produced selector string matches the specific formatting you want for AO3 tag hrefs.

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

**Examples (expected output)**
- Input: `python -m ao3tagblockgenerator --tags "café, tag/with/slash, a & b"`
- Output (example CSS rule):
```
.blurb:has(a[href$="/tags/caf%C3%A9/works"]),
.blurb:has(a[href$="/tags/tag*s*with*s*slash/works"]),
.blurb:has(a[href$="/tags/a%20*a*%20b/works"]) {
    display: none;
}
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
- Current behavior: the CLI prints a CSS rule (exact-match selectors) that you can paste into an AO3 skin.
- Next items to consider:
  - Add an option to write output to a file
  - Add option to allow partial-match mode for looser css matching

See `LICENSE` for licensing.
