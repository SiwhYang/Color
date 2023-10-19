class Manipulate():
    def color_name(self):
            return (list(self.__dict__.keys()))
    def color_value(self):
        color_value = []
        for element in list(self.__dict__.keys()):
            color_value.append(getattr(self,element))
        return color_value
    

class ColorCheckerBoard_2005():
    def __init__(self):
        self.CIExyY = self.CIExyY()
        self.CIELAB_D50 = self.CIELAB_D50()

    class CIExyY(Manipulate):
        def __init__(self):
            self.Dark_skin = [0.4316, 0.3777 ,10.08]
            self.Light_skin = [0.4197, 0.3744, 34.95]
            self.Blue_sky = [0.2760, 0.3016, 18.26]
            self.Foliage = [0.3703, 0.4499, 13.25]
            self.Blue_flower = [0.2999, 0.2856, 23.04] 
            self.Bluish_green = [0.2848, 0.3911, 41.78]
            self.Orange = [0.5295, 0.4055, 31.18]
            self.Purplish_blue = [0.2305, 0.2106, 11.26]   
            self.Moderate_red = [0.5012, 0.3273, 19.38] 
            self.Purple = [0.3319, 0.2482, 6.37]
            self.Yellow_green = [0.3984, 0.5008, 44.46 ] 
            self.Orange_yellow = [0.4957, 0.4427, 43.57] 
            self.Blue = [0.2018, 0.1692, 5.75 ]
            self.Green = [0.3253, 0.5032, 23.18 ]
            self.Red = [0.5686, 0.3303, 12.57  ]
            self.Yellow = [0.4697, 0.4734, 59.81]
            self.Magenta = [0.4159, 0.2688, 20.09]
            self.Cyan = [0.2131, 0.3023, 19.30] 
            self.White = [0.3469, 0.3608, 91.31 ]
            self.Neutral8 = [0.3440, 0.3584, 58.94]
            self.Neutral6 = [0.3432, 0.3581, 36.32]
            self.Neutral5 = [0.3446, 0.3579, 19.15 ]
            self.Neutral3 = [0.3401, 0.3548, 8.83]
            self.Black2 = [0.3406, 0.3537, 3.11]

    class CIELAB_D50(Manipulate):
        def __init__(self):
            self.Dark_skin = [ 37.99, 13.56, 14.06]
            self.Light_skin = [66.056, 17.737, 17.848]
            self.Blue_sky = [50.09, -4.407, -22.51]
            self.Foliage = [43.204, -13.46, 21.73]
            self.Blue_flower = [55.356, 8.891, -24.82] 
            self.Bluish_green = [70.700, -32.89, -0.24]
            self.Orange = [62.559,  35.135, 58.050]
            self.Purplish_blue = [40.178, 9.551, -44.28]   
            self.Moderate_red = [51.711, 47.694, 16.857] 
            self.Purple = [30.375, 21.131, -20.30]
            self.Yellow_green = [72.492, -23.46, 57.07] 
            self.Orange_yellow = [71.963, 19.486, 67.998] 
            self.Blue = [28.653, 15.600, -50.52]
            self.Green = [55.046, -38.088, 31.617]
            self.Red = [42.182, 54.893, 28.785]
            self.Yellow = [82.230, 4.048, 79.844]
            self.Magenta = [51.820, 49.787, -13.90]
            self.Cyan = [50.555, -27.973, -28.13] 
            self.White = [96.387, -0.404, 2.238 ]
            self.Neutral8 = [81.014, -0.570, 0.180]
            self.Neutral6 = [66.297, -0.434, -0.079]
            self.Neutral5 = [50.830, -0.687, -0.268]
            self.Neutral3 = [35.724,  -0.521, -0.468] 
            self.Black2 = [20.706, 0.025, -0.447]
        
        
if __name__ == "__main__" :
    ColorCheckerBoard = ColorCheckerBoard_2005()
    print(ColorCheckerBoard.CIExyY.color_value())