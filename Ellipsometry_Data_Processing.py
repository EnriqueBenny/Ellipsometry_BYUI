import numpy as np
import matplotlib.pyplot as plt
import csv

 
class Ellipsometer:
    def __init__(self):
        '''
            Initializes the Ellipsometer class. 

            variables:
                self.alpha_1: Polarizer Azimuth Angle (alpha 1) in degrees (int)
                self.alpha_2: Analyzer (alpha 2) angles in degrees (array of int)
                self.Aoi:     Angle of Incidence (Aoi) in degrees (array of int)
                self.psi:     Psi value (array of float)
                self.delta:   Delta value (array of float)
        '''

        self.alpha_1 = 45
        self.alpha_2 = [45,90,-45,0] 
        self.Aoi = [20,25,30,35,40,45,50,55,60,65,70,75]
        self.psi = []
        self.delta = []

    def view_data(self):
        '''
            Inspect the current data in the .csv file. 
            Can be used to check proper updates while the code is running.
            The first line in the csv gives the formatting. 
            Uncomment the 'next(data)' call to get rid of it.

            Parameters:
                None
        '''

        with open('ellipsometry_data.csv') as data:
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

        with open('ellipsometry_data.csv','r') as data:
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

    def Plot_PD(self):
        '''
            Plot Aoi vs Psi and Aoi vs Delta. 
            Must be called after the Calculate method.
        '''

        plt.scatter(self.Aoi,self.psi)
        plt.scatter(self.Aoi,self.delta)
        plt.xlim(5,90)
        plt.xticks(np.arange(5,90,5))
        plt.show()

# Class Call
E = Ellipsometer()

# Method Calls
#E.data_entry() # Keep commented if entering data via csv.
E.view_data()
E.Calculate() # Call after the data is entered.
E.Plot_PD() # Call after Calculate

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