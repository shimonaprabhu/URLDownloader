from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context, request
from time import sleep
from threading import Thread, Event
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

#Data Generator Thread
thread = Thread()
thread_stop_event = Event()
class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()

    def dataGenerator(self):
        """
        Generate the request in chunks and process the data accordingly
        """
        done=0
        
        if (round(total_length/(2**30))) > 0: 
            chunk_size=1024*1024*1024
        elif (round(total_length/(2**20))) > 0:
            chunk_size=1024*1024
        else:
            chunk_size=1024
        print(chunk_size)
        for data in r.iter_content(chunk_size):
            done += len(data)   # Keep track of file length downloaded
            if total_length-done<0:
                exit
            else:
                left=total_length-done  # Keep track of file length left to be downloaded
            socketio.emit('newnumber', {'left': left, 'done':done, 'total':total_length, 'displ':chunk_size} , namespace='/test')
            sleep(self.delay)

    def run(self):
        self.dataGenerator()

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/download', methods=['POST', 'GET'])
def down():
    global url
    url=request.form['url']
    global r
    r=requests.get(url, stream=True)
    global total_length
    total_length = int(r.headers.get('content-length'))
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread()
        thread.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)