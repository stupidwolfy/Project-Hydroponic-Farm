import cv2

def GetImage(rotate = 0):
    cap = cv2.VideoCapture(0)
    # Capture frame
    ret, frame = cap.read()
    cap.release()
    if ret:
        if rotate == 90:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        elif rotate == 180:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
        elif rotate == 270:
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
    return encodedImage
