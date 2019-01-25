import os
import glob
import numpy as np
import cv2

font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 1
fontColor              = (0,0, 255)
lineType               = 2

for f_in in glob.glob('nq*.jpg'):
    img_in = cv2.imread(f_in)
    fn, fext = os.path.splitext(f_in)
    txt = fn
    txt_pos = (int(0.90*img_in.shape[1]), int(0.97*img_in.shape[0]))
    tmp = cv2.putText(img_in,txt, txt_pos, font, fontScale, fontColor, lineType)
    cv2.imwrite("wg-%s%s"%(fn,fext), img_in)
