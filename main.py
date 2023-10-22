import colour
import colour.plotting
from colour.plotting.diagrams import render
import matplotlib.pyplot as plt
import numpy as np
from ColorCheckerBoard import ColorCheckerBoard_2005
from ColorSpace import ColorSpace

# // Willy state :
# // Colorspace class construct color spcae by giving rgbw cooridnate
# // 1. calculate RGB <-> XYZ matrix 2. tansform from RGB <-> XYZ by matrix
# // 3.  transformation between xyY <-> XYZ <-> LAB
# // ColorCheckerBoard class collect 24 color checkerboard data
# //

class Color_Application():

    def __init__(self,Rx, Ry, Gx, Gy, Bx, By, Wx, Wy):
        self.Color = ColorSpace(Rx, Ry, Gx, Gy, Bx, By, Wx, Wy)
        self.board = ColorCheckerBoard_2005()

    def Calculation_RYGYBY(self,WY):
        # // Willy : We get WY = RY*R + GY*G + BY*B from matrix expansion, where (R,G,B) = (1,1,1) denote white,
        # // RY, GY, BY could simply denote the luminance contriburtion of primary to white  
        # // Example : NTSC return RY = 0.2989, GY = 0.5864, BY = 0.1146
        # // this is how Gray = 0.299 * Red + 0.587 * Green + 0.114 * Blue coming from
        matrix = self.Color.Calculation_RGB2XYZ_matrix()
        RY = matrix[1][0]
        GY = matrix[1][1]
        BY = matrix[1][2]
        return RY*WY, GY*WY, BY*WY

    def Calculation_RGB2newcolor_ratio(self,x,y):
        # // Willy : WY is arbitrary since we would do normalize,
        # // If normalize is canceled, the vector should be careful for its length (reference to Calculation_RGB2XYZ_matrix )
        matrix = self.Color.Calculation_RGB2XYZ_matrix(1)
        vector = np.array([x,y,(1-x-y)])
        x = np.linalg.solve(matrix,vector)
        # // Normalize
        c = x[0]+x[1]+x[2]
        ratio = x/c
        return ratio

   
    def Calculation_ResizeColorSpace(self):
        # // Case : ILI9341 has red issue
        # // Resize standard to new color space, in order to construction new space with adjusted primary
        standard_color = []
        grayscale = []
        resize_color = []
        for color in self.board.CIExyY_D50.color_value():
            # // choose 24 color chart (D50) and get its graysacle
            # // This grayscale is not correct, cuase the sRGB provide more complex transformation than simply gamma transformation
            # // but our goal is just compare color shift in same grayscale, the absolute value of grayscale matters little
            self.Color.Setting_sRGB()
            self.Color.Setting_D50()
            X, Y, Z = self.Color.Calculation_xyY2XYZ(color[0],color[1],color[2]/100)
            grayscale_element = self.Color.Calculation_XYZ2RGB(X, Y, Z,Gamma=2.2)  
            grayscale.append(grayscale_element)

            # // calculate sRGB lab
            # self.Color.Setting_sRGB()
            # self.Color.Setting_NewColorSpace( 0.596441999, 0.355781034, \
            # 0.297029107, 0.574883202, \
            # 0.151284294, 0.074234338, \
            # 0.264637327, 0.275447912) # // ILI9341 color
            # self.Color.Calculation_RGB2XYZ()

        print((grayscale))  
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
    Application = Color_Application(
        0.596441999, 0.355781034, \
        0.297029107, 0.574883202, \
        0.151284294, 0.074234338, \
        0.264637327, 0.275447912) # ILI9341
    # Application.Color.Setting_sRGB()
    print(Application.Calculation_ResizeColorSpace())
    