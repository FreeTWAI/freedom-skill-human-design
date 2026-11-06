"""Validate a public synthetic collaboration plan; never perform external actions."""
import json
import sys
from pathlib import Path


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ["plan must be an object"]
    if not isinstance(data.get("title"), str) or not data["title"].strip():
        errors.append("title is required")
    if data.get("data_classification") != "synthetic":
        errors.append("public examples must be synthetic; private records stay outside this repo")
    expected_kind = 'human-design'
    if data.get("kind") != expected_kind:
        errors.append("kind must be " + expected_kind)
    check(data, errors)
    return errors


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def records(data, key, errors):
    value = data.get(key)
    if not isinstance(value, list) or not value:
        errors.append(key + " must contain at least one object")
        return []
    for item in value:
        if type(item) is not dict:
            errors.append(key + " must contain at least one object")
            return []
    return value


def unique_ids(items, label, errors):
    seen = set()
    invalid = False
    duplicate = False
    for item in items:
        val = item.get("id")
        if type(val) is not str or not val.strip():
            invalid = True
        elif val in seen:
            duplicate = True
        else:
            seen.add(val)
    if invalid:
        errors.append(label + " ids must be nonempty strings")
        return set()
    if duplicate:
        errors.append(label + " ids must be unique")
    return seen


def text(value):
    return isinstance(value, str) and bool(value.strip())


def check(data, errors):
    if data.get("birth_data_collected") is not False:
        errors.append("this public study template does not collect birth data")
    cs = data.get("consent_scope")
    if type(cs) is not str or not cs.strip():
        errors.append("consent scope is required")

    sources = records(data, "sources", errors)
    source_ids = unique_ids(sources, "source", errors)

    for source in sources:
        t = source.get("title")
        r = source.get("rights")
        if type(t) is not str or not t.strip() or type(r) is not str or not r.strip():
            errors.append("source title and rights are required")
        url = source.get("url", "")
        if type(url) is not str or not url.startswith("https://"):
            errors.append("source must link to an HTTPS reading reference")

    valid_claims = {"interpretation", "personal_observation", "source_claim", "open_question"}
    notes = records(data, "notes", errors)

    for note in notes:
        if note.get("source_id") not in source_ids:
            errors.append("note must reference a listed source")
        if note.get("claim_type") not in valid_claims:
            errors.append("classify notes without claiming a diagnostic or scientific finding")

        s = note.get("summary")
        if type(s) is not str or not s.strip():
            errors.append("note requires summary")

        q = note.get("question")
        if type(q) is not str or not q.strip():
            errors.append("note requires question")

        l = note.get("limitations")
        if type(l) is not str or not l.strip():
            errors.append("note requires limitations")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 scripts/validate.py <plan.json>")
    try:
        problems = validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as error:
        raise SystemExit(str(error))
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("PASS: structural checks only; no real-world activity or results verified")
