import ROOT as r 
import xml.etree.ElementTree as ET
import math
from array import array
<<<<<<< Updated upstream
import wsh

=======
>>>>>>> Stashed changes

r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(True)

	
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

c2 = r.TCanvas()

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
			l_wsh5 =  wsh.WheelSectorHistograms5(file, name, full_data, 7.5)
		else:
			#l_wsh.add(wsh.WheelSectorHistograms(file, name, full_data, 7.5))
			l_wsh5.add(wsh.WheelSectorHistograms5(file, name, full_data, 7.5))
		count = count +1 
	#l_wsh.draw_hists()
	l_wsh5.draw_hists(c2)
	
	#hist_array.append(l_wsh)
	hist_array5.append(l_wsh5)



import makeplots


#print dir(hist_array[0])


<<<<<<< Updated upstream
makeplots.make2dStatsPlotsPHI(hist_array5, "X", .1,"output_mc_2", .02, c2)
makeplots.make2dStatsPlotsPHI(hist_array5, "Y", .3,"output_mc_2", .02, c2)
makeplots.make2dStatsPlotsPHI(hist_array5, "Z", .3,"output_mc_2", .02, c2)
makeplots.make2dStatsPlotsPHI(hist_array5, "PHIX", .03,"output_mc_2", .0005, c2)
makeplots.make2dStatsPlotsPHI(hist_array5, "PHIY", .014,"output_mc_2", .0005, c2)
makeplots.make2dStatsPlotsPHI(hist_array5, "PHIZ", .002,"output_mc_2", .0005, c2)
		
=======
#make2dStatsPlots(hist_array, "X", .1)
#make2dStatsPlots(hist_array, "Y", .2)
#make2dStatsPlots(hist_array, "Z", .3)
#make2dStatsPlots(hist_array, "PHIX", .01)
#make2dStatsPlots(hist_array, "PHIY", .014)
#make2dStatsPlots(hist_array, "PHIZ", .002)


TH2F_X_absmean_DTs = r.TH2F("TH2F_X_absmean_DTs", "Final chamber position X vs. approximate luminosity; L; X abs(mean) (cm) ", 100, 0, 9, 100, 0, .04)


meanRangeX = .04
meanRangeY = .2
meanRangeZ = .2
meanRangePhiX = .004
meanRangePhiY = .004
meanRangePhiZ = .001

TH2F_X_mean_DTs = r.TH2F("TH2F_X_mean_DTs", "Final chamber position X vs. approximate luminosity; L; X mean (cm) ", 100, 0, 9, 100, 0, meanRangeX )
TH2F_Y_mean_DTs = r.TH2F("TH2F_Y_mean_DTs", "Final chamber position Y vs. approximate luminosity; L; Y mean (cm) ", 100, 0, 9, 100, 0, meanRangeY )
TH2F_Z_mean_DTs = r.TH2F("TH2F_Z_mean_DTs", "Final chamber position Z vs. approximate luminosity; L; Z mean (cm) ", 100, 0, 9, 100, 0, meanRangeZ )

TH2F_PhiX_mean_DTs = r.TH2F("TH2F_PhiX_mean_DTs", "Final chamber position #phi_{X} vs. approximate luminosity; L; #phi_{X} mean (cm) ", 100, 0, 9, 100, 0, meanRangePhiX )
TH2F_PhiY_mean_DTs = r.TH2F("TH2F_PhiY_mean_DTs", "Final chamber position #phi_{Y} vs. approximate luminosity; L; #phi_{Y} mean (cm) ", 100, 0, 9, 100, 0, meanRangePhiY )
TH2F_PhiZ_mean_DTs = r.TH2F("TH2F_PhiZ_mean_DTs", "Final chamber position #phi_{Z} vs. approximate luminosity; L; #phi_{Z} mean (cm) ", 100, 0, 9, 100, 0, meanRangePhiZ )




rmsRangeX = .04
rmsRangeY = .2
rmsRangeZ = .2
TH2F_X_rms_DTs = r.TH2F("TH2F_X_rms_DTs", "Final chamber position X vs. approximate luminosity; L; X RMS (cm) ", 100, 0, 9, 100, 0, rmsRangeX)
TH2F_Y_rms_DTs = r.TH2F("TH2F_Y_rms_DTs", "Final chamber position Y vs. approximate luminosity; L; Y RMS (cm) ", 100, 0, 9, 100, 0, rmsRangeY)
TH2F_Z_rms_DTs = r.TH2F("TH2F_Z_rms_DTs", "Final chamber position Z vs. approximate luminosity; L; Z RMS (cm) ", 100, 0, 9, 100, 0, rmsRangeZ)
rmsRangePhiX = .004
rmsRangePhiY = .004
rmsRangePhiZ = .001
TH2F_phiX_rms_DTs = r.TH2F("TH2F_phiX_rms_DTs", "Final chamber position #phi X vs. approximate luminosity; L; #phi X RMS (cm) ", 100, 0, 9, 100, 0, rmsRangePhiX)
TH2F_phiY_rms_DTs = r.TH2F("TH2F_phiY_rms_DTs", "Final chamber position #phi Y vs. approximate luminosity; L; #phi Y RMS (cm) ", 100, 0, 9, 100, 0, rmsRangePhiY)
TH2F_phiZ_rms_DTs = r.TH2F("TH2F_phiZ_rms_DTs", "Final chamber position #phi Z vs. approximate luminosity; L; #phi Z RMS (cm) ", 100, 0, 9, 100, 0, rmsRangePhiZ)

for count, report in enumerate(report_array):
	print report.totalMuons, report.totalMuons/stats_7_5_fb*7.5
	print report.TH1F_X.GetRMS(), report.TH1F_X.GetStdDev()

	TH2F_X_rms_DTs.Fill(report.totalMuons/stats_7_5_fb*7.5,report.TH1F_X.GetRMS())
	TH2F_Y_rms_DTs.Fill(report.totalMuons/stats_7_5_fb*7.5,report.TH1F_Y.GetRMS())
	TH2F_Z_rms_DTs.Fill(report.totalMuons/stats_7_5_fb*7.5,report.TH1F_Z.GetRMS())
	TH2F_phiX_rms_DTs.Fill(report.totalMuons/stats_7_5_fb*7.5,report.TH1F_phiX.GetRMS())
	TH2F_phiY_rms_DTs.Fill(report.totalMuons/stats_7_5_fb*7.5,report.TH1F_phiY.GetRMS())
	TH2F_phiZ_rms_DTs.Fill(report.totalMuons/stats_7_5_fb*7.5,report.TH1F_phiZ.GetRMS())

	TH2F_X_mean_DTs.Fill(report.totalMuons/stats_7_5_fb*7.5, report.absAverageX)
	TH2F_Y_mean_DTs.Fill(report.totalMuons/stats_7_5_fb*7.5, report.absAverageY)
	TH2F_Z_mean_DTs.Fill(report.totalMuons/stats_7_5_fb*7.5, report.absAverageZ)
	TH2F_PhiX_mean_DTs.Fill(report.totalMuons/stats_7_5_fb*7.5, report.absAveragePhiX)
	TH2F_PhiY_mean_DTs.Fill(report.totalMuons/stats_7_5_fb*7.5, report.absAveragePhiY)
	TH2F_PhiZ_mean_DTs.Fill(report.totalMuons/stats_7_5_fb*7.5, report.absAveragePhiZ)


	#TH2F_X_mean_DTs.Fill(report.totalMuons/stats_7_5_fb*7.5, abs(report.TH1F_X.GetMean()))



c4 = r.TCanvas()

th1f_x = []
th1f_x_fit = []

for wheel in range(3):
	th1f_x.append([])
	th1f_x_fit.append([])
	for station in range(4):
		th1f_x[wheel].append(r.TH2F("th1f_x_{}_{}".format(wheel,station+1), "th1f_x_{}_{}; eqv fb; x cm".format(wheel,station+1), 10, 0, 20, 100, -.01, .2))
		th1f_x_fit[wheel].append(r.TH1F("th1f_x_fit_{}_{}".format(wheel,station+1), "th1f_x_fit_{}_{}; eqv fb; x cm".format(wheel,station+1), 10, 0, 20))

		#print wheel, station



for i in range(len(report_array)-1):
	#for j in range(len(report_array[i].chambers)):
	
	for j in range(len(report_array[i].chambers)):
		wheel_address = report_array[i].chambers[j].wheel 
		station_address = report_array[i].chambers[j].station 
		#print wheel_address, station_address, 
		th1f_x[abs(wheel_address)-1][station_address-1].Fill((report_array[i].chambers[j].stats+ .0)/(full_data.chambers[j].stats+.0)*7.5, report_array[i].chambers[j].x )


for wheel in range(3):
	for station in range(4):
		drawFunction2d(th1f_x[wheel][station], "x_{}_{}".format(wheel+1,station+1), .4)

		for bin_address in range(th1f_x[wheel][station].GetNbinsX()):
			temp = th1f_x[wheel][station].ProjectionY("{}_{}_{}".format(wheel, station, bin_address),bin_address+1,bin_address+1 )
			if temp.GetEntries() > 0:
				sigmas = 1.5
				lower, upper = temp.GetMean()-sigmas*temp.GetRMS(), temp.GetMean()+sigmas*temp.GetRMS()
				temp.Fit("gaus","", "", lower, upper)		
				fit = temp.GetFunction("gaus")
				print fit.GetParameter(2)
				th1f_x_fit[wheel][station].SetBinContent(bin_address,fit.GetParameter(2))
				th1f_x_fit[wheel][station].SetBinError(bin_address,fit.GetParError(2))
				#yq = array('d', [0.] * 2)
				#xq = array('d', [0.] * 2)
				#th1f_x_fit[wheel][station].GetQuantiles(2,xq,  yq)
				#print xq
				#th1f_x_fit[wheel][station].SetBinContent(bin_address, xq)
				#th1f_x_fit[wheel][station].SetBinError(bin_address, h1f_x_fit[wheel][station].GetRMS()*1.253/math.Sqrt(th1f_x_fit[wheel][station].GetEntries() ))
				

		th1f_x_fit[wheel][station].GetYaxis().SetRangeUser(-.1, .4)
		drawFunction(th1f_x_fit[wheel][station], "x_fit_{}_{}".format(wheel+1,station+1), .4)

	
	

>>>>>>> Stashed changes


