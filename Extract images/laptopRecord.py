from Video import Video, Camera
source = Camera.laptop
video = Video(source, name = "Laptop Record", seconds_to_run = None)
# video.stop_send = True
video.flip = True
video.show()
