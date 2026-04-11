def distribute_topics(topics, num_questions):
    distributed = []

    total_topics = len(topics)

    for i in range(num_questions):
        topic = topics[i % total_topics]
        distributed.append(topic)

    return distributed