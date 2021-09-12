import cv2
vid = cv2.VideoCapture(1)
cv2.namedWindow('frame') 
while(True):
    ret, frame = vid.read()
    # frames.append(frame)
    cv2.imshow('frame', frame)
    # cv2.imwrite(f"images\{len(frames)}.png", frame)  

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break