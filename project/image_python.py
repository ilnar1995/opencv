import cv2
import time
def zoom_frames(src, dim, k):                   #получить картинку для отдаленного разрешения
    dim_max = (int(dim[0]*k), int(dim[1]*k)) #нужно ввести данные для отдаленного разрешения
    width = dim_max[0]
    height = dim_max[1]
    if src.shape[1]<dim_max[0]:
        width = dim_max[0]
    height = int(src.shape[0]*dim_max[0] / src.shape[1])
    dsize = (width, height)
    output = cv2.resize(src, dsize)

    if output.shape[0]<dim_max[1]:
        height = dim_max[1]
        width = int(output.shape[1]*dim_max[1]/output.shape[0])
        dsize = (width, height)
        output = cv2.resize(src, dsize)
    return output

fps = 24
dim = (1366, 720)
k1= {'1x':1.20, '2x':1.25, '3x':1.30, '4x':1.35, '5x':1.40, '6x':1.45, '7x':1.50}
k=1.15     #коэффицэнт зума
img = cv2.imread('image.jpg', cv2.IMREAD_UNCHANGED)

x1 = 10
x2 = 600
y1 = 10
y2 = 600
start_time = time.time()

output1 = zoom_frames(img, dim, k1.get('1x'))
crop_img = output1[y1:y2, x1:x2]
print("--- %s seconds ---" % (time.time() - start_time))

cv2.imwrite('image4.jpg', output1)


# #
# import cv2
# fps = 24
# dim = (807, 600)
# src = cv2.imread('image.jpg', cv2.IMREAD_UNCHANGED)
# width = dim[0]
# height = dim[1]
# if src.shape[1]<dim[0]:
#     width = dim[0]
#     height = int(src.shape[0]*dim[0] / src.shape[1])
#     print('меншье 800', width, height)
# else:
#     height = int(src.shape[0] * dim[0] / src.shape[1])
#     pass
#     print('больше 800       ', width, height)#, output.shape[1], output.shape[0])
# dsize = (width, height)
# output = cv2.resize(src, dsize)
#
# if output.shape[0]<dim[1]:
#     height = dim[1]
#     width = int(output.shape[1]*dim[1] / output.shape[0])
#     dsize = (width, height)
#     output = cv2.resize(src, dsize)
#     print('меншье 600       ', width, height)
# cv2.imwrite('resize_image.jpg', output)
#
#

# # percent by which the image is resized
# scale_percent = 200
#
# # calculate the 50 percent of original dimensions
# width = int(src.shape[1] * scale_percent / 100)
# height = int(src.shape[0] * scale_percent / 100)
#
# # dsize
# dsize = (width, height)
#
# # resize image
# output = cv2.resize(src, dsize)
