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
# // 3. transformation between xyY <-> XYZ <-> LAB
# // ColorCheckerBoard class collect 24 color checkerboard data
# //

class Color_Application():

    def __init__(self,Rx, Ry, Gx, Gy, Bx, By, Wx, Wy):
        self.Color = ColorSpace(Rx, Ry, Gx, Gy, Bx, By, Wx, Wy)
        self.board = ColorCheckerBoard_2005()

    def Calculation_RYGYBY(self,WY):
        # // Case : for LED brightness criteria
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
        # // For corrected color temperature 1st step
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
        # // Case : for ILI9341 primary color shift issue, 1st solution
        # // Resize standard to new color space, in order to construction 
        # // new space with adjusted primary ---->> RGB=(1,1,1) = D65
        grayscale = []
        standard_color = []
        resize_color = []
        standard_color_xy = []
        resize_color_xy = []
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
        self.Color.Setting_sRGB()
        for i in range(0,len(grayscale)):
            X,Y,Z = self.Color.Calculation_RGB2XYZ(grayscale[i][0][0],grayscale[i][1][0],grayscale[i][2][0])
            x,y,Y = self.Color.Calculation_XYZ2xyY(X,Y,Z)
            L,a,b = self.Color.Calculation_XYZ2LAB(X,Y,Z)
            standard_color.append([L,a,b])
            standard_color_xy.append([x,y,Y])
        # // calculate Ili9341 lab
        self.Color.Setting_NewColorSpace( 0.596441999, 0.355781034, \
        0.297029107, 0.574883202, \
        0.151284294, 0.074234338, \
        0.264637327, 0.275447912) # // ILI9341 color
        self.Color.Setting_W(0.3127,0.329) # // KEY part !!!!!!!!!!
        for i in range(0,len(grayscale)):
            X,Y,Z = self.Color.Calculation_RGB2XYZ(grayscale[i][0][0],grayscale[i][1][0],grayscale[i][2][0])
            x,y,Y = self.Color.Calculation_XYZ2xyY(X,Y,Z)
            L,a,b = self.Color.Calculation_XYZ2LAB(X,Y,Z)
            resize_color.append([L,a,b])
            resize_color_xy.append([x,y,Y])

        # #  // prepare for compareing
        # standard_color_x = []
        # standard_color_y = []
        # resize_color_x = []
        # resize_color_y =[]
        # plt.figure(figsize=[24,24])
        # fig, axes = colour.plotting.diagrams.plot_chromaticity_diagram_CIE1931(standalone=False)
        # for i in range(0,len(standard_color_xy)):
        #     temp_a = [] #// use to plot connecting line between resize and standard
        #     temp_b = []
        #     standard_color_x.append(standard_color_xy[i][0][0])
        #     standard_color_y.append(standard_color_xy[i][1][0])
        #     resize_color_x.append(resize_color_xy[i][0][0])
        #     resize_color_y.append(resize_color_xy[i][1][0])
        #     temp_a.append([standard_color_xy[i][0][0],resize_color_xy[i][0][0]])
        #     temp_b.append([standard_color_xy[i][1][0],resize_color_xy[i][1][0]])
        #     axes.scatter(standard_color_x[i],standard_color_y[i],c = 'black')
        #     axes.scatter(resize_color_x[i],resize_color_y[i], c = 'red')
        #     axes.plot(temp_a[0],temp_b[0],color = 'black')
        #     axes.annotate(i+1, (standard_color_x[i],standard_color_y[i]))
        # # // plot for primary
        # ILIprimary_x = [0.596441999, 0.297029107,0.151284294,0.596441999]
        # ILIprimary_y = [0.355781034, 0.574883202,0.074234338,0.355781034]
        # self.Color.Setting_sRGB()
        # sRGBprimary_x = [self.Color.Rx,self.Color.Gx,self.Color.Bx,self.Color.Rx]
        # sRGBprimary_y = [self.Color.Ry,self.Color.Gy,self.Color.By,self.Color.Ry]
        # axes.plot(sRGBprimary_x,sRGBprimary_y,color='black',label = 'sRGB')
        # axes.plot(ILIprimary_x,ILIprimary_y,color = 'red',label = 'ILI9341')
        # axes.legend()
        # fig.show()
        # plt.show()
        
        # // prepare for compareing
        standard_color_a = []
        standard_color_b = []
        resize_color_a = []
        resize_color_b =[]
        # // plot lab
        for i in range(0,len(standard_color)):
            temp_a = [] #// use to plot connecting line between resize and standard
            temp_b = []
            standard_color_a.append(standard_color[i][1][0])
            standard_color_b.append(standard_color[i][2][0])
            resize_color_a.append(resize_color[i][1][0])
            resize_color_b.append(resize_color[i][2][0])
            temp_a.append([standard_color_a,resize_color_a])
            temp_b.append([standard_color_b,resize_color_b])
            plt.plot(temp_a[0],temp_b[0],color = 'black')
            plt.annotate(i+1, (standard_color_a[i],standard_color_b[i]))
        plt.scatter(standard_color_a,standard_color_b,c = 'black',label = "sRGB")
        plt.scatter(resize_color_a,resize_color_b, c = 'red',label = "Ili9341")
        img = plt.imread("Lab.png")
        plt.imshow(img, extent=[-70, 80, -70, 100])
        plt.legend()
        plt.xlim(-70,80)
        plt.ylim(-70,100)
        plt.show()
        
        return

    def Calculation_CuttingColorSpace(self):
        # // Case : for ILI9341 primary color shift issue, 2nd solution
        # // Willy : cutting out the color space

        return
    

    
    
       
if __name__ == "__main__" :

    # initialize the class
    Application = Color_Application(
        0.596441999, 0.355781034, \
        0.297029107, 0.574883202, \
        0.151284294, 0.074234338, \
        0.264637327, 0.275447912) # ILI9341
    Application.Calculation_ResizeColorSpace()
    