from app.core.domain_config import DOMAINS

VALID_DIFFICULTY = {"Easy", "Medium", "Hard"}

def validate_request(data):
    domain = data.domain
    difficulty = data.difficulty
    num_questions = data.num_questions

    # 1. Domain validation
    if domain not in DOMAINS:
        raise ValueError(f"Unsupported domain: {domain}")

    # 2. Difficulty validation
    if difficulty not in VALID_DIFFICULTY:
        raise ValueError(f"Invalid difficulty: {difficulty}")

    topics = DOMAINS[domain]

    # 3. Minimum coverage enforcement
    if num_questions < len(topics):
        raise ValueError(
            f"num_questions must be >= {len(topics)} (topics count)"
        )

    return data