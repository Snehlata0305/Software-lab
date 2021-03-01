from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
from matplotlib import cm
import matplotlib.pyplot as plt
import csv
import os
from mpl_toolkits.axes_grid1 import make_axes_locatable

fig = plt.figure(figsize =(12, 12))
axs = fig.add_subplot(111, projection='3d')

#plt.box(on=None)
#right_side = axs.spines["right"]
#right_side.set_visible(False)

x =[]
y =[]
z =[]

with open('csv_file','r') as csvfile:
    ips = csv.reader(csvfile, delimiter=',')
    for row in ips:
        x.append(float(row[0]))
        y.append(float(row[1]))
        z.append(float(row[2]))

bardtl = axs.scatter(x, y, z, c=z, alpha=0.5, marker='o', cmap=cm.coolwarm)
#axs.view_init(40, 295)

divider = make_axes_locatable(plt.gca())
cax = fig.add_axes([0.94, 0.25, 0.02, 0.5]) 
plt.colorbar(bardtl, shrink=0.5, cax=cax)


axs.set_xlabel('X axis', fontweight='bold')
axs.set_ylabel('Y axis', fontweight='bold')
axs.set_zlabel('Z axis', labelpad=6, fontweight='bold')
axs.w_xaxis.pane.fill = False
axs.w_yaxis.pane.fill = False
axs.w_zaxis.pane.fill = False

axs.grid(None)

fig.savefig('q3plot2.png', bbox_inches='tight')
im1 = Image.open(r'q3plot2.png')
imjpg = im1.convert('RGB')
imjpg.save('q3plot.jpg')

os.remove("q3plot2.png") 
