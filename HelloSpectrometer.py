# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 21:57:20 2020

@author: justins
"""

#start - what do I need to talk to the spectrometer?

#import wrapper
from avaspec import *

#connect to the .dll

#(-1 Eth and USB, 0 USB, 256 Eth)
ret = AVS_Init(-1)
#or depricated AVS_GetNrOfDevices
ret = AVS_GetNrOfDevices()
#ret = AVS_UpdateUSBDevices()
#why 75? explain how to find this.
#lib = ctypes.CDLL("avaspecx64.dll")
#init; updateUSBDevices
#Param1 = 
#AVS_GetList()
ret = AVS_GetList(75, 75, AvsIdentityType*1)
handle = AVS_Activate(ret[1])

config = DeviceConfigType
ret = AVS_GetParameter(handle, 63484, 63484, config)
pixels = ret[1].m_Detector_m_NrPixels
lamb = AVS_GetLambda(handle,[])
wavelengths = []
for pix in range(pixels):
    wavelengths.append(lamb[pix])

ret = AVS_UseHighResAdc(handle, True)
measconfig = MeasConfigType
measconfig.m_StartPixel = 0
measconfig.m_StopPixel = pixels - 1
measconfig.m_IntegrationTime = 50 #in milliseconds
measconfig.m_IntegrationDelay = 0 #in FPGA clock cycles
measconfig.m_NrAverages = 1
measconfig.m_CorDynDark_m_Enable = 0  # nesting of types does NOT work!!
measconfig.m_CorDynDark_m_ForgetPercentage = 100
measconfig.m_Smoothing_m_SmoothPix = 0
measconfig.m_Smoothing_m_SmoothModel = 0
measconfig.m_SaturationDetection = 0
measconfig.m_Trigger_m_Mode = 0
measconfig.m_Trigger_m_Source = 0
measconfig.m_Trigger_m_SourceType = 0
measconfig.m_Control_m_StrobeControl = 0
measconfig.m_Control_m_LaserDelay = 0
measconfig.m_Control_m_LaserWidth = 0
measconfig.m_Control_m_LaserWaveLength = 0.0
measconfig.m_Control_m_StoreToRam = 0
ret = AVS_PrepareMeasure(handle, measconfig)

scans = 1
ret = AVS_Measure(handle, 0, scans)
dataready = False
import time
while not dataready:
    dataready = AVS_PollScan(handle)
    time.sleep(measconfig.m_IntegrationTime/1000)
        
timestamp = 0
spectraldata = []
ret = AVS_GetScopeData(handle, timestamp, spectraldata)
timestamp = ret[0]
for i,pix in enumerate(wavelengths):
    spectraldata.append(ret[1][i])

import matplotlib.pyplot as plt
plt.plot(wavelengths,spectraldata)
