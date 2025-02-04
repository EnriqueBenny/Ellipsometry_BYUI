# Ellipsometer Optimization

## Introduction and Background
The purpose of this code is to provide an improved interactability and
visualization of an existing project: "Optical measurements on a budget: A 3D-printed
ellipsometer" by Matthew Mantia and Teresa Bixby, linked also in this folder.

While there exists a working program, it resides in excel, creating a highly limited environment for visualization and interaction. By migrating it to python, we hope to improve the code and the environment.

## Contents:
Budged_Ellipsometer_Mantia_Bixby.pdf -> The Referenced Paper. (https://pubs.aip.org/aapt/ajp/article-abstract/90/6/445/2820104/Optical-measurements-on-a-budget-A-3D-printed?redirectedFrom=fulltext)

Ellipsometry_Data_Processing.py -> The main python folder

ellipsometry_data.csv -> The storage file for the data.

## Notes:

- Either via the provided code or manually, enter the collected data into the csv file.
    - Notes: Do not add additional lines. Maintain the proper formatting and don't forget commas. 
    This will be handled automatically if entered in via the code.
    *The Data in the CSV will be overwritten every time the code is run.*


# License

Copyright (c) [2025] [Erik Benson]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.