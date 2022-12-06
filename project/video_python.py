import numpy as np
import cv2 as cv2
import time

#
def zoom_frames(src, dim, k=1):  # получить картинку для отдаленного разрешения
    dim_max = (int(dim[0] * k), int(dim[1] * k))  # нужно ввести данные для отдаленного разрешения
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


# def zoom_in_zoom_out(frame, zoom, effectName, dim, frame_time, fps, i):
#     centre_width = frame.shape[1] / 2
#     centre_height = frame.shape[0] / 2
#     withdif = centre_width - (dim[0] / 2)
#     heightdif = centre_height - (dim[1] / 2)
#     k = i / frame_time * 1000 / 24
#     x1 = int(centre_width - (zoom * dim[0] / 2) + k*withdif)
#     x2 = int(centre_width + (zoom * dim[0] / 2) - k*withdif)
#     y1 = int(centre_height - (zoom * dim[1] / 2) + k*withdif*dim[1]/dim[0])
#     y2 = int(centre_height + (zoom * dim[1] / 2) - k*withdif*dim[1]/dim[0])
#     print("(x1", x1, "y1", y1, ")(x2", x2, "y2", y2, "                    k", k)
#     return {"y1": y1, "y2": y2, "x1": x1, "x2": x2}


def zoom_in_zoom_out(frame, zoom, effectName, dim, frame_time, fps, i):
    centre_width = frame.shape[1] / 2
    centre_height = frame.shape[0] / 2
    withdif = centre_width - (dim[0] / 2)
    heightdif = centre_height - (dim[1] / 2)
    k = i / frame_time * 1000 / 24
    if frame.shape[1] / dim[0] <= frame.shape[0] / dim[1]:
        a = k*withdif
        b = k*withdif*dim[1]/dim[0]
    else:
        a = k * heightdif * dim[0] / dim[1]
        b = k * heightdif
    x1 = int(centre_width - (zoom * dim[0] / 2) + a)
    x2 = int(centre_width + (zoom * dim[0] / 2) - a)
    y1 = int(centre_height - (zoom * dim[1] / 2) + b)
    y2 = int(centre_height + (zoom * dim[1] / 2) - b)
    #print("(x1", x1, "y1", y1, ")(x2", x2, "y2", y2, "                    k", k)
    return {"y1": y1, "y2": y2, "x1": x1, "x2": x2}


# Define the codec and create VideoWriter object
fps = 24
dim = (1366, 720)
k1 = {'1x': 1.20, '2x': 1.25, '3x': 1.30, '4x': 1.35, '5x': 1.40, '6x': 1.45, '7x': 1.50}
frame_time = 120000
effectName = "zoomIn"
# effectName = (
#     ("zoomIn", "zoomIn"),
#     ("zoomOut", "zoomOut"),
#     ("moveTop", " moveTop"),
#     ("moveLeft", " moveLeft"),
#     ("moveRight", "moveRight"),
#     ("moveBottom", "moveBottom"))
# fourcc = cv.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter('output1.avi', cv2.VideoWriter_fourcc(*"mp4v"), fps, dim)

quantity_frame: int = int(fps * frame_time // 1000)
frame = cv2.imread('image.jpg')
frame = zoom_frames(frame, dim, k1.get('7x'))  # k1.get('5x'))
print("количество кадров", quantity_frame)
start_time = time.time()
# resized = cv2.resize(frame, dim, interpolation=cv2.INTER_LINEAR)
if effectName == "zoomIn" or effectName == "zoomOut":
    pass
    for i in range(quantity_frame):
        coordinates = zoom_in_zoom_out(frame, k1.get('7x'), effectName, dim, frame_time, fps, i)
        frame1_resized = frame[coordinates.get("y1"):coordinates.get("y2"), coordinates.get("x1"):coordinates.get("x2")]
        resized = cv2.resize(frame1_resized, dim, interpolation=cv2.INTER_LINEAR)
        out.write(resized)
elif effectName == "moveTop" or effectName == "moveLeft" or effectName == "moveRight" or effectName == "moveBottom":
    pass
else:
    pass

print("--- %s seconds ---" % (time.time() - start_time))
# Release everything if job is finished
out.release()
# cv.destroyAllWindows()


# import numpy as np
# import cv2 as cv
# cap = cv.VideoCapture(0)
# # Define the codec and create VideoWriter object
# fourcc = cv.VideoWriter_fourcc(*'XVID')
# out = cv.VideoWriter('output.avi', fourcc, 20.0, (640,  480))
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break
#     frame = cv.flip(frame, 0)
#     # write the flipped frame
#     out.write(frame)
#     cv.imshow('frame', frame)
#     if cv.waitKey(1) == ord('q'):
#         break
# # Release everything if job is finished
# cap.release()
# out.release()
# cv.destroyAllWindows()


import numpy as np
import cv2 as cv

# Define the codec and create VideoWriter object
fps = 24
dim = (200, 200)
# fourcc = cv.VideoWriter_fourcc(*"mp4v")
out = cv.VideoWriter('output.avi', cv.VideoWriter_fourcc(*"mp4v"), fps, dim)

duration = 20
i = duration * fps
seconds_left = 0
frame = cv.imread('image1.jpg')
while seconds_left < i:
    # write the flipped frame
    out.write(frame)
    seconds_left += 1
# Release everything if job is finished
out.release()
# cv.destroyAllWindows()
