import time
from collections import defaultdict
from app.services.llm_service import generate_with_retry


def generate_mcqs_topicwise(
    build_prompt,
    distributed_topics,
    difficulty,
    domain
):
    topic_map = defaultdict(int)

    # Count how many questions per topic
    for topic in distributed_topics:
        topic_map[topic] += 1

    all_mcqs = []

    for topic, count in topic_map.items():
        remaining = count

        while remaining > 0:
            BATCH_SIZE = 5
            current_batch = min(BATCH_SIZE, remaining)

            prompt = build_prompt(
                topic=topic,
                difficulty=difficulty,
                domain=domain,
                num_questions=current_batch
            )

            batch_mcqs = generate_with_retry(prompt)

            all_mcqs.extend(batch_mcqs)

            remaining -= current_batch

            time.sleep(2)  # avoid rate limit

    return all_mcqs