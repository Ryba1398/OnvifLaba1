from camera import Camera

miemCam = Camera('192.168.15.42', 80, 'rubs1998', 'XotV7G3YiCpc') # Camera class object


if miemCam.checkAbsoluteMove(): # if camera provides Absolute Move function
    miemCam.moveAbsolute(-1, -1, 0.5) # we will move it




