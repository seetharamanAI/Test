from flask import Blueprint, redirect, render_template, request, session, url_for

from app.quiz_data import QUESTIONS

quiz_bp = Blueprint("quiz", __name__, url_prefix="/quiz")


@quiz_bp.route("/")
def start():
    session["quiz_index"] = 0
    session["quiz_score"] = 0
    return redirect(url_for("quiz.question"))


@quiz_bp.route("/question", methods=["GET", "POST"])
def question():
    index = session.get("quiz_index", 0)

    if request.method == "POST":
        selected = int(request.form["choice"])
        if selected == QUESTIONS[index]["answer"]:
            session["quiz_score"] = session.get("quiz_score", 0) + 1
        index += 1
        session["quiz_index"] = index

    if index >= len(QUESTIONS):
        return redirect(url_for("quiz.result"))

    return render_template(
        "quiz/question.html",
        question=QUESTIONS[index],
        index=index,
        total=len(QUESTIONS),
    )


@quiz_bp.route("/result")
def result():
    score = session.get("quiz_score", 0)
    total = len(QUESTIONS)
    return render_template("quiz/result.html", score=score, total=total)
