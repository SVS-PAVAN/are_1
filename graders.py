def base_checks(history):
    used_db = any("query_db" in h for h in history)
    used_calc = any("calculate" in h for h in history)
    used_reflect = any("reflect" in h for h in history)

    score = 0.0
    if used_db:
        score += 0.2
    if used_calc:
        score += 0.2
    if used_reflect:
        score += 0.2

    return score


def grade_easy(answer, history):
    score = base_checks(history)
    if "1350000" in answer:
        score += 0.4
    return min(score, 1.0)


def grade_medium(answer, history):
    score = base_checks(history)
    if "manager" in answer.lower():
        score += 0.4
    return min(score, 1.0)


def grade_hard(answer, history):
    score = base_checks(history)
    text = answer.lower()

    if "global" in text:
        score += 0.2
    if "increase" in text:
        score += 0.2

    return min(score, 1.0)