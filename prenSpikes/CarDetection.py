from cv2 import *

i = imread('../resources/parking-car.png')

imshow("MyWindow", i)
waitKey(0)
destroyAllWindows()