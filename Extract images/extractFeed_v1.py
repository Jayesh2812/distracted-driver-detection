import cv2
import time
import os
from datetime import datetime
import json
fps = 2
seconds_to_run = 10
vid = cv2.VideoCapture(0)
cv2.namedWindow('frame') 
frames = []
start = datetime.now().timestamp()
end = datetime.now().timestamp()
record = False
print("Start :", start)
while(True):
    print(datetime.now().timestamp() - start)
    time.sleep(5)
    ret, frame = vid.read()
    # frames.append(frame)
    frame = cv2.putText(frame, str(end), (20,40),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),1, cv2.LINE_AA)
    cv2.imshow('frame', frame)
    print(len(frames))
    # cv2.imwrite(f"images\{len(frames)}.png", frame)  

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # if end-start <= seconds_to_run:
    #     break
    end = datetime.now().timestamp()

# After the loop release the cap object
print("Start :", start)
print("End :", end)
print("Total Time : ",end-start)
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()


# Save data
f = open('data.json', 'r')
data = json.load(f)
f.close()
f = open('data.json', 'w')
data[str(seconds_to_run)] = {'frames':len(frames), fps:len(frames)/seconds_to_run}
f.write(json.dumps(data))
f.close()
