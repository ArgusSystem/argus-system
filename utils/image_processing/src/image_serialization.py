import numpy as np
import cv2


def bytearray_to_image(np_arr, color=cv2.IMREAD_COLOR):
    return cv2.imdecode(np_arr, color)


def image_to_bytearray(image, extension='.jpg'):
    ret_val, np_arr = cv2.imencode(extension, image)
    return np_arr


def bytestring_to_image(buffer, color=cv2.IMREAD_COLOR):
    np_arr = np.fromstring(buffer, np.uint8)
    return bytearray_to_image(np_arr, color)


def image_to_bytestring(image, extension='.jpg'):
    return image_to_bytearray(image, extension).tostring()


def image_to_RGB(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def save_image(filepath, image):
    cv2.imwrite(filepath, image)


def image_debug(name, image, wait_time=1, color_convert=None):
    final_image = image if color_convert is None else cv2.cvtColor(image, color_convert)
    cv2.imshow(name, final_image)
    cv2.waitKey(1)


def draw_boxes(im, boxes, color=(0, 0, 255)):
    x1 = [i[0] for i in boxes]
    y1 = [i[1] for i in boxes]
    x2 = [i[2] for i in boxes]
    y2 = [i[3] for i in boxes]
    for i in range(len(boxes)):
        cv2.rectangle(im, (int(x1[i]), int(y1[i])), (int(x2[i]), int(y2[i])), color, 1)
    return im
