# TOON vs JSON vs XML

For tabular/repeated-schema data, TOON cuts 30-60% of tokens vs JSON with comparable model accuracy.

## The data

100 product records:

### JSON (3,847 tokens)
```json
[
  {"id": 1, "name": "Widget A", "price": 9.99, "stock": 42},
  {"id": 2, "name": "Widget B", "price": 19.99, "stock": 17},
  {"id": 3, "name": "Widget C", "price": 4.99, "stock": 88}
]
```
Repeats `id`, `name`, `price`, `stock` 100 times.

### TOON (1,512 tokens — 60.7% reduction)
```
products[100]{id,name,price,stock}:
1,Widget A,9.99,42
2,Widget B,19.99,17
3,Widget C,4.99,88
```
Schema declared once, then comma-separated rows.

### XML (4,387 tokens — 14% heavier than JSON)
```xml
<products>
  <product>
    <id>1</id><name>Widget A</name><price>9.99</price><stock>42</stock>
  </product>
  ...
</products>
```

## Rules

- **TOON wins** for: tabular data, repeated schemas, log lines, CSV-like content, agent state, RAG chunks with uniform structure
- **JSON wins** for: nested/hierarchical single objects, API requests/responses, when downstream tooling expects JSON
- **XML wins** for: prompt structure (`<thinking>`, `<answer>`, `<example>`), document wrappers (`<documents>`), Claude was trained on these tags
- **Markdown wins** for: prose context, documentation, narratives

## Decision

| Shape | Format |
|---|---|
| Rows of identical-shape records | TOON |
| Hierarchical, one object | JSON |
| Prompt scaffolding | XML |
| Prose | Markdown |
| Code | Triple-backtick code block |

## Implementation

Convert JSON to TOON in 5 lines of Python — see [github.com/toon-format/toon](https://github.com/toon-format/toon).

```python
def to_toon(records: list[dict], name: str) -> str:
    if not records:
        return f"{name}[0]{{}}:"
    fields = list(records[0].keys())
    header = f"{name}[{len(records)}]{{{','.join(fields)}}}:"
    rows = [",".join(str(r.get(f, "")) for f in fields) for r in records]
    return "\n".join([header] + rows)
```

## Benchmarks

Average across Haiku/Flash/GPT-5 Nano/Grok on 100 row records:
- JSON: 4,587 tokens, 69.7% accuracy
- TOON: 1,820 tokens (-60%), 73.9% accuracy (+4 pts)

TOON is cheaper AND slightly more accurate. Net win.
