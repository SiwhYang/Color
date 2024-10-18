import pandas as pd
import os



class Integral_spectrum :

    def __init__ (self,color_matching_table,lightsource_spectrum):
        self.color_matching_table = None
        self.matching_wavelength = None
        self.matching_x = None
        self.matching_y = None
        self.matching_z = None
        self.lightsource_spectrum = None
        self.lightsource_wavelength = None
        self.lightsource_intensity = None
        self.probe(color_matching_table,lightsource_spectrum)
        self.X = None
        self.Y = None
        self.Z = None
        self.x = None
        self.y = None
        self.z = None
        self.calculation()

    def probe (self,color_matching_table,lightsource_spectrum) :
        CURRENT_DIR = os.path.dirname(__file__)  # Gets directory path of the current python module
        match_path = os.path.join(CURRENT_DIR,color_matching_table)
        light_path = os.path.join(CURRENT_DIR,lightsource_spectrum)
        self.color_matching_table = pd.read_csv(match_path)
        self.matching_wavelength = self.color_matching_table["wavelength"].T.to_numpy()
        self.matching_x = self.color_matching_table["x"].T.to_numpy()
        self.matching_y = self.color_matching_table["y"].T.to_numpy()
        self.matching_z = self.color_matching_table["z"].T.to_numpy()
        self.lightsource_spectrum = pd.read_csv(light_path)
        self.lightsource_wavelength = self.lightsource_spectrum["wavelength"].T.to_numpy()
        self.lightsource_intensity = self.lightsource_spectrum["intensity"].T.to_numpy()
        

    def calculation (self):
        if (len(self.matching_wavelength)  == len(self.lightsource_wavelength)):
            integral_x = 0
            integral_y = 0 
            integral_z = 0
            for i in range (0,len(self.matching_wavelength)):    
                if (int(self.matching_wavelength[i]) == int(self.lightsource_wavelength[i])) :    
                    integral_x = self.matching_x[i] * self.lightsource_intensity[i] + integral_x
                    integral_y = self.matching_y[i] * self.lightsource_intensity[i] + integral_y
                    integral_z = self.matching_z[i] * self.lightsource_intensity[i] + integral_z
                    self.X = integral_x
                    self.Y = integral_y
                    self.Z = integral_z
                    normalize = integral_x + integral_y + integral_z
                    self.x = integral_x/normalize
                    self.y = integral_y/normalize
                    self.z = integral_z/normalize

                else :
                    print("wavelength not match, check data format")
                    return
        else :
            
            print("wavelength length not match, check wavelength width ")
            return 
        

a = Integral_spectrum ("5mmColormatchingFunction.csv","5mmD65spectrum.csv")      
print(a.y)