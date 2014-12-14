from flask import Flask, session
from dict_utils import LRUCache
import gtfs
from quiz_manager import QuizManager, DifficultyLevel

app = Flask(__name__)
app.secret_key = 'A0zR98j/3yX R~XHH!jmN]LWX/,?RT'

quiz_managers = LRUCache(1024)

@app.route('/')
def hello_world():
    while 'quiz_manager_id' in session:
        try:
            quiz_manager = quiz_managers.get(session['quiz_manager_id'])
            break
        except:
            session.pop('quiz_manager_id')
    else:
        quiz_manager = QuizManager(agency)
        quiz_managers.set(quiz_manager.get_instance_id(), quiz_manager)
        session['quiz_manager_id'] = quiz_manager.get_instance_id()

    return 'Hello World! Your quiz manager is ' + str(quiz_manager.get_instance_id())

if __name__ == '__main__':
    agency = gtfs.TransitAgency("/Users/spencert/Projects/transit-quiz/gtfs/kcmetro")
    app.run(debug=True)

