from app.quiz_data import QUESTIONS


def test_start_resets_session_and_redirects(client):
    response = client.get("/quiz/")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/quiz/question")


def test_first_question_renders(client):
    client.get("/quiz/")
    response = client.get("/quiz/question")
    assert response.status_code == 200
    assert QUESTIONS[0]["question"].encode() in response.data


def test_full_quiz_awards_perfect_score(client):
    client.get("/quiz/")
    for q in QUESTIONS:
        response = client.post("/quiz/question", data={"choice": q["answer"]})
        assert response.status_code in (200, 302)

    response = client.get("/quiz/result")
    assert response.status_code == 200
    assert f"{len(QUESTIONS)} out of {len(QUESTIONS)}".encode() in response.data


def test_wrong_answer_does_not_score(client):
    client.get("/quiz/")
    wrong_choice = (QUESTIONS[0]["answer"] + 1) % len(QUESTIONS[0]["choices"])
    client.post("/quiz/question", data={"choice": wrong_choice})

    with client.session_transaction() as sess:
        assert sess["quiz_score"] == 0
        assert sess["quiz_index"] == 1
