import cv2

def GetImage():
    cap = cv2.VideoCapture(0)
    # Capture frame
    ret, frame = cap.read()
    cap.release()
    if ret:
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
    return encodedImage
