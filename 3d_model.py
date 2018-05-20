# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2018 sarah-murray

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.





Plot surfaces in 3D and slice in the X, Y, and Z axes.

Import .csv data defining the elevation of surfaces. Take in 3 
surfaces. Create slider bar to set upper and lower X, Y, and Z limits to
slice the data along these axes. Set NaN to any data outside of these 
limits.

Args:
	central (.txt) -- Contains Z values for the middle surface to be 
		plotted. Will be used to define X and Y extents of model.
	lower(.txt) -- Contains Z values for the lower-most surface to be 
		plotted.
	upper(.txt) -- Contains Z values for the upper-most surface to be 
		plotted.
"""


import matplotlib.pyplot as plt
#Will be identified as not needed...but it is
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from model_functions import Cross_section
from matplotlib.widgets import Slider, Button


#Set directory of input layers
central = "surfaces/in.txt"
lower = "surfaces/in_lower.txt"
upper = "surfaces/in_upper.txt"


#Create space for model
fig = plt.figure()
ax = fig.gca(projection='3d')
#Allow space for slider bars
plt.subplots_adjust(bottom=0.4)

#Connect to functions
model = Cross_section(ax)

#access data files + create 2d lists
data_in = []
data_high = []
data_low = []
model.create_data(central, data_in)
model.create_data(lower, data_high)
model.create_data(upper, data_low)

#Define x and y extents and find range of z
x_extents = [] # 2d grid to define x axis
y_extents = [] #2d grid to define y axis
x_range = []    #All x, y, z
y_range = []    #values to allow
z_range = []    #finding the max and min
#Use data_in dimensions to define x and y extents
model.set_extents(data_in, x_extents, y_extents)
#Find full range of data
full_range = data_in + data_low + data_high
model.define_limits(x_extents, x_range)
model.define_limits(y_extents, y_range)
model.define_limits(full_range, z_range)
#Find min and max coordinate values
min_z = min(z_range)
max_z = max(z_range)
min_x = min(x_range)
max_x = max(x_range)
min_y = min(y_range)
max_y = max(y_range)

#Takes all limitations on x, y, z and builds surface
def build_surface(surface, low_x, high_x, low_y, high_y, low_z, high_z, x, y):
    """
    Slice data along X, Y, and Z and create surfaces.
	
    Slice data along X, Y, and Z where defined and create 3D surfaces.
    Set axes to maximum X, Y, and Z ranges and normalise colour bar 
    across all data.
	
    Args:
        surface (list) -- 2D list containing Z values for each cell.
        low_x (float) -- Define lowest coordinate where data is sliced 
            along the X axis.
        high_x (float) -- Define highest coordinate where data is sliced
            along the X axis.
        low_y (float) -- Define lowest coordinate where data is sliced 
            along the Y axis.
        high_y (float) -- Define highest coordinate where data is sliced
            along the Y axis.
        low_z (float) -- Define lowest coordinate where data is sliced 
            along the Z axis.
        high_z (float) -- Define highest coordinate where data is sliced
            along the Z axis.
        x (list) -- 2D list containing X values for each cell.
        y (list) -- 2D list containing Y values for each cell.
	
    Returns:
        new_surf -- New surface plotted within the model.
    """
    new_surface = []
    new_x = []
    new_y = []
    #Slice x, y, z
    model.limit_surface(surface, new_surface, high_z, low_z)
    model.limit_surface(x, new_x, high_x, low_x)
    model.limit_surface(y, new_y, high_y, low_y)
    
    #Plot new surface
    global new_surf 
    new_surf = ax.plot_surface(new_x, new_y, new_surface, cmap=cm.terrain)
    #Limit axes to max extents, excluding np.nan
    model.set_axes(x_range, y_range, z_range)
    #Define normalisation for colour ramp
    normal = new_surf.norm
    normal.vmax = max(z_range)
    normal.vmin = min(z_range)

#Plot initial surfaces
build_surface(data_high, min_x, max_x, min_y, max_y, min_z, max_z, x_extents, y_extents)    
build_surface(data_in, min_x, max_x, min_y, max_y, min_z, max_z, x_extents, y_extents)
build_surface(data_low, min_x, max_x, min_y, max_y, min_z, max_z, x_extents, y_extents)

#Insert colour bar
fig.colorbar(new_surf, shrink=0.5, aspect=5)

#Set up slider positioning and colours
axcolour = '#FFFFFF'
ax_z_low = plt.axes([0.2, 0.06, 0.6, 0.02], facecolor=axcolour)
ax_z_high = plt.axes([0.2, 0.11, 0.6, 0.02], facecolor=axcolour)
ax_x_low = plt.axes([0.2, 0.16, 0.6, 0.02], facecolor=axcolour)
ax_x_high = plt.axes([0.2, 0.21, 0.6, 0.02], facecolor=axcolour)
ax_y_low = plt.axes([0.2, 0.26, 0.6, 0.02], facecolor=axcolour)
ax_y_high = plt.axes([0.2, 0.31, 0.6, 0.02], facecolor=axcolour)
#Insert sliders
slide_z_low = Slider(ax_z_low, 'Lower Z Limit', min_z, max_z, valinit=min_z)
slide_z_high = Slider(ax_z_high, 'Upper Z Limit', min_z, max_z, valinit=max_z)
slide_x_low = Slider(ax_x_low, 'Lower X Limit', min_x, max_x, valinit=min_x)
slide_x_high = Slider(ax_x_high, 'Upper X Limit', min_x, max_x, valinit=max_x)
slide_y_low = Slider(ax_y_low, 'Lower Y Limit', min_y, max_y, valinit=min_y)
slide_y_high = Slider(ax_y_high, 'Upper Y Limit', min_y, max_y, valinit=max_y)

#Set up reset button
button_ax = plt.axes([0.05, 0.01, 0.1, 0.04])
button = Button(button_ax, 'Reset', color=axcolour)

def update(val):
    """
    Update surfaces to slice data along coordinates specified by user.
    
    Takes in upper and lower X, Y, and Z limits specified by user to
    update the displayed surfaces.
    
    Args:
        val (float) -- Value from slider bar.
    
    Returns:
        zlow_val (float) -- Lower value to slice data along the Z axis.
        zhigh_val (float) -- Upper value to slice data along the Z axis.
        xlow_val (float) -- Lower value to slice data along the X axis.
        xhigh_val (float) -- Upper value to slice data along the X axis.
        ylow_val (float) -- Lower value to slice data along the Y axis.
        yhigh_val (float) -- Upper value to slice data along the Y axis.
    """
    #Clear previous surfaces
    ax.clear()
    #Get value from slider
    zlow_val = slide_z_low.val
    zhigh_val = slide_z_high.val
    xlow_val = slide_x_low.val
    xhigh_val = slide_x_high.val
    ylow_val = slide_y_low.val
    yhigh_val = slide_y_high.val
    #Plot new surfaces
    build_surface(data_high, xlow_val, xhigh_val, ylow_val, yhigh_val, zlow_val, zhigh_val, x_extents, y_extents)
    build_surface(data_in, xlow_val, xhigh_val, ylow_val, yhigh_val, zlow_val, zhigh_val, x_extents, y_extents)
    build_surface(data_low, xlow_val, xhigh_val, ylow_val, yhigh_val, zlow_val, zhigh_val, x_extents, y_extents)


def reset():
    """
    Reset slider bars and surfaces to original setup.
    	
    Requires no setup.
    """
    slide_z_low.reset()
    slide_z_high.reset()
    slide_x_low.reset()
    slide_x_high.reset()
    slide_y_low.reset()
    slide_y_high.reset()

#When sliders change, call upddate()
slide_z_low.on_changed(update)
slide_z_high.on_changed(update)
slide_x_low.on_changed(update)
slide_x_high.on_changed(update)
slide_y_low.on_changed(update)
slide_y_high.on_changed(update)
#When button clicked, call reset()
button.on_clicked(reset)