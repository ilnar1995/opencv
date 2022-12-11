import numpy as np
import cv2 as cv2
import time


#
def zoom_frames(src, dim, zoom):  # получить картинку для отдаленного разрешения
    dim_max = (int(dim[0] * zoom), int(dim[1] * zoom))  # нужно ввести данные для отдаленного разрешения
    width = dim_max[0]
    height = dim_max[1]
    if src.shape[1] < dim_max[0]:
        width = dim_max[0]
    height = int(src.shape[0] * dim_max[0] / src.shape[1])
    dsize = (width, height)
    output = cv2.resize(src, dsize)

    if output.shape[0] < dim_max[1]:
        height = dim_max[1]
        width = int(output.shape[1] * dim_max[1] / output.shape[0])
        dsize = (width, height)
        output = cv2.resize(src, dsize)
    return output


def zoom_in_zoom_out(frame, effectName, dim, frame_time, fps, i, zoom):
    centre_width = frame.shape[1] / 2
    centre_height = frame.shape[0] / 2
    withdif = centre_width - (dim[0] / 2)
    heightdif = centre_height - (dim[1] / 2)
    k = i / frame_time * 1000 / fps
    if frame.shape[1] / dim[0] > frame.shape[0] / dim[1]:
        a = k * heightdif * dim[0] / dim[1]
        b = k * heightdif
    else:
        a = k * withdif
        b = k * withdif * dim[1] / dim[0]
    if effectName == "zoomIn":
        c = 1
    elif effectName == "zoomOut":
        c = -1
        zoom = 1
    x1 = int(centre_width - (zoom * dim[0] / 2) + a * c)
    x2 = int(centre_width + (zoom * dim[0] / 2) - a * c)
    y1 = int(centre_height - (zoom * dim[1] / 2) + b * c)
    y2 = int(centre_height + (zoom * dim[1] / 2) - b * c)
    # print("(x1", x1, "y1", y1, ")(x2", x2, "y2", y2, "                    k", k)
    return cv2.resize(frame[y1:y2, x1:x2], dim, interpolation=cv2.INTER_LINEAR)


def move_zoom_frame(frame, effectName, dim, frame_time, fps, i, zoom):
    k = i / frame_time * 1000 / fps
    withdif = frame.shape[1] - dim[0]
    heightdif = frame.shape[0] - dim[1]
    if effectName == "moveTop" or effectName == "moveBottom":
        a = k * heightdif
        centre_width = frame.shape[1] / 2
        b = dim[0] / 2
        x1 = int(centre_width - b)
        x2 = int(centre_width + b)
        if effectName == "moveTop":
            y1 = int(heightdif - a)
            y2 = int(frame.shape[0] - a)
        else:
            y1 = int(a)
            y2 = int(frame.shape[0] - heightdif + a)
    if effectName == "moveLeft" or effectName == "moveRight":
        a = k * withdif
        centre_height = frame.shape[0] / 2
        b = dim[1] / 2
        y1 = int(centre_height - b)
        y2 = int(centre_height + b)
        if effectName == "moveLeft":
            x1 = int(withdif - a)
            x2 = int(frame.shape[1] - a)
        else:
            x1 = int(a)
            x2 = int(frame.shape[1] - withdif + a)
    # print("(x1", x1, "y1", y1, ")(x2", x2, "y2", y2, "                    k", k)
    return cv2.resize(frame[y1:y2, x1:x2], dim, interpolation=cv2.INTER_LINEAR)

def zoom_without_effects(frame, dim, frame_time, fps, i, zoom):
    centre_width = frame.shape[1] / 2
    centre_height = frame.shape[0] / 2
    withdif = centre_width - (dim[0] / 2)
    heightdif = centre_height - (dim[1] / 2)
    if frame.shape[1] / dim[0] > frame.shape[0] / dim[1]:
        a = heightdif * dim[0] / dim[1]
        b = heightdif
    else:
        a = withdif
        b = withdif * dim[1] / dim[0]
    c = 1
    x1 = int(centre_width - (zoom * dim[0] / 2) + a * c)
    x2 = int(centre_width + (zoom * dim[0] / 2) - a * c)
    y1 = int(centre_height - (zoom * dim[1] / 2) + b * c)
    y2 = int(centre_height + (zoom * dim[1] / 2) - b * c)
    # print("(x1", x1, "y1", y1, ")(x2", x2, "y2", y2, "                    k", k)
    return cv2.resize(frame[y1:y2, x1:x2], dim, interpolation=cv2.INTER_LINEAR)


# Define the codec and create VideoWriter object
fps = 30
dim = (1366, 768)
k1 = {'10%': 1.20, '20%': 1.2, '30%': 1.30, '40%': 1.4, '50%': 1.5, '60%': 1.6, '70%': 1.7, '80%': 1.8, '90%': 1.9, '100%': 2.0}
zoom = k1.get('50%', 1)
frame_time = 3000#3000
effectName = "zoomIn"       # zoomIn        zoomOut     moveTop  moveLeft  moveRight  moveBottom
if not zoom:
    zoom = 1
if not frame_time:
    frame_time = 1000
out = cv2.VideoWriter('output1.avi', cv2.VideoWriter_fourcc(*"mp4v"), fps, dim)

quantity_frame: int = int(fps * frame_time // 1000)
frame = cv2.imread('Stones.jpg')
frame = zoom_frames(frame, dim, zoom)  # k1.get('5x'))
print("количество кадров", quantity_frame)
start_time = time.time()
# resized = cv2.resize(frame, dim, interpolation=cv2.INTER_LINEAR)
if effectName == "zoomIn" or effectName == "zoomOut":
    for i in range(quantity_frame):
        resized = zoom_in_zoom_out(frame, effectName, dim, frame_time, fps, i,
                                   zoom)  # обрезка кадра для i-го изображения
        out.write(resized)
elif effectName == "moveTop" or effectName == "moveLeft" or effectName == "moveRight":
    for i in range(quantity_frame):
        resized = move_zoom_frame(frame, effectName, dim, frame_time, fps, i,
                                  zoom)  # обрезка кадра для i-го изображения
        out.write(resized)
else:
    for i in range(quantity_frame):
        resized = zoom_without_effects(frame, dim, frame_time, fps, i,
                                   zoom)  # обрезка кадра для i-го изображения
        out.write(resized)

print("--- %s seconds ---" % (time.time() - start_time))
# Release everything if job is finished
out.release()
# cv.destroyAllWindows()
