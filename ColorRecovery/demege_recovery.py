import numpy as np
import cv2

img = cv2.imread('profile_damage2.jpg')
mask = cv2.imread('mask2.png',0)

damage_recovery = cv2.inpaint(img,mask,3,cv2.INPAINT_TELEA)

cv2.imshow('damage_recovery_before',img)
cv2.imshow('damage_recovery_after',damage_recovery)
cv2.waitKey(0)
cv2.destroyAllWindows()