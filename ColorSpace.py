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
    
    def Calculation_XYZ2RGB(self,X,Y,Z):
        # // Willy : default setting is gamma = 2.2
        matrix = self.Calculation_XYZ2RGB_matrix()
        a = 100/((255)**2.2)
        scale = 255/100 # // rescale maximum luminance to grayscale 255
        vector = np.array([[X],[Y],[Z]])
        result = np.dot(matrix,vector) * scale
        return ((255**(1.2))*result)**(1/2.2)
    

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



class Color_Application():
    def __init__(self):
        self.CS = self.colorspace
        self.Trans = self.transformation

    def Calculation_RYGYBY(self,WY):
        # // Willy : We get WY = RY*R + GY*G + BY*B from matrix expansion, where (R,G,B) = (1,1,1) denote white,
        # // RY, GY, BY could simply denote the luminance contriburtion of primary to white  
        # // Example : NTSC return RY = 0.2989, GY = 0.5864, BY = 0.1146
        # // this is how Gray = 0.299 * Red + 0.587 * Green + 0.114 * Blue coming from
        matrix = self.Calculation_RGB2XYZ_matrix(WY)
        RY = matrix[1][0]
        GY = matrix[1][1]
        BY = matrix[1][2]
        return RY, GY, BY

 

    def Calculation_RGB2newcolor_ratio(self,x,y):
        # // Willy : WY is arbitrary since we would do normalize,
        # // If normalize is canceled, the vector should be careful for its length (reference to Calculation_RGB2XYZ_matrix )
        matrix = self.Calculation_RGB2XYZ_matrix(1)
        vector = np.array([x,y,(1-x-y)])
        x = np.linalg.solve(matrix,vector)
        # // Normalize
        c = x[0]+x[1]+x[2]
        ratio = x/c
        return ratio

   

    # // transformation module of color space (device independence)
    

 
    def Calculation_XYZ2LUV_coordinate(self):
        # // Reference white is using self.Wx, self.Wy. 1nits Be Careful of the difference of RW
        return


    def Calculation_ResizeColorSpace(self):
        # // Willy : Resize standard to new color space, in order to construction new space with adjusted primary
        # // Advantage : ensure R,G,B = (1,1,1) is the D65, every color is continuous within this space
        # // Disadvantage : every color within this space wouold move from standard color space  
        return

       

    def Calculation_CuttingColorSpace(self):
        # // Willy : cutting out the color space
        # // Advantage : ervery color is same as standard color space which is overlap
        # // Disadvantage : color is not continuous when is face cutting part
        return
    
    # // Verification module
    def Verification(self):
        f1 = open("LabRef.txt",'r')
        f2 = open("measure.txt",'r')
        L_standard = []
        a_standard = []
        b_standard = []
        color = []
        L_measure = []
        a_measure = []
        b_measure = []
        for line in f1.readlines():
            data = line.split()
            L_standard.append(float(data[0]))
            a_standard.append(float(data[1]))
            b_standard.append(float(data[2]))
            # print(data)
            # color.append(hex(data[3]))
        for line in f2.readlines():
            data = line.split()
            L_measure.append(float(data[4]))
            a_measure.append(float(data[5]))
            b_measure.append(float(data[6]))
        return 


    def Plot_Verification(self):
        f1 = open("LabRef.txt",'r')
        f2 = open("measure.txt",'r')
        L_standard = []
        a_standard = []
        b_standard = []
        color = []
        L_measure = []
        a_measure = []
        b_measure = []
        for line in f1.readlines():
            data = line.split()
            L_standard.append(float(data[0]))
            a_standard.append(float(data[1]))
            b_standard.append(float(data[2]))
            # print(data)
            # color.append(hex(data[3]))
        for line in f2.readlines():
            data = line.split()
            L_measure.append(float(data[4]))
            a_measure.append(float(data[5]))
            b_measure.append(float(data[6]))
        for i in range(len(L_standard)):
            plt.scatter(a_standard[i],b_standard[i],c = 'black')
            plt.scatter(a_measure[i],b_measure[i], c = 'b')
            plt.annotate(i+1, (a_standard[i],b_standard[i]))
        plt.xlim(-70,80)
        plt.ylim(-70,100)
        plt.show()
        # return L,a,b
      
    

    
    
       
if __name__ == "__main__" :

    # initialize the class
    Application = Color_Application()
    Application.CS.Setting_R(0.596441999, 0.355781034)
    Application.CS.Setting_G(0.297029107, 0.574883202)
    Application.CS.Setting_B(0.151284294, 0.074234338)
    Application.CS.Setting_W(0.264637327, 0.275447912)
    # a = ColorSpace(0.6758,0.3132105,0.19,0.7,0.1509,0.03039,0.31272,0.32903) # // purple

    print(Application.CS.RGB2XYZ_matrix)





