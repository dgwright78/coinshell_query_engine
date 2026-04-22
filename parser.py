from config import (
    COMMANDS,
    TYPE_WORDS,
    STOP_WORDS,
    TOKEN_ALIASES,
    ALLOWED_SORT_COLUMNS,
)

from helpers import collect_value, ci_equals, match_alias_group, resolve_alias

def parse_natural_query(user_input, aliases):
    limit_value = None
    text = user_input.lower().strip()

    if text == "quit":
        return "QUIT", [], False, False, None

    if text == "help":
        return "HELP", [], False, False, None
    
    where_clauses = []
    params = []
    is_count = False
    is_random = False
    sort_column = None

    words = text.split()

    if "count" in words:
        is_count = True
        words = [w for w in words if w != "count"]
        text = " ".join(words)

    if "random" in words:
        is_random = True
        words = [w for w in words if w != "random"]
        text = " ".join(words)

    if "limit " in text:
        try:
            limit_value = int(text.split("limit ")[1].split()[0])
        except (IndexError, ValueError):
            pass

    if "before " in text:
        try:
            year = int(text.split("before ")[1].split()[0])
            where_clauses.append("year < ?")
            params.append(year)
        except (IndexError, ValueError):
            pass

    if "after " in text:
        try:
            year = int(text.split("after ")[1].split()[0])
            where_clauses.append("year > ?")
            params.append(year)
        except (IndexError, ValueError):
            pass

    if "sort " in text:
        try:
            candidate = text.split("sort ")[1].split()[0]
            candidate = TOKEN_ALIASES.get(candidate, candidate)
            if candidate in ALLOWED_SORT_COLUMNS:
                sort_column = candidate
        except IndexError:
            pass

    canonical, text = match_alias_group(text, aliases["monarchs"])
    if canonical:
        where_clauses.append("LOWER(monarch) = LOWER(?)")
        params.append(canonical)

    canonical, text = match_alias_group(text, aliases["denominations"])
    if canonical:
        where_clauses.append("LOWER(denomination) = LOWER(?)")
        params.append(canonical)

    canonical, text = match_alias_group(text, aliases["grades"])
    if canonical:
        where_clauses.append("LOWER(grade) = LOWER(?)")
        params.append(canonical)

    if "silver" in words:
        where_clauses.append("fineness > 0")

    canonical, text = match_alias_group(text, aliases["metals"])
    if canonical:
        where_clauses.append("LOWER(metal) = LOWER(?)")
        params.append(canonical)

    if is_count and is_random:
        raise ValueError("Cannot use count and random together.")

    recognised = any([where_clauses, is_count, is_random, sort_column])

    if not recognised:
        raise ValueError("Unknown query.")

    if is_count:
        sql = "SELECT COUNT(*) FROM coins"
    else:
        sql = """SELECT year, denomination, monarch, metal, fineness, mintmark, variety, grade FROM coins"""

    if where_clauses:
        where_part = " WHERE " + " AND ".join(where_clauses)
        sql += where_part
    else:
        where_part = " "
    
    count_sql = None
    if limit_value is not None:
       count_sql = "SELECT COUNT(*) FROM coins" + where_part

    if is_random and not is_count:
        sql += " ORDER BY RANDOM()"
    elif sort_column and not is_count:
        sql += f" ORDER BY {sort_column}"

    if limit_value is not None and not is_count:
        sql += f" LIMIT {limit_value}"
    elif is_random and not is_count:
        sql += " LIMIT 1"

    return sql, params, is_count, is_random, count_sql

def parse_explicit_query(user_input, aliases):
    limit_value = None
    is_count = False
    is_random = False
    tokens = user_input.lower().strip().split()

    if not tokens:
        return None, [], False, False, None
    
    if tokens[0] == "quit":
        return "QUIT", [], False, False, None
    
    if tokens[0] == "help":
        return "HELP", [], False, False, None

    where_clauses = []
    params = []
    sort_column = None

    i = 0
    t_len = len(tokens)

    while i < t_len:
        x = i + 1
        token = tokens[i].lower()
        token = TOKEN_ALIASES.get(token, token)

        if token == "before" and x < t_len:
            where_clauses.append("year < ?")
            params.append(int(tokens[x]))
            i += 2
        elif token == "limit" and x < t_len:
            limit_value = int(tokens[x])
            i += 2
        elif token == "year" and x < t_len:
            where_clauses.append("year == ?")
            params.append(int(tokens[x]))
            i += 2
        elif token == "after" and x < t_len:
            where_clauses.append("year > ?")
            params.append(int(tokens[x]))
            i += 2
        elif token == "monarch" and x < t_len:
            value, i = collect_value(tokens, x, TOKEN_ALIASES, STOP_WORDS)
            value = resolve_alias(value, aliases["monarchs"])
            where_clauses.append(ci_equals("monarch"))
            params.append(value)
        elif token == "denomination" and x < t_len:
            value, i = collect_value(tokens, x, TOKEN_ALIASES, STOP_WORDS)
            value = resolve_alias(value, aliases["denominations"])
            where_clauses.append(ci_equals("denomination"))
            params.append(value)
        elif token == "metal" and x < t_len:
            value, i = collect_value(tokens, x, TOKEN_ALIASES, STOP_WORDS)
            value = resolve_alias(value, aliases["metals"])
            where_clauses.append(ci_equals("metal"))
            params.append(value)
        elif token == "silver":
            where_clauses.append("fineness > 0")
            i += 1
        elif token == "grade" and x < t_len:
            value, i = collect_value(tokens, x, TOKEN_ALIASES, STOP_WORDS)
            value = resolve_alias(value, aliases["grades"])
            where_clauses.append(ci_equals("grade"))
            params.append(value)
        elif token == "mintmark" and x < t_len:
            value, i = collect_value(tokens, x, TOKEN_ALIASES, STOP_WORDS)
            where_clauses.append(ci_equals("mintmark"))
            params.append(value)
        elif token == "variety" and x < t_len:
            value, i = collect_value(tokens, x, TOKEN_ALIASES, STOP_WORDS)
            where_clauses.append(ci_equals("variety"))
            params.append(value)
        elif token == "sort" and x < t_len:
            candidate = tokens[x].lower()
            candidate = TOKEN_ALIASES.get(candidate, candidate)

            if candidate in ALLOWED_SORT_COLUMNS:
                sort_column = candidate
            i += 2
        elif token in TYPE_WORDS:
            i += 1
            if token == "count":
                is_count = True
            if token == "random":
                is_random = True
        else:
            raise ValueError(f"Unknown or incomplete token: {tokens[i]}")
        
    if is_count:
        sql = "SELECT COUNT(*) FROM coins"
    else:
        sql = """
        SELECT year, denomination, monarch, metal, fineness, mintmark, variety, grade
        FROM coins
        """

    if where_clauses:
        where_part = " WHERE " + " AND ".join(where_clauses)
        sql += where_part
    else:
        where_part = " "
    
    count_sql = None
    if limit_value is not None:
        count_sql = "SELECT COUNT(*) FROM coins" + where_part

    if is_random and not is_count:
        sql += " ORDER BY RANDOM()"
    elif sort_column and not is_count:
        sql += f" ORDER BY {sort_column}"

    if limit_value is not None and not is_count:
        sql += f" LIMIT {limit_value}"
    elif is_random and not is_count:
        sql += " LIMIT 1"

    return sql, params, is_count, is_random, count_sql

def parse_query(user_input, aliases):
    tokens = user_input.strip().split()
    if not tokens:
        return None, None, False, False, None
    
    if tokens[0].lower() == "show":
        user_input = " ".join(tokens[1:])
        tokens = user_input.strip().split()
        if not tokens:
            raise ValueError("Show what?")

    first = TOKEN_ALIASES.get(tokens[0].lower(), tokens[0].lower())

    if first in COMMANDS:
        return parse_explicit_query(user_input, aliases)
    
    return parse_natural_query(user_input, aliases)