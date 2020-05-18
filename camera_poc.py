import cv2

cap = cv2.VideoCapture(0)
i = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow("frame", frame)

    key = cv2.waitKey(1) & 0xff
    if key == ord("q"):
        break
    if key == ord("s"):
        print("save image")
        cv2.imwrite(f"image{i}.jpg", frame)
        i += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
