import cv2
import requests
import sys
from requests.auth import HTTPBasicAuth
import threading
payload = HTTPBasicAuth('admin', 'admin')
content_type = 'image/jpeg'
headers = {'content-type': content_type}
url = 'http://127.0.0.1:8000/upload/'
device = int(sys.argv[1])
from datetime import datetime
class Webcam:
    phone = 1
    laptop = 0
class Video:
    def __init__(self, name = 'Frames', seconds_to_run=10):
        self.name = name
        self.frames=[]
        self.record = False
        self.startTime = None
        self.endTime = None
        self.vid = cv2.VideoCapture(device)
        self.msg = 'Press Spacebar to start recording'
        self.seconds_to_run = seconds_to_run
        self.FPS = 2
        self.max_fps = 0
        self.total_frames = 0
        self.total_run_time = 0
        self.prev = 0
        self.QUEUE = []
    
    def show(self):
        cv2.namedWindow(self.name) 
        while(True):
            _, frame = self.vid.read()
            modified_frame = frame.copy()
            modified_frame = cv2.putText(modified_frame, str(self.msg), (20,40),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),1, cv2.LINE_AA)
            # cv2.imwrite(f"I{len(self.frames)}.png", frame)  
            if self.record:
                self.msg = f"""{self.endTime - self.startTime} | Press Spacebar to stop recording"""
                self.endTime = datetime.now()

                if self.seconds_to_run:
                    if self.endTime.timestamp() - self.startTime.timestamp() > self.seconds_to_run:
                        self.startStopRecord()
                self.addFrame(frame)
            
            cv2.imshow(self.name, modified_frame)
            waitKey = cv2.waitKey(1) 
            if waitKey:
                if waitKey & 0xFF == ord(' '):
                    self.startStopRecord()
                if waitKey & 0xFF == ord('q'):
                    self.quit()
                    break

    def startStopRecord(self):
        # if not self.record:
        #     self.seconds_to_run = int(input("Enter no of seconds : ") or 0)
        #     print(self.seconds_to_run)
        if not self.total_run_time:
            self.total_run_time = datetime.now()

        self.record = not self.record
        if not self.record:
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
        if datetime.now().timestamp() - self.prev.timestamp() > 1:
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
        interval = len(self.frames) / (self.FPS + 1)
        print('Interval' , interval)
        for i in range(1, self.FPS + 1):
            frame_number = round(i * interval)
            print(frame_number)
            # self.send(self.frames[frame_number])
            # sending = threading.Thread(target=self.enqueue_frames, args=(self.frames[frame_number],))
            # sending.start()



    def send(self, frame):
        
        import os
        print('Sending Images ...')

        # print('Sending Complete ...')

        p = cv2.imwrite(f'./temp.jpg', frame)
        f = open('./temp.jpg','rb' )
        response = requests.post(url, auth=payload , files= {'image':f})
        f.close()
        os.remove('./temp.jpg')
        print(response.text)
        return True

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

video = Video(seconds_to_run=0)
video.show()
# print(video.details())
