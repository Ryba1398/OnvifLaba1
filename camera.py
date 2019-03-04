from onvif import ONVIFCamera
from time import sleep
import zeep


def zeepPythonvalue(self, xmlvalue):
    return xmlvalue


zeep.xsd.simple.AnySimpleType.pythonvalue = zeepPythonvalue


class Camera:

    def __init__(self, ip, port, login, password): # class initializer
        self.miemCam = ONVIFCamera(
            ip,         # camera ip
            port,       # camera port
            login,      # my login for authorization
            password    # my password for authorization
        )

        self.token = self.miemCam.create_media_service().GetProfiles()[0].token # get token to use specific functions

        self.ptz = self.miemCam.create_ptz_service() # create service which help to perform movements

        self.requestAbsoluteMove = self.ptz.create_type('AbsoluteMove') # make request for absolute move
        self.requestAbsoluteMove.ProfileToken = self.token  # pass token for absolute move

        self.requestStop = self.ptz.create_type('Stop') # make request for stop
        self.requestStop.ProfileToken = self.token  # pass token for stop

        self.stop() # stop previous movements

    def stop(self): # function to stop camera
        self.requestStop.PanTilt = True
        self.requestStop.Zoom = True
        self.ptz.Stop(self.requestStop)

    def checkAbsoluteMove(self):  # function to check, is current camera provides absolute move

        pos = self.ptz.GetStatus({"ProfileToken": self.token}).Position # position value
        x = pos.PanTilt.x   # x coordinate
        y = pos.PanTilt.y   # y coordinate

        initialCoordinate = x   # x coordinate before check

        step = 0.1 # variable to check camera on move

        if x + step <= 1:   # if it is not out of range
            x1 = x + step   # plus step
        else:
            x1 = x - step   # or subtract step

        self.ptz.AbsoluteMove({"ProfileToken": self.token, "Position": {"PanTilt": {"x": x1, "y": y}}})  # try perform movement
        sleep(3)    # wait until it ends
        pos = self.ptz.GetStatus({"ProfileToken": self.token}).Position # take current position
        newCoordinate = pos.PanTilt.x # take current x position

        if initialCoordinate != newCoordinate:  # if current x position not equal initial
            print('Absolute Move поддерживается')   # it means that camera can move
            print('Координаты камеры: X = ' + str(pos.PanTilt.x) + ', Y = ' + str(pos.PanTilt.y))   # output coordinates
                                                                                                    # to be sure that we can get them
            return True     # if camera can move - return true, then we will use it

        else:   # if x coordinate is the same
            print( 'Absolute Move не поддерживается' )  # it means that camera can't move
            return False        # so return false

    def performAbsoluteMove(self):  # tech function that will perform movement
        self.ptz.AbsoluteMove(self.requestAbsoluteMove)
        sleep(4)    # wait until camera ends move

    def moveAbsolute(self, x, y, zoom): # function to move camera and change zoom
        print('Направить в точку (' + str(x) + '; ' + str(y) + ') с зумом  ' + str(zoom)) # output target coordinates and zoom

        status = self.ptz.GetStatus({'ProfileToken': self.token})   # get status to performe movement
        status.Position.PanTilt.x = x   # set x coordinate
        status.Position.PanTilt.y = y   # set y coordinate
        status.Position.Zoom.x = zoom   # set zoom value

        self.requestAbsoluteMove.Position = status.Position # make request for move
        self.performAbsoluteMove()  # make move !!!
