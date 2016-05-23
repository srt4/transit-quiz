from flask import Flask, session, render_template
import gtfs
import json
from quiz_manager import DifficultyLevel, QuizManagerRepository

app = Flask(__name__)
app.secret_key = 'A0zR98j/3yX R~XHH!jmN]LWX/,?RT'

quiz_manager_repository = None

@app.route('/')
def begin_quiz():
    if 'quiz_manager_id' not in session:
        session['quiz_manager_id'] = quiz_manager_repository.initialize_quiz_manager(DifficultyLevel.EXTREMELY_DIFFICULT, 10)
    quiz_manager = quiz_manager_repository.get_quiz_manager(session['quiz_manager_id'])
    return render_template('main.html', quiz_manager=quiz_manager)


if __name__ == '__main__':
    agency = gtfs.TransitAgency("/Users/spencert/Projects/transit-quiz/gtfs/capmetro")
    quiz_manager_repository = QuizManagerRepository(agency)
    app.run(debug=True)
