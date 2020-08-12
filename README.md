# SDSS Data Extractor

This program uses your input parameter and specified astronomical catalog to find the value of the parameter for the SDSS object at that coordinates. I am using FSPS GranEarlyDust, however if you want to change the port just change the name on line 11.


###  The available ports (Fit Parameters) on the SDSS website are:

- sppParameters
- StarformingPort
- PassivePort
- emissionLinesPort
- PCAWiseBC03
- PCAWiseM11
- FSPSGranEarlyDust
- FSPSGranEarlyNoDust
- FSPSGranWideDust
- FSPSGranWideNoDust

The program can be extended to include Spec Summary and Imaging Summary as well by just changing the name in the URL 
