import cv2
import time

# initalize the cam
cap = cv2.VideoCapture(0)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()


def ReadQR():
    _, img = cap.read()
    # detect and decode
    data, bbox, _ = detector.detectAndDecode(img)
    # check if there is a QRCode in the image
    if bbox is not None:
        # display the image with lines
        for i in range(len(bbox)):
            # draw all lines
            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i + 1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
        if data:
            return data
        

def __main__():
    print("System ON")
    while(True):
        print("[INFO] QR Code Información:", ReadQR())
        time.sleep(2)
        
    print("System Completed!!")


if __name__ == '__main__':
    __main__()
