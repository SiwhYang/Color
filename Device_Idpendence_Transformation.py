import colour
import colour.plotting
from colour.plotting.diagrams import render
import matplotlib.pyplot as plt
import numpy as np
from ColorCheckerBoard import ColorCheckerBoard_2005


class Device_Idpendence_Transformation():
    
        def Calculation_xyY2XYZ (self,x,y,Y):
            w = Y/y
            X = x*w
            Y = y*w
            Z = (1-x-y)*w
            return X,Y,Z
        def Calculation_XYZ2LAB_coordinate(self,X,Y,Z):
            # // Reference white is using self.Wx, self.Wy, 1nits Be Careful of the difference of RW
            target_RW_luminance = 100
            w = target_RW_luminance/self.Wy      
            RW_X = self.Wx*w
            RW_Y = self.Wy*w
            RW_Z = (1-self.Wx-self.Wy)*w
            def f ( t ):
                if t > (6/29)**3 :
                    return t **(1/3)
                else :
                    return ((1/3) * (29/6)**2 )*t + 16/116
            L = 116*(f(Y/RW_Y)) -16
            a = 500*(f(X/RW_X)-f(Y/RW_Y))
            b = 200*(f(Y/RW_Y)-f(Z/RW_Z))
            return L, a, b

        def Calculation_LAB2XYZ_coordinate(self,L,a,b):
            # // Reference white is using self.Wx, self.Wy, 1nits Be Careful of the difference of RW
            target_RW_luminance = 100
            w = target_RW_luminance/self.Wy      
            RW_X = self.Wx*w
            RW_Y = self.Wy*w
            RW_Z = (1-self.Wx-self.Wy)*w
            X = RW_X* ((L+16)/116 + (a/500))**3
            Y = RW_Y* ((L+16)/116 )**3
            Z = RW_Z* ((L+16)/116 - (b/200))**3
            return X, Y, Z