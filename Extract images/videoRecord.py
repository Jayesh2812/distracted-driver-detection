from Video import Video, Camera
source = '../demo_media/demo.mp4'
video = Video(source, name = "Laptop Record", seconds_to_run = None)
video.stop_send = True
video.show()
