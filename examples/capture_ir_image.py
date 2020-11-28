"""
Simple IR camera using freenect2. Saves captured IR image
to output.jpg.

"""
# Import parts of freenect2 we're going to use
import sys
import cv2
import numpy as np
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel


try:
    from pylibfreenect2 import OpenGLPacketPipeline
    pipeline = OpenGLPacketPipeline()
except:  # NOQA
    try:
        from pylibfreenect2 import OpenCLPacketPipeline
        pipeline = OpenCLPacketPipeline()
    except:  # NOQA
        from pylibfreenect2 import CpuPacketPipeline
        pipeline = CpuPacketPipeline()
print("Packet pipeline:", type(pipeline).__name__)


# Open default device
fn = Freenect2()
num_devices = fn.enumerateDevices()
if num_devices == 0:
    print("No device connected!")
    sys.exit(1)

# Create and set logger
logger = createConsoleLogger(LoggerLevel.Debug)
setGlobalLogger(logger)

serial = fn.getDeviceSerialNumber(0)
device = fn.openDevice(serial, pipeline=pipeline)

listener = SyncMultiFrameListener(FrameType.Ir)

# Register listener
device.setIrAndDepthFrameListener(listener)

device.start()

while True:
    frames = listener.waitForNewFrame()
    frame = frames["ir"]
    
    cv2.imshow("ir", frame.asarray() / 65535.)

    key = cv2.waitKey(delay=1)
    if key == ord('q'):
        listener.release(frames)
        break
    if key == ord('s'):
        output = (frame.asarray() / 65535. * 255).astype(np.uint8)  
        cv2.imwrite("output.bmp", output)
        cv2.imwrite("output.jpg", output)
    listener.release(frames)
    

device.stop()
device.close()

sys.exit(0)