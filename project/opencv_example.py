import cv2
import numpy as np
import matplotlib.pyplot as plt

def resizing(img, new_width=None, new_height=None, interp=cv2.INTER_LINEAR):
    h, w = img.shape[:2]
    if new_width is None and new_height is None:
        return img
    if new_width is None:
        ratio = new_height / h
        dimension = (int(w * ratio), new_height)
    else:
        ratio = new_width / w
        dimension = (new_width, int(h * ratio))
    return cv2.resize(img, dimension, interpolation=interp)

def cropping(crop_img, x1, y1, x2, y2):
    return crop_img[y1:y2, x1:x2]


img=cv2.imread('image.jpg')
#img1 = resizing(img, 600, 100)
img1 = cropping(img, 20, 20, 300, 1700)
#img1 = img[10:450, 300:750]
cv2.imshow('image2', img1)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('image3.jpg', img1)

#video = cv2.VideoWriter(temp_video_path, cv2.VideoWriter_fourcc(*"mp4v"), 0.001, dim)




# # читать входное изображение
# img = cv2.imread("image.jpg")
# # преобразовать из BGR в RGB, чтобы можно было построить график с помощью matplotlib
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# # отключить оси x и y
# plt.axis('off')
# # показать изображение
# plt.imshow(img)
# plt.show()
# # получаем 200 пикселей от 100 до 300 по оси x и оси y
# # измените это, если хотите, просто убедитесь, что вы не превышаете столбцы и строки
# cropped_img = img[100:100, 300:400]
# # отключить оси x и y
# plt.axis('off')
# # показать получившееся изображение
# plt.imshow(cropped_img)
# plt.show()
# # сохраняем получившееся изображение на диск
# #plt.imsave("chelyabinsk_cropped.jpg", cropped_img)