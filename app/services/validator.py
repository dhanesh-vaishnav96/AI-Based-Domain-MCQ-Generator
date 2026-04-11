# from app.utils.normalizer import normalize_text

# seen_questions = set()

# REQUIRED_FIELDS = {
#     "question",
#     "option_a",
#     "option_b",
#     "option_c",
#     "option_d",
#     "answer",
#     "difficulty",
#     "points"
# }


# def validate_schema(mcq: dict):
#     # Check all required fields exist
#     if not REQUIRED_FIELDS.issubset(mcq.keys()):
#         return False

#     # Ensure answer is valid
#     if mcq["answer"] not in ["option_a", "option_b", "option_c", "option_d"]:
#         return False

#     return True


# def is_duplicate(mcq: dict):
#     normalized = normalize_text(mcq["question"])

#     if normalized in seen_questions:
#         return True

#     seen_questions.add(normalized)
#     return False


# def validate_quality(mcq: dict):
#     # Question length check
#     if len(mcq["question"]) < 15:
#         return False

#     # Options should not be identical
#     options = {
#         mcq["option_a"],
#         mcq["option_b"],
#         mcq["option_c"],
#         mcq["option_d"]
#     }

#     if len(options) < 4:
#         return False

#     return True


# def validate_mcq_list(mcqs: list):
#     valid_mcqs = []

#     for mcq in mcqs:
#         if not validate_schema(mcq):
#             continue

#         if is_duplicate(mcq):
#             continue

#         if not validate_quality(mcq):
#             continue

#         valid_mcqs.append(mcq)

#     return valid_mcqs


# def fill_missing_questions(current_mcqs, target_count, generate_func):
#     while len(current_mcqs) < target_count:
#         new_mcqs = generate_func()

#         for mcq in new_mcqs:
#             if len(current_mcqs) >= target_count:
#                 break

#             if (
#                 validate_schema(mcq)
#                 and not is_duplicate(mcq)
#                 and validate_quality(mcq)
#             ):
#                 current_mcqs.append(mcq)

#     return current_mcqs

# validator.py

from app.utils.normalizer import normalize_text

REQUIRED_FIELDS = {
    "question",
    "option_a",
    "option_b",
    "option_c",
    "option_d",
    "answer",
    "difficulty",
    "points"
}

VALID_ANSWERS = {"option_a", "option_b", "option_c", "option_d"}

DIFFICULTY_POINTS = {
    "Easy": 1,
    "Medium": 1.5,
    "Hard": 2
}


# -------------------------------
# SCHEMA VALIDATION
# -------------------------------
def validate_schema(mcq: dict) -> bool:
    # Check required fields
    return REQUIRED_FIELDS.issubset(mcq.keys()) and mcq["answer"] in VALID_ANSWERS

# -------------------------------
# QUALITY VALIDATION
# -------------------------------
def validate_quality(mcq: dict) -> bool:
    question = mcq.get("question", "").strip()

    # Question length
    if len(question) < 15:
        return False

    # Options
    options = [
        mcq.get("option_a", "").strip(),
        mcq.get("option_b", "").strip(),
        mcq.get("option_c", "").strip(),
        mcq.get("option_d", "").strip()
    ]

    return len(set(options)) == 4

# -------------------------------
# DIFFICULTY VALIDATION
# -------------------------------
def validate_difficulty(mcq: dict) -> bool:
    diff = mcq.get("difficulty")

    return diff in DIFFICULTY_POINTS and mcq.get("points") == DIFFICULTY_POINTS[diff]

# -------------------------------
# DUPLICATE CHECK
# -------------------------------
def is_duplicate(mcq: dict, seen: set):
    q = normalize_text(mcq.get("question", ""))
    if q in seen:
        return True
    seen.add(q)
    return False

# -------------------------------
# MAIN VALIDATOR
# -------------------------------
def validate_mcq_list(mcqs: list) -> list:
    valid_mcqs = []
    seen_questions = set()

    for mcq in mcqs:
        if not isinstance(mcq, dict):
            continue

        if not validate_schema(mcq):
            continue

        if not validate_quality(mcq):
            continue

        if not validate_difficulty(mcq):
            continue

        if is_duplicate(mcq, seen_questions):
            continue

        valid_mcqs.append(mcq)

    return valid_mcqs


# -------------------------------
# FILL MISSING QUESTIONS (SAFE)
# -------------------------------
def fill_missing_questions(
    current_mcqs: list,
    target_count: int,
    generate_func,
    max_attempts: int = 10
) -> list:

    attempts = 0
    seen_questions = {normalize_text(q["question"]) for q in current_mcqs if "question" in q}

    while len(current_mcqs) < target_count and attempts < max_attempts:
        attempts += 1

        try:
            new_mcqs = generate_func()
        except Exception:
            continue

        for mcq in new_mcqs:
            if len(current_mcqs) >= target_count:
                break

            if not isinstance(mcq, dict):
                continue

            if (
                validate_schema(mcq)
                and validate_quality(mcq)
                and validate_difficulty(mcq)
                and not is_duplicate(mcq, seen_questions)
            ):
                current_mcqs.append(mcq)

    return current_mcqs