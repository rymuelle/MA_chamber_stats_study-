import ROOT as r 
import xml.etree.ElementTree as ET
import math
from array import array
import wsh


r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(True)

c2 = r.TCanvas()

	
hist_array = []
hist_array5 = []

#execfile("mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01_report.py")
#example = wsh.ChamberInfo("test", reports, "mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01.xml")

#hist_array.append(wsh.WheelSectorHistograms("example", example))

#example2.draw_hists()

execfile("full_data.py")
full_data = wsh.ChamberInfo("full_data", reports, "full_data.xml")
#stats_7_5_fb = full_data.totalMuons

execfile("full.py")

full = wsh.ChamberInfo("full", reports, "full.xml")
fullwsh = wsh.WheelSectorHistograms5("full", full, full_data, 7.5, full_data)
fullwsh.draw_hists(c2)

#hist_array.append(wsh.WheelSectorHistograms("full", full, full_data, 7.5))
#hist_array5.append(wsh.WheelSectorHistograms5("full", full, full_data, 7.5))

#execfile("half.py")
#half = wsh.ChamberInfo("half", reports, "half.xml")
##hist_array.append(wsh.WheelSectorHistograms("half", half))
##hist_array[1].draw_hists()
#
#execfile("one_third.py")
#one_third = wsh.ChamberInfo("one_third", reports, "one_third.xml")
##hist_array.append(wsh.WheelSectorHistograms("one_third", one_third))
#
#
#execfile("one_sixth.py")
#one_sixth = wsh.ChamberInfo("one_sixth", reports, "one_sixth.xml")
##hist_array.append(wsh.WheelSectorHistograms("one_sixth", one_sixth))
#
#
#
#execfile("super_small.py")
#super_small = wsh.ChamberInfo("super_small", reports, "super_small.xml")
##hist_array.append(wsh.WheelSectorHistograms("super_small", super_small))
#
#
#execfile("superduper_small.py")
#superduper_small = wsh.ChamberInfo("superduper_small", reports, "superduper_small.xml")
#hist_array.append(wsh.WheelSectorHistograms("superduper_small", superduper_small))






#fileArray = ["div_16_3", "div_16_2", "div_16_1", "div_2_1", "div_16_8", "div_16_7", "div_16_6", "div_16_5", "div_16_4", "div_4_2", "div_4_1", "div_2_4", "div_2_3", "div_2_2", "div_4_4", "div_4_3", "div_8_4", "div_8_3", "div_8_2", "div_8_1", "div_8_8", "div_8_7", "div_8_6", "div_8_5"]
fileArray = []
fileArray.append(["div_16_3", "div_16_2", "div_16_1", "div_16_8", "div_16_7", "div_16_6", "div_16_5", "div_16_4"])
fileArray.append(["div_8_4", "div_8_3", "div_8_2", "div_8_1", "div_8_8", "div_8_7", "div_8_6", "div_8_5"])
fileArray.append([  "div_4_2", "div_4_1",  "div_4_4", "div_4_3" ])
fileArray.append([  "div_2_1", "div_2_4", "div_2_3", "div_2_2" ])
fileArray.append(["div_p7_3", "div_p7_2", "div_p7_1", "div_p7_8", "div_p7_7", "div_p7_6", "div_p7_5", "div_p7_4"])

for l_array in fileArray:
	count = 0
	for file in l_array:
		print count
		execfile("{}.py".format(file))
		name = wsh.ChamberInfo(file, reports, "{}.xml".format(file))
		if count == 0:
			#l_wsh =  wsh.WheelSectorHistograms(file, name, full_data, 7.5)
			l_wsh5 =  wsh.WheelSectorHistograms5(file, name, full_data, 7.5, full)
		else:
			#l_wsh.add(wsh.WheelSectorHistograms(file, name, full_data, 7.5))
			l_wsh5.add(wsh.WheelSectorHistograms5(file, name, full_data, 7.5, full))
		count = count +1 
	#l_wsh.draw_hists()
	l_wsh5.draw_hists(c2)
	
	#hist_array.append(l_wsh)
	hist_array5.append(l_wsh5)

import makeplots



#print dir(hist_array[0])



makeplots.make2dStatsPlotsPHI(hist_array5, "X", .1,"output_mc_2", .02, c2)
makeplots.make2dStatsPlotsPHI(hist_array5, "Y", .3,"output_mc_2", .02, c2)
makeplots.make2dStatsPlotsPHI(hist_array5, "Z", .3,"output_mc_2", .02, c2)
makeplots.make2dStatsPlotsPHI(hist_array5, "PHIX", .03,"output_mc_2", .0005, c2)
makeplots.make2dStatsPlotsPHI(hist_array5, "PHIY", .014,"output_mc_2", .0005, c2)
makeplots.make2dStatsPlotsPHI(hist_array5, "PHIZ", .002,"output_mc_2", .0005, c2)
		
