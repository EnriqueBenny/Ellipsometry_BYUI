import numpy as np
import cmath as cm
import matplotlib.pyplot as plt
import csv

 
class Ellipsometer:
    def __init__(self):
        '''
            Initializes the Ellipsometer class. 

            variables:
                self.alpha_1:   Polarizer Azimuth Angle (alpha 1) in degrees (int)
                self.alpha_2:   Analyzer (alpha 2) angles in degrees (array of int)
                self.Aoi:       Angle of Incidence (Aoi) in degrees (array of int)
                self.model_Aoi: Angle of Incidence (Aoi) in degress for the model calculation (array of int)
                self.psi:       Psi value (array of float)
                self.delta:     Delta value (array of float)
                self.exp_P:     Our P-Value as determined by the experiment (array of float)
                self.wavel:     Wavelength of Light from the laser (float)
                # The comments below, from self.n0 to self.k2 need to be fixed. 
                # It's not clear what purpose they serve, so the comments are currently general.
                self.n0:        Atomsphere Section (int)
                self.k0:        Atmosphere Section (int)
                self.n1:        Film Section, best not to mess with this section unless necessary. (float)
                self.k1:        Film Section, best not to mess with this section unless necessary. (float)
                self.d1:        Film Section, best not to mess with this section unless necessary. (float)
                self.n2:        Substrate Section (float)
                self.k2:        Substrate Section (float)
        '''

        self.alpha_1 = 45
        self.alpha_2 = [45,90,-45,0] 
        self.Aoi = [20,25,30,35,40,45,50,55,60,65,70,75]
        self.model_Aoi = np.arange(1,90,1)
        self.psi = []
        self.delta = []
        self.exp_P = []
        self.wavel = 6530.0
        # Index of Refraction Solver Inputs
        self.n0 = 1
        self.k0 = 0
        self.n1 = 1.4830
        self.k1 = 0.0000
        self.d1 = 14857 # Angs
        self.n2 = 3.844
        self.k2 = 0.015793

    def view_data(self):
        '''
            Inspect the current data in the .csv file. 
            Can be used to check proper updates while the code is running.
            The first line in the csv gives the formatting. 
            Uncomment the 'next(data)' call to get rid of it.

            Parameters:
                None
        '''

        with open('Ellipsometry_BYUI/ellipsometry_data.csv') as data:
            #next(data)
            reader = csv.reader(data)
            for i in reader:
                print(i)
        
    def data_entry(self):
        '''
            Enter data into the .csv file. Mistakes are easier to correct in the .csv file.
            This function can be skipped, just enter the data directly into the
            .csv, but ensure that proper formatting is maintained.
            The line, writer.writerow(['Aoi',45,90,-45,0]) exists to provide formatting. 
        '''

        with open('Ellipsometry/ellipsometry_data.csv','w', newline='') as data:
            
            writer = csv.writer(data)
            writer.writerow(['Aoi',45,90,-45,0]) #Adds the formatting to the csv file.
            print('If data for an Aoi has not been collected, type "skip".')

            for i in self.Aoi:
                line = [i]
                for j in self.alpha_2:
                    inp = input(f'For Aoi {i}, enter in {j} Intensity: ')
                    if inp.lower() == 'skip':
                        break
                    line.append(inp)
                print(f'Appending: {line}')
                writer.writerow(line)

        self.view_data()

    def Calculate(self): 
        '''
            Calculates the Psi and Delta values. 
            Pages 446 and 447 of the Mantia Bixby paper explain what Psi and Delta are.
            Contains the sub-functions Cal_Psi and Cal_Delta.
            Data must be entered prior to this function call for it to work.
        '''

        def Cal_Psi(nt, zr):
            '''
                Calculates Psi for a single line from the csv.
                This one must be called before Cal_Delta as Psi is used in calculating delta.
                The code curently does this automatically.

                Parameters:
                    self.psi = a class array (float) psi will be appended to.
                    nt = the ninety degree measurement
                    zr = the zero degree measurement
            '''

            self.psi.append(np.arctan(np.tan(self.alpha_1)*np.tan(np.arccos((nt-zr)/(nt+zr))/2)))

        def Cal_Delta(ff,nff):
            '''
                Calculates Delta for a single line from the csv.
                This one must be called after Cal_Psi as Psi is needed for these calculations.
                The code currently does this automatically.

                Parameters:
                    self.delta = a class array (float) delta will be appended to.
                    ff = The Forty-Five degree measurement
                    nff = The Negative Forty-Five degree measurement
            '''

            self.delta.append(np.arccos(((ff-nff)/(ff+nff))/\
                              np.sin(2*np.arctan(np.tan(self.psi[-1])/np.tan(self.alpha_1)))))

        with open('Ellipsometry_BYUI/ellipsometry_data.csv','r') as data:
            reader = csv.reader(data)
            self.Aoi = [] # To keep the number of variables lower, this one is being reused to overwrite the 
                          # initialized version. 

            for line in reader:

                try: # The try/except exist to prevent issues ocurring if the formatting line is removed.
                    erorr_test = int(line[0])
                except:
                    continue

                if len(line) > 1: # This line exists to handle skipped measurements.
                    aoi = int(line[0]) # Angle of Incidence
                    ff = int(line[1]) # Forty-Five degree angle
                    nt = int(line[2]) # Ninety degree angle
                    nff = int(line[3]) # Negative Forty-Five degree angle
                    zr = int(line[4]) # Zero Degree Angle

                    self.Aoi.append(aoi)
                    Cal_Psi(nt,zr)
                    Cal_Delta(ff,nff)

                    
            for i in range(len(self.Aoi)):
                self.psi[i] = round(180*self.psi[i]/np.pi,2)
                self.delta[i] = round(180*self.delta[i]/np.pi,2)
                print(f'Aoi: {aoi}, Psi: {self.psi}, Delta: {self.delta}')
    
    def Model(self):
        '''
            Calculates the Model Fitting.
        '''
        def to_rad(value):
            return np.radians(value)
        model_rads = list(map(to_rad, self.model_Aoi)) # Create an array from the model_Aoi of radians.
        #print(model_rads)
        N0 = np.complex(self.n0, self.k0)
        N1 = np.complex(self.n1, self.k1)
        N2 = np.complex(self.n2, self.k2)
        



    def Experiment_P(self):
        '''
            Taken from the second tab of the referenced Excel Document, this function calculates
            our P values from the experimental data. The model P is calulated in Model_P.
        '''
        for i in range(len(self.psi)): # This loop could be condenced, but is written this way for legibility.
            psi_rad = np.radians(self.psi[i]) # These calculations need to be done in radians.
            delta_rad = np.radians(self.delta[i])

            psi_cal = cm.tan(psi_rad) # The tangent of psi.
            delta_cal = cm.exp(cm.rect(1, delta_rad)) # reading the documentation of rect is recommended.

            self.exp_P.append(psi_cal*delta_cal)

    def Model_P(self):
        '''
            Taken from the second tab of the referenced Excel Document, this function calculates
            our P values from the model. The experimental P is calculated in Experiment_P
        '''
        pass


    def Plot_PD(self):
        '''
            Plot Aoi vs Psi and Aoi vs Delta. 
            Must be called after the Calculate method.
        '''

        plt.scatter(self.Aoi,self.psi)
        plt.scatter(self.Aoi,self.delta)
        plt.xlim(5,90)
        plt.xticks(np.arange(5,90,5))
        plt.ylim(0,200)
        plt.yticks(np.arange(0,200,20))
        plt.show()

# Class Call
E = Ellipsometer()

# Method Calls
#E.data_entry() # Keep commented if entering data via csv.
E.view_data()
E.Model()
#E.Calculate() # Call after the data is entered.
#E.Plot_PD() # Call after Calculate


''' A copy of the test data for the .csv.
Aoi,45,90,-45,0
25,1,60,137,67
30,3,101,202,88
35,11,211,373,137
40,18,310,501,160
45,25,357,524,153
50,49,295,402,117
55,50,145,219,113
60,29,31,141,135
65,167,225,214,155
'''