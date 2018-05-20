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
"""


import numpy as np
import csv

class Cross_section():
    """
    Provide methods to build and slice 3D surfaces.
    
    Build 3D surfaces within a matplotlib figure. Take in user-specified
    X, Y, and Z coordinates and slice the data along upper and lower 
    limits.	Assign NaN to any data outside of these limits.
    """

    def __init__(self,ax):
        """
        Define the model.
        
        Args:
            ax -- Matplotlib object, 
                matplotlib.pyplot.figure().gca(projection='3d')
        """
        self.ax = ax
        
    def create_data(self, directory, data_list):
        """
        Converts .csv data into a 2D list of values.
        
        Args:
            directory (str) -- .csv filename.
            data_list (list) -- Empty list to contain data.
        
        Returns:
            data_list (list) -- 2D list containing values from .csv.
        """
        f = open(directory, newline="")
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            rowlist = []
            for value in row:
                rowlist.append(float(value))
            data_list.append(rowlist)
        f.close()
    
    def set_extents(self, raw_data, x_data, y_data):
        """
        Create 2D lists to define the X and Y extents.
        
        Create 2D lists to correspond with the input data to define the
        X and Y coordinate for each cell.
        
        Args:
            raw_data (list) -- input data of Z values.
            x_data (list) -- Empty list.
            y_data (list) -- Empty list.
        
        Returns:
            x_data (list) -- 2D list of X values.
            y_data (list) -- 2D list of Y values.
        """
        ypoint = 1
        while ypoint <= len(raw_data[0]):
            ypoints = 1
            ylist = []
            while ypoints <= len(raw_data[0]):
                ylist.append(ypoint)
                ypoints += 1
            y_data.append(ylist)
            ypoint += 1
        
        xpoint = 1
        xlist = []
        while xpoint <= len(raw_data):
            xlist.append(xpoint)
            xpoint += 1
        xpoints = 1
        while xpoints <= len(raw_data):
            x_data.append(xlist)
            xpoints += 1

    def limit_surface(self, surface, new_surface, upper_limit, lower_limit):
        """
        Set 2D list value to NaN where outside of specified values.
        
        Args:
            surface (list) -- 2D list.
            new_surface (list) -- Empty 2D list.
            upper_limit (float) -- Maximum value to keep within data.
            lower_limit (float) -- Minimum value to keep within data.
        
        Returns:
            new_surface (list) -- 2D list of the same dimensions as 
            input data. Replace values not between lower_limit and 
            upper_limit with "nan".
        """
        #recreate surfaces replaces limited values with nan
        for i in surface:
            list = []
            for j in i:
                if j >= upper_limit:
                    j = np.nan
                if j <= lower_limit:
                    j = np.nan
                list.append(j)
            new_surface.append(list)

    def set_axes(self, x, y, z):
        """
        Set axes to the minimum and maximum X, Y, and Z values.
        
        Prevent axes from changing with the maximum and minimum of
        displayed data.
        
        Args:
            x (list) -- 1D list of X coordinates.
            y (list) -- 1D list of Y coordinates.
            z (list) -- 1D list of Z coordinates.
        """
        self.ax.set_xlim(min(x), max(x))
        self.ax.set_ylim(min(y), max(y))
        self.ax.set_zlim(min(z), max(z))

    def define_limits(self, data, limits):
        """
        Convert a 2D list to a 1D list.
        
        Args:
            data (list) -- 2D list.
            limits (list) -- Empty list.
        
        Returns:
            limits (list) -- 1D list containing all values from data.
        """
        for i in data:
            for j in i:
                limits.append(j)