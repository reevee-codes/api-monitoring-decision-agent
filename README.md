This app uses OpenAI **only for decision making** (not chat).
You need to provide your own API key via environment variables.

---

## OpenAI API key

### Windows

```powershell
setx OPENAI_API_KEY "sk-your-api-key"
```

Restart your terminal / IDE after setting the variable.

---

### macOS / Linux

```bash
export OPENAI_API_KEY="sk-your-api-key"
```

---

## Verify

```python
import os
print(os.getenv("OPENAI_API_KEY"))
```

If it prints the key → setup is correct.

---

## Notes

* API keys are **never** stored in code
* If the key is missing or invalid, the system **automatically falls back** to rule‑based decisions

---

## Run

```bash
python main.py
```

---

**Project focus:** AI‑driven decision system with deterministic fallback.