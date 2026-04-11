# def build_prompt(topic: str, difficulty: str, domain: str, num_questions: int):
    
#     prompt = f"""
# You are a highly strict MCQ generation engine.

# TASK:
# Generate EXACTLY {num_questions} multiple choice questions.

# CONTEXT:
# - Domain: {domain}
# - Topic: {topic}
# - Difficulty: {difficulty}

# QUESTION STYLE:
# - Domain-specific and concept-focused (NOT scenario-based)
# - Test deep understanding of concepts
# - Avoid generic or repeated textbook questions
# - Each question must be UNIQUE

# OPTIONS RULE:
# - Exactly 4 options per question
# - All options must be plausible
# - Only ONE correct answer

# DIFFICULTY & POINTS RULE:
# - Easy → 1 point
# - Medium → 1.5 points
# - Hard → 2 points
# - All generated questions MUST match difficulty: {difficulty}

# OUTPUT FORMAT (STRICT JSON ARRAY ONLY):

# [
#   {{
#     "question": "string",
#     "option_a": "string",
#     "option_b": "string",
#     "option_c": "string",
#     "option_d": "string",
#     "answer": "option_a",
#     "difficulty": "{difficulty}",
#     "points": 2
#   }}
# ]

# IMPORTANT CONSTRAINTS:
# - Return ONLY valid JSON array
# - Do NOT return explanations
# - Do NOT return markdown
# - Do NOT include extra text
# - Do NOT change schema
# - Do NOT include trailing commas
# - Ensure all questions are different
# - Ensure valid JSON syntax

# FAIL CONDITIONS (STRICTLY AVOID):
# - No text outside JSON
# - No missing fields
# - No duplicate questions
# - No invalid JSON

# FINAL CHECK BEFORE OUTPUT:
# - Count of questions = {num_questions}
# - JSON is valid
# - All fields present
# """

#     return prompt.strip()



def build_prompt(topic: str, difficulty: str, domain: str, num_questions: int):

    prompt = f"""
You are a STRICT JSON-only generator for high-quality MCQ questions.
You MUST follow ALL rules. If ANY rule is violated, REGENERATE internally until correct.

================================
TASK
================================
Generate EXACTLY {num_questions} UNIQUE, NON-REPEATED multiple-choice questions.

================================
CONTEXT
================================
Domain: {domain}
Topic: {topic}
Difficulty: {difficulty}

================================
CORE RULES (MANDATORY)
================================
- Questions MUST be concept-based (no scenarios, no storytelling)
- Each question MUST test a DIFFERENT concept
- NO duplicate or rephrased questions
- NO repeated concepts (even if wording changes).  (important)
- Ensure technical correctness (VERY IMPORTANT)
- Avoid generic or repeated textbook questions
- must not generate the Repeted questions (MOST IMPORTANT)
- must not generate the Same type of questions also (important)
- always give each questions has the correct answer is truly correct (VERY VERY MOST IMPORTANT)

================================
UNIQUENESS ENFORCEMENT
================================
Before final output:
- Compare all questions
- Remove duplicates or similar concepts
- Ensure each question is DISTINCT in meaning

================================
OPTIONS RULE (STRICT)
================================
- Exactly 4 options: option_a, option_b, option_c, option_d
- Only ONE correct answer
- All options must be logically distinct
- Avoid ambiguous or partially correct options
- Incorrect options must be plausible but clearly wrong

================================
ANSWER VALIDATION (CRITICAL)
================================
For EACH question:
- Verify the correct answer is 100% accurate (MOST IMPORTANT)
- Ensure NO other option can be correct
- If ambiguity exists → FIX the question

================================
DIFFICULTY RULE (STRICT)
================================
Difficulty: "{difficulty}"

- Easy → basic definition
- Medium → conceptual understanding
- Hard → deep/internal/advanced concept

Points:
- Easy → 1
- Medium → 1.5
- Hard → 2

================================
OUTPUT FORMAT (STRICT)
================================
Return ONLY a valid JSON array.

Each object MUST follow EXACT structure:
[
  {{
    "question": "Clear question text without quotes inside",
    "option_a": "Option A",
    "option_b": "Option B",
    "option_c": "Option C",
    "option_d": "Option D",
    "answer": "option_a",
    "difficulty": "{difficulty}",
    "points": 2
  }}
]

================================
JSON RULES (STRICT)
================================
- ONLY double quotes (")
- NO trailing commas
- NO comments
- NO explanation
- NO markdown
- NO extra text
- NO invalid escape characters
- NO newline inside string values

================================
ANTI-FAIL SAFE
================================
If ANY rule is violated:
- DO NOT return output
- REGENERATE internally until ALL rules pass

================================
FINAL VALIDATION (MANDATORY)
================================
Before returning:
- Total questions = {num_questions}
- All questions are UNIQUE (no repetition in concept)
- Confirm the correct answer is truly correct
- JSON is valid and parsable
- No duplicate options
- No formatting errors
- Check that other options are incorrect
- Ensure no duplication or overlap
- each questions has the correct answer is truly correct (VERY MOST IMPORTANT )

If any issue is found, FIX the question before output.
Return only the final corrected JSON.
"""
    return prompt.strip()