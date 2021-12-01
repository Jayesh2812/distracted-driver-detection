from Video import Video, Camera
source = Camera.phone
video = Video(source, name = "Laptop Record", seconds_to_run = None)
video.stop_send = True
video.show()
