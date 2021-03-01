##Do it here##
import numpy as np
#import PIL
#from PIL import Image
#import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
im = np.load('decode_this.npy')
#plt.imshow(im)
#img = Image.fromarray(im,'RGB')
#plt.imshow(img)
#image = np.array(img)
#img = mpimg.imread('my.jpeg')
#black_pixels_mask = np.all(image == [0, 0, 0])
c = np.min(im) 
d = np.max(im) 
a = 0
b = 255
nr = float(b - a)
dr = float(d - c)
con = nr / dr
#print(con)
s1 = np.array([ (r - c) for r in im ])
#print(s1)
s2 = s1 * con
s = s2 + a
#print(s)
#plt.gray()
#plt.imshow(s)
#img = Image.fromarray(s,'RGB')
#img.show()
#s[black_pixels_mask]=[255,255,255]
#image_s = Image.fromarray(s,'RGB')
#plt.imshow(s.astype('uint8'))
plt.imsave('result.png',s.astype('uint8'))
#image_s.show()



#img.show()
#img_open = open('my.jpeg','rb')
#img_read = img_open.read()
#img_decode = img_read.decode('latin1')
#print(img_decode().decode('ascii'))'''



