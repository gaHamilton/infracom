from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import imutils
import time
import cv2

from StreamingUDP.webstreaming import generate, app


class Streaming():
    outputFrame = None
    lock = threading.Lock()
    # initialize a flask object
    app = Flask(__name__)
    pausePlay = False
    time.sleep(2.0)
    videoDir = ""
    port = 0

    def detect_motion(self, videoDir):
        vs3 = cv2.VideoCapture(videoDir)
        # loop over frames from the video stream
        frame_counter = 0
        while True:
            # read the next frame from the video stream, resize it,
            # convert the frame to grayscale, and blur it
            # TODO elegir vs, aunque en verdad solo sirve para vs3 por como esta ahora
            # frame = vs.read()
            # ret, frame = vs2.read()
            ret, frame = vs3.read()

            if not ret:
                frame_counter = 0
                vs3.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = vs3.read()
            frame_counter += 1

            # frame = imutils.resize(frame, width=800)

            while pausePlay:
                # cv2.imshow("Video en puerto " + str(port), frame)
                continue

            # cv2.imshow("Video en puerto " + str(port), frame)
            # acquire the lock, set the output frame, and release the
            # lock
            with self.lock:
                self.outputFrame = frame.copy()

    def generate(self):
        # loop over frames from the output stream
        while True:
            # wait until the lock is acquired
            with self.lock:
                # check if the output frame is available, otherwise skip
                # the iteration of the loop
                if self.outputFrame is None:
                    continue
                # encode the frame in JPEG format
                (flag, encodedImage) = cv2.imencode(".jpg", self.outputFrame)
                # ensure the frame was successfully encoded
                if not flag:
                    continue
            # yield the output frame in the byte format
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(encodedImage) + b'\r\n')

    def __init__(self, video, puerto):
        ip = "0.0.0.0"
        self.videoDir=video
        self.port=puerto
        t = threading.Thread(target=self.detect_motion, args=(video,))
        t.daemon = True
        t.start()

        self.app.run(host=ip, port=puerto, debug=True, threaded=True, use_reloader=False)
        self.vs3.release()

@app.route("/")
def index():
    # return the rendered template
    print("index")
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/PausePlay", methods=["GET"])
def PausePlay():
    global pausePlay
    with Streaming.lock:
        pausePlay = not pausePlay
    # print("PAUSE PLAY:", pausePlay)
    return str(Streaming.pausePlay)