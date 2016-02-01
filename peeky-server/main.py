import cv2
import pytz
from datetime import datetime
from tzlocal import get_localzone


def get_utc_offset(d):
    return d.utcoffset().total_seconds() / 60 / 60


def get_time_str():
    d = datetime.now(get_localzone())
    utc_t = datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S") + ' UTC'
    offset = get_utc_offset(d)
    # todo: should utc0 be 'UTC+0'?
    offset_str = '+' + str(offset) if offset >= 0 else str(offset)
    local_t = d.strftime("%Y-%m-%d %H:%M:%S UTC") + offset_str
    return utc_t, local_t


img_path = "D:\\"
img_params = [cv2.IMWRITE_JPEG_QUALITY, 60]
# starting point for both timestamps
org_pos = (0, 30)
org_pos2 = (0, 60)
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    utc_time, local_time = get_time_str()
    cv2.putText(frame, local_time, org_pos, cv2.FONT_HERSHEY_DUPLEX, .8, (255,255,255), 1, lineType=8)
    cv2.putText(frame, utc_time, org_pos2, cv2.FONT_HERSHEY_DUPLEX, .8, (255,255,255), 1, lineType=8)
    key = cv2.waitKey(20)
    # exit on ESC
    if key == 27:
        break
    # if ENTER key
    if key == 13:
        y, x, z = frame.shape
        cv2.imwrite(img_path + "caca" + ".jpg", frame, img_params)
        print 'img has been saved'
cv2.destroyWindow("preview")


