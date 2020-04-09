import threading
import StreamingUDP.StreamingC as Stream

def startStreaming(video,i):
    Stream.Streaming(video, 8000 + i)


video=["../Doc/Prueba4.mp4", "../Doc/Prueba5.mp4"]
for i in range(2):
    t = threading.Thread(target=startStreaming, args=(video[i],i,))
    t.start()