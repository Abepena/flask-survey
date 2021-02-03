from flask import (
    Flask,
    request,
    redirect,
    render_template,
    flash,
    jsonify,
    session,
    url_for,
)
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


debug = DebugToolbarExtension(app)


@app.route("/")
def index():
    # session.clear()
    context = {
        "title": satisfaction_survey.title,
        "instructions": satisfaction_survey.instructions,
    }
    return render_template("index.html", **context)


@app.route("/question/<int:question_id>")
def question_detail(question_id):
    """Render the question form for the survey"""
    questions_answered = session.get("questions_answered", 0)

    if questions_answered == len(satisfaction_survey.questions):
        return redirect("/thank-you")
    elif question_id != questions_answered:
        flash("Attempted to access an invalid question")
        return redirect(f"/question/{questions_answered}")

    question = satisfaction_survey.questions[question_id]
    return render_template("question.html", question=question)


@app.route("/answer", methods=["POST"])
def answer():
    answer = request.form.get("answer")
    next_question_id = session.get("question_id", 0) + 1
    session["question_id"] = next_question_id
    responses = session.get("responses", [])
    responses.append(answer)
    session["responses"] = responses
    session["questions_answered"] = session.get("questions_answered", 0) + 1

    if next_question_id >= len(satisfaction_survey.questions):
        return redirect("/thank-you")

    return redirect(url_for("question_detail", question_id=next_question_id))


@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")
