from typing import Union
import cv2
import requests
import sys
from requests.auth import HTTPBasicAuth
import threading
import base64
from datetime import datetime
class Camera:
    phone = 1
    laptop = 0

class Video:
    def __init__(self, source : Union[int, str] , name : str = 'Frames', seconds_to_run : Union[int, None] = 10):
        '''
            Initializes Video Capture and defines variables to be used across the class
            :param source
        '''
        self.name = name 
        self.frames=[]
        self.is_recording = False
        self.startTime = None
        self.endTime = None
        self.is_pre_recorded_video = isinstance(source, str)
        self.vid = cv2.VideoCapture(source)
        self.msg = 'Press Spacebar to start recording'
        self.seconds_to_run = seconds_to_run
        self.FPS_limit = 30
        self.enable_FPS_limiter = False
        self.max_fps = 0
        self.total_frames = 0
        self.total_run_time = 0
        self.prev = 0
        self.stop_send = False
        self.time_interval = 1
        self.flip = False
    
    def show(self):
        cv2.namedWindow(self.name) 
        _, frame = self.vid.read()
        frame = cv2.flip(frame, 1) if self.flip else frame

        while(True):
            if not self.is_pre_recorded_video or self.is_recording:
                _, frame = self.vid.read()
                frame = cv2.flip(frame, 1) if self.flip else frame


            if frame is None:
                self.quit()
                return

            modified_frame = frame.copy()
            cv2.rectangle(modified_frame, (20,25), (len(self.msg)*9, 45), (0,0,0), -1)
            modified_frame = cv2.putText(modified_frame, str(self.msg), (20,40),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),1, cv2.LINE_AA)

            if self.is_recording:
                self.msg = f"""{self.endTime - self.startTime} | Press Spacebar to stop recording"""
                self.endTime = datetime.now()

                if self.seconds_to_run:
                    if self.endTime.timestamp() - self.startTime.timestamp() > self.seconds_to_run:
                        self.startStopRecord()
                self.addFrame(frame)
            
            cv2.imshow(self.name, modified_frame)

            waitKey = cv2.waitKey(25) # Wait Untill this milliseconds before showing next frame
            if waitKey:
                if waitKey & 0xFF == ord(' '):
                    self.startStopRecord()
                if waitKey & 0xFF == ord('q'):
                    self.quit()
                    break

    def startStopRecord(self):
        # if not self.is_recording:
        #     self.seconds_to_run = int(input("Enter no of seconds : ") or 0)
        #     print(self.seconds_to_run)
        if not self.total_run_time:
            self.total_run_time = datetime.now()

        self.is_recording = not self.is_recording
        if not self.is_recording:
            self.msg = f"""{self.endTime - self.startTime} | Press Q to quit | Press Spacebar to Restart recording """
            if len(self.frames) > self.max_fps:
                self.max_fps = len(self.frames)
            self.frames = []

            self.details()
            self.total_frames = 0
        self.startTime = datetime.now()
        self.endTime = datetime.now()
        self.prev = datetime.now()
        
    def addFrame(self, frame):
        self.total_frames += 1
        if datetime.now().timestamp() - self.prev.timestamp() > self.time_interval or (self.enable_FPS_limiter and len(self.frames) > self.FPS_limit):
            self.prev = datetime.now()
            if len(self.frames) > self.max_fps:
                self.max_fps = len(self.frames)
            print("No of Frames : ", len(self.frames))
            self.save()
            self.frames = []
            self.details()
        self.frames.append(frame)

    def save(self):
        '''
            Gives the interval at which the frames should be saved to get required frames per second uniformly
        '''
        chosen_index = 3
        index = 0 if len(self.frames) <= chosen_index else chosen_index

        try: 
            frame = self.frames[index]
            base64_frame = base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode()
            try: 
                sending = threading.Thread(target=self.send, args=(base64_frame,))
                if not self.stop_send:
                    sending.start()
                # self.send(base64_frame)
            except Exception as e:
                raise e
        except IndexError as e:
            print("Frames List is Empty")
            raise e

        # interval = len(self.frames) / (self.FPS + 1)
        # print('Interval' , interval)
        # for i in range(1, self.FPS + 1):
        #     frame_number = round(i * interval)
        #     print(frame_number)
            # self.send(self.frames[frame_number])
            # sending = threading.Thread(target=self.enqueue_frames, args=(self.frames[frame_number],))
            # sending.start()



    def send(self, frame_encoded):
        import requests
        from requests.auth import HTTPBasicAuth
        import time
        start = time.time()
        auth = HTTPBasicAuth('admin', 'admin')
        response = requests.post(
            url="http://localhost:8000/upload-encoded/",
            data={"image" : frame_encoded}, 
            auth = auth
        )
        end = time.time()
        print("Time taken to upload: ", end-start)


    def enqueue_frames(self, frame):
        # send(frame)
        pass

    def now(self):
        return datetime.now().timestamp()

    def quit(self):
        self.vid.release()
        cv2.destroyAllWindows()

    def details(self):
        self.total_run_time = self.endTime - self.startTime

        data = {
            "Max Frames Per Second" : self.max_fps,
            "Total Frames" : self.total_frames,
            "Total Run Time" : self.total_run_time,
            "Average Frames Per second" : self.total_frames / self.total_run_time.total_seconds()
        }
        for i in data:
            print(f"{i} : {data[i]}")

        print('----------------------------------------------------------')
        return data

if __name__ == "__main__":
    video = Video(seconds_to_run=2)
    video.show()
