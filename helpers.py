import re

def collect_value(tokens, start_index, token_aliases, stop_words):
    value_tokens = []
    i = start_index

    while i < len(tokens):
        raw = tokens[i].lower()
        normalised = token_aliases.get(raw, raw)

        if normalised in stop_words:
            break

        value_tokens.append(tokens[i])
        i += 1

    return " ".join(value_tokens), i

def ci_equals(column):
    return f"LOWER({column}) = LOWER(?)"

def match_alias_group(text, aliases):
    for phrase, canonical in sorted(aliases.items(), key=lambda item: len(item[0]), reverse=True):
        pattern = r"\b" + re.escape(phrase) + r"\b"
        if re.search(pattern, text):
            new_text = re.sub(pattern, "", text, count=1)
            return canonical, new_text
    return None, text

def resolve_alias(value, alias_dict):
    return alias_dict.get(value.strip().lower(), value.strip())