from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import imutils
import time
import cv2

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to
# warmup
# TODO Elegir vs
# vs = VideoStream(src=0).start()
# vs2 = cv2.VideoCapture(0)
vs3 = cv2.VideoCapture('../Doc/Prueba4.mp4')
time.sleep(2.0)


@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


def detect_motion():
    # grab global references to the video stream, output frame, and
    # lock variables
    global vs, outputFrame, lock

    # loop over frames from the video stream
    frame_counter = 0
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        # TODO elegir vs, aunque en verdad solo sirve para vs3
        # frame = vs.read()
        # ret, frame = vs2.read()
        ret, frame = vs3.read()

        if not ret:
            frame_counter =0
            vs3.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = vs3.read()
        frame_counter += 1

        frame = imutils.resize(frame, width=800)
        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = frame.copy()



def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


# check to see if this is the main thread of execution
if __name__ == '__main__':
    # # construct the argument parser and parse command line arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--ip", type=str, required=True,
    #                 help="ip address of the device")
    # ap.add_argument("-o", "--port", type=int, required=True,
    #                 help="ephemeral port number of the server (1024 to 65535)")
    # ap.add_argument("-f", "--frame-count", type=int, default=32,
    #                 help="# of frames used to construct the background model")
    # args = vars(ap.parse_args())

    # assign ip and port, above is to receive it as parameters when running the command
    ip = "0.0.0.0"
    port = 8000

    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_motion, args=())
    t.daemon = True
    t.start()
    # start the flask app

    # With command ------> host=args["ip"], port=args["port"],
    # Without -----------> host=ip, port=port,
    app.run(host=ip, port=port, debug=True, threaded=True, use_reloader=False)
# release the video stream pointer
# TODO Elegir vs
# vs.stop()
# vs2.release()
vs3.release()
