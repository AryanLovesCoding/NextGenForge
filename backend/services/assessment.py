from data.questions import questions

def calculate_scores(responses):
    scores = {"STEM": 0, "Commerce": 0, "Humanities": 0, "Design/Creative Arts": 0}
    for question, response in zip(questions, responses):
        domain = question["domain"]
        if domain in scores:
            scores[domain]+=response

    for domain in scores:
        scores[domain] /= 25

    return scores
            