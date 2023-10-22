import colour
import colour.plotting
from colour.plotting.diagrams import render
import matplotlib.pyplot as plt
import numpy as np
from ColorCheckerBoard import ColorCheckerBoard_2005


class ColorSpace():

    def __init__(self,Rx, Ry, Gx, Gy, Bx, By, Wx, Wy):
        self.Rx = Rx
        self.Ry = Ry
        self.Gx = Gx
        self.Gy = Gy
        self.Bx = Bx
        self.By = By    
        self.Wx = Wx
        self.Wy = Wy  
        self.RGB2XYZ_matrix = self.Calculation_RGB2XYZ_matrix()
        self.XYZ2RGB_matrix = self.Calculation_XYZ2RGB_matrix()
    def Setting_R(self,Rx,Ry):
        self.Rx = Rx
        self.Ry = Ry
    def Setting_G(self,Gx,Gy):
        self.Gx = Gx
        self.Gy = Gy
    def Setting_B(self,Bx,By):
        self.Bx = Bx
        self.By = By
    def Setting_W(self,Wx,Wy):
        self.Wx = Wx
        self.Wy = Wy
    def Setting_NewColorSpace(self,Rx,Ry,Gx,Gy,Bx,By,Wx,Wy):
        self.Rx = Rx
        self.Ry = Ry
        self.Gx = Gx
        self.Gy = Gy
        self.Bx = Bx
        self.By = By
        self.Wx = Wx
        self.Wy = Wy
        self.RGB2XYZ_matrix = self.Calculation_RGB2XYZ_matrix()
        self.XYZ2RGB_matrix = self.Calculation_XYZ2RGB_matrix()
    def Setting_sRGB(self):
        self.Setting_R(0.64, 0.33)
        self.Setting_G(0.30, 0.60)
        self.Setting_B(0.15, 0.06)
        self.Setting_W(0.31272,0.32903)
        self.RGB2XYZ_matrix = self.Calculation_RGB2XYZ_matrix()
        self.XYZ2RGB_matrix = self.Calculation_XYZ2RGB_matrix()
    def Setting_NTSC_C(self):
        self.Setting_R(0.67, 0.33)
        self.Setting_G(0.21, 0.71)
        self.Setting_B(0.14, 0.08)
        self.Setting_W(0.310, 0.316)
        self.RGB2XYZ_matrix = self.Calculation_RGB2XYZ_matrix()
        self.XYZ2RGB_matrix = self.Calculation_XYZ2RGB_matrix()
    def Setting_P3_D65(self):
        self.Setting_R(0.680, 0.320)
        self.Setting_G(0.265, 0.690)
        self.Setting_B(0.150, 0.060)
        self.Setting_W(0.3127, 0.3290)
        self.RGB2XYZ_matrix = self.Calculation_RGB2XYZ_matrix()
        self.XYZ2RGB_matrix = self.Calculation_XYZ2RGB_matrix()
    def Setting_D50(self):
        self.Setting_W(0.34567,0.35850)
    
    def Calculation_RGB2XYZ_matrix(self, WY=1):
        # // Willy : Major function of colorspace, which denote transformation of signal(R,G,B or grayscale) and physical world (X,Y,Z)
        # // Reference white (RW) is crucial cause it define how (R,G,B) == (1,1,1) looks like,
        # // usually D65 is favorable, but some colorspace used D50 or some other RW.
        # // Use Setting_W (Wx,Wy) to change reference white, argument WY denote luminance, 1 (nits) is convention
        RGB2XYZ_matrix = np.array([[self.Rx,self.Gx,self.Bx],[self.Ry,self.Gy,self.By],
        [1-self.Rx-self.Ry,1-self.Gx-self.Gy,1-self.Bx-self.By]])
        w = 1 / self.Wy
        White_vector = np.array([self.Wx*w*WY, self.Wy*w*WY,(1-self.Wx-self.Wy)*w*WY])
        x = np.linalg.solve(RGB2XYZ_matrix,White_vector)
        for row in range(3) :
            for column in range(3) :
                RGB2XYZ_matrix[column][row] = RGB2XYZ_matrix[column][row]*x[row]
        return RGB2XYZ_matrix
    
    def Calculation_XYZ2RGB_matrix(self, WY=1):
        matrix = np.linalg.inv(self.Calculation_RGB2XYZ_matrix())
        return matrix
    
    def Calculation_RGB2XYZ(self,R,G,B,Gamma = 2.2):
        RGBvector = np.array([[R],[G],[B]])
        vector = (1/(255**Gamma))*RGBvector**Gamma
        matrix = self.Calculation_RGB2XYZ_matrix()
        Result = np.dot(matrix,vector)
        return Result
    

    def Calculation_XYZ2RGB(self,X,Y,Z,Gamma = 2.2):
        # // Willy : default setting is gamma = 2.2,
        # // we first give the grayscale of gamma1.0, by using matrix of XYZ2RGB
        matrix = self.Calculation_XYZ2RGB_matrix()
        scale = 255/1 # // rescale maximum luminance to grayscale 255
        vector = np.array([[X],[Y],[Z]])
        Grayscale_1 = np.dot(matrix,vector) * scale
        Grayscale_2 = ((255**(Gamma-1))*Grayscale_1)**(1/Gamma) 
        return Grayscale_2
    
   
    
    def Calculation_xyY2XYZ (self,x,y,Y):
            w = Y/y
            X = x*w
            Y = y*w
            Z = (1-x-y)*w
            return X,Y,Z
    
    def Calculation_XYZ2LAB(self,X,Y,Z):
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

    def Calculation_LAB2XYZ(self,L,a,b):
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
    
    def Plot_ColorSpace(self,coordinate_x, coordinate_y):
        plt.figure(figsize=[24,24])
        fig, axes = colour.plotting.diagrams.plot_chromaticity_diagram_CIE1931(standalone=False)
        D65 = [0.313,0.329]
        plotcolor = ["Red","Green","Blue"]
        for i in range (len (coordinate_x)):
            axes.plot( coordinate_x[i], coordinate_y[i], 'o-', color='black')   
            # axes.annotate(i+1, (coordinate_x[i], coordinate_y[i])) 
        # srgb = colour.models.RGB_COLOURSPACE_sRGB.primaries
        axes.plot( D65[0], D65[1], 'o-', color='black',label='D65')#
        
        axes.legend(facecolor='C8')
        # fig.savefig('CIE_xy.jpg',dpi=600)
        fig.show()
        plt.show()







