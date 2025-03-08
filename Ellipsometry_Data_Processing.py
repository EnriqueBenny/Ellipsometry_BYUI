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
            Calculates the Model Fitting. I used the map() function as a quick way to 
            apply repeated processes while avoiding loops. This is going to be a 
            very difficult section to read, as a warning.
        '''
        # N Parameters
        N0 = complex(self.n0, self.k0)
        N1 = complex(self.n1, self.k1)
        N2 = complex(self.n2, self.k2)

        def to_rad(deg):
            return np.radians(deg)
        model_rads = list(map(to_rad, self.model_Aoi)) # Create an array from the model_Aoi of radians.

        # All following functions are for intermediate parameters. 
        # See columns T to AD in the third tab on the excel document.
        def COS0(rads):
            return cm.sqrt(1.0 - cm.sin(rads) * cm.sin(rads))
        cos0 = list(map(COS0, model_rads))
        
        def COS1(value):
            return cm.sqrt(N1**2 - N0**2 * (cm.sin(value)**2)) / N1
        cos1 = list(map(COS1, model_rads))

        def COS2(value):
            return cm.sqrt(N2**2 - N0**2 * (cm.sin(value)**2)) / N2
        cos2 = list(map(COS2, model_rads))

        def P1_PI(value1, value2):
            return  (N1*value1 - N0 * value2)/(N1*value1+N0*value2)
        p1_pi = list(map(P1_PI, cos0, cos1))

        def P1_SIG(value1,value2):
            return (N0*value1 - N1*value2)/(N0*value1+N1*value2)
        p1_sig = list(map(P1_SIG, cos0, cos1))

        def P2_PI(value1, value2):
            return (N2*value1-N1*value2)/(N2*value1+N1*value2)
        p2_pi = list(map(P2_PI, cos1, cos2))

        def P2_SIG(value1,value2):
            return (N1*value1-N2*value2)/(N1*value1+N2*value2)
        p2_sig = list(map(P2_SIG, cos1, cos2))

        def Beta(value):
            return 2 * np.pi * (self.d1 / self.wavel) * N1 * value
        beta = list(map(Beta, cos1))

        def P_PI(value1, value2, value3):
            exp = cm.exp(-2j*value3)
            return (value1 + value2 * exp)/(1 + value1 * value2 * exp)
        p_pi = list(map(P_PI, p1_pi, p2_pi, beta))

        def P_Sigma(value1, value2, value3):
            exp = cm.exp(-2j*value3)
            return (value1+value2*exp)/(1+value1*value2*exp)
        p_sigma = list(map(P_Sigma, p1_sig,p2_sig,beta))

        def parameter_P(value1,value2):
            return value1/value2
        P = list(map(parameter_P, p_pi, p_sigma))
        
        # The following has been made available for the entire class.
        def model_Psi_rads(value):
            return np.arctan(np.abs(value))
        self.Psi_rads = list(map(model_Psi_rads,P))

        def model_Delta_rads(value):
            return cm.phase(value)
        self.Delta_rads = list(map(model_Delta_rads,P))

        def to_deg(value):
            return np.degrees(value)
        self.Psi_deg = list(map(to_deg,self.Psi_rads))
        
        def to_deg_delta(value):
            return np.degrees(np.abs(value))
        self.Delta_deg = list(map(to_deg_delta,self.Delta_rads))

    def Model_P(self):
        '''
            Calculates P values from the Model. 
            The self.Model() function must be run for this function
            to work, so it was included to prevent user error.
        '''
        self.Model()

        def P(value1, value2):
            return cm.tan(value1) * cm.exp(1j * value2)
        mod_P = list(map(P,self.Psi_rads,self.Delta_rads))


    def Experiment_P(self):
        '''
            Taken from the second tab of the referenced Excel Document, this function calculates
            our P values from the experimental data. The model P is calulated in Model_P.
        '''
        def to_rads(value):
            return np.radians(value)
        psi_rad = list(map(to_rads,self.psi))
        delta_rad = list(map(to_rads,self.delta))
        
        def Psi_Cal(value):
            return cm.tan(value)
        psi_cal = list(map(Psi_Cal,psi_rad))

        def Delta_Cal(value):
            return cm.exp(cm.rect(1, value))
        delta_cal = list(map(Delta_Cal,delta_rad))

        def Exp_P(value1, value2):
            return value1*value2
        self.exp_P = list(map(Exp_P,psi_cal,delta_cal))

    def Fit_Err(self):
        '''
            Calculates the fitting error rate as a %. Must be run after Model().

            CURRENTLY BROKEN.
        '''
        def Err(value1,value2):
            return np.abs(value1-value2)/value2
        #self.psi_err = list(map(Err,self.,self.Psi_deg))
        #self.delta_err = list(map(Err,))

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
#E.view_data()
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