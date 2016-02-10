# written by Gustavo Hernando Puma Tejada

import cv2
import pytz
import ntpath
import time
from datetime import datetime

from tzlocal import get_localzone
from ftplib import FTP


# gets the UTC offset in hours
def get_utc_offset(d):
    return int(d.utcoffset().total_seconds() / 3600)


# returns the string version of the UTC time and local time
# for displaying purposes
def get_time_str():
    d = datetime.now(get_localzone())
    utc_t = datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S") + ' UTC'
    offset = get_utc_offset(d)
    # todo: should utc0 be 'UTC+0'?
    offset_str = '+' + str(offset) if offset >= 0 else str(offset)
    local_t = d.strftime("%Y-%m-%d %H:%M:%S UTC") + offset_str
    return utc_t, local_t


# saves the specified frame to disk
# returns the full path to the file
def take_snapshot(f):
    full_img_path = img_path + "caca" + ".jpg"
    cv2.imwrite(full_img_path, f, img_params)
    print 'img has been saved'
    return full_img_path


# reads the ftp details from a text file
# text file should have three lines:
# <host>
# <user>
# <password>
def get_ftp_credentials(filename):
    with open(filename) as f:
        content = f.readlines()
    return [x.strip('\n') for x in content]


def upload(ftp, full_path):
    # we only specify filename on the server; no path
    fn_only = ntpath.split(full_path)[1]
    print "STOR " + fn_only
    ftp.storbinary("STOR " + fn_only, open(full_path, "rb"))

# huge loop
while True:
    img_path = "D:\\"
    img_params = [cv2.IMWRITE_JPEG_QUALITY, 60]
    # starting point for both timestamps
    org_pos = (0, 30)
    org_pos2 = (0, 60)
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    rval = False

    # we loop until we get a frame
    while not rval:
        # try to get the first frame
        if vc.isOpened():
            rval, frame = vc.read()
        else:
            rval = False
    utc_time, local_time = get_time_str()
    cv2.putText(frame, local_time, org_pos, cv2.FONT_HERSHEY_DUPLEX, .8, (255,255,255), 1, lineType=8)
    cv2.putText(frame, utc_time, org_pos2, cv2.FONT_HERSHEY_DUPLEX, .8, (255,255,255), 1, lineType=8)
    img_path = take_snapshot(frame)

    # important! if not camera will remain ON
    vc.release()
    cv2.destroyAllWindows()

    # FTP UPLOAD
    host, user, pwd = get_ftp_credentials("ftp.txt")
    try:
        ftp = FTP(host)
        print 'connecting to host'
        ftp.login(user, pwd)
        print 'success. uploading image now...'
        ftp.cwd("public_html/")
        upload(ftp, img_path)
        print 'img upload was successful. disconnecting...'
    # so it doesn't print an error when a keyboard or system interrupt happnes
    except Exception:
        print 'problem with FTP connection'
    finally:
        ftp.quit()
    # every five minutes
    time.sleep(60 * 5)