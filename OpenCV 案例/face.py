from openni import openni2
import numpy as np
import cv2


def mousecallback(event,x,y,flags,param):
     if event==cv2.EVENT_LBUTTONDBLCLK:
         print(y, x, dpt[y,x])


if __name__ == "__main__": 

    openni2.initialize()

    dev = openni2.Device.open_any()
    print(dev.get_device_info())

    depth_stream = dev.create_depth_stream()
    depth_stream.start()

    color_stream = dev.create_color_stream()
    color_stream.start()

    #cap = cv2.VideoCapture(0)
    cv2.namedWindow('depth')
    cv2.setMouseCallback('depth',mousecallback)

    cv2.namedWindow('color')
    cv2.setMouseCallback('color',mousecallback)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    while True:

        frame = depth_stream.read_frame()
        dframe_data = np.array(frame.get_buffer_as_triplet()).reshape([480, 640, 2])
        dpt1 = np.asarray(dframe_data[:, :, 0], dtype='float32')
        dpt2 = np.asarray(dframe_data[:, :, 1], dtype='float32')
        
        dpt2 *= 255
        dpt = dpt1 + dpt2
        
        cv2.imshow('depth', dpt)

        cframe = color_stream.read_frame()
        cframe_data = np.array(cframe.get_buffer_as_triplet()).reshape([480, 640, 3])
        R = cframe_data[:, :, 0]
        G = cframe_data[:, :, 1]
        B = cframe_data[:, :, 2]
        cframe_data = np.transpose(np.array([B, G, R]), [1, 2, 0])
        cframe_data = cframe_data.copy()
        faces = face_cascade.detectMultiScale(cframe_data, 1.3, 5)
        for (x, y, w, h) in faces:
            cframe_data = cv2.rectangle(cframe_data, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
        cv2.imshow('color', cframe_data)

        key = cv2.waitKey(1)
        if int(key) == ord('q'):
            break

    depth_stream.stop()
    color_stream.stop()
    dev.close()

