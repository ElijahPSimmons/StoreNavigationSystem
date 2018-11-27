import pixy 
import time
from ctypes import *
from pixy import *

# Pixy2 Python SWIG get blocks example #

#print ("Pixy2 Python SWIG Example -- Get Blocks")
def ColorSensor():
	pixy.init ()
	pixy.change_prog ("color_connected_components");

	class Blocks (Structure):
	  _fields_ = [ ("m_signature", c_uint),
		("m_x", c_uint),
		("m_y", c_uint),
		("m_width", c_uint),
		("m_height", c_uint),
		("m_angle", c_uint),
		("m_index", c_uint),
		("m_age", c_uint) ]

	blocks = BlockArray(100)
	frame = 0
	i = 0
	check = [0,0,0,0,0,0,0,0,0,0]
	ret = check
	while i<20:
            count = pixy.ccc_get_blocks (100, blocks)

            if count > 0:
		#print 'frame %3d:' % (frame)
                frame = frame + 1
                for index in range (0, count):
                    check[blocks[index].m_signature-1] +=1
                    #print blocks[index].m_signature
		  #print '[BLOCK: SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (blocks[index].m_signature, blocks[index].m_x, blocks[index].m_y, blocks[index].m_width, blocks[index].m_height)
                for j in range(0,count):
                    if(check[j]-1 == 1 or check[j] == 2 or check[j] == 3):
                        ret[check[j]-1]+=1
                print check
                #print ret
                i+=1
                time.sleep(.5)
	return ret

#ColorSensor()