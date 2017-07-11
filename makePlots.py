import ROOT as r 
import xml.etree.ElementTree as ET
import math

r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(True)

c1 = r.TCanvas()

class Chamber:
	def __init__(self, report, child):
		self.detector = report.postal_address[0]
		self.wheel = report.postal_address[1]
		self.station= report.postal_address[2]
		self.sector = report.postal_address[3]
		self.stats = report.posNum
		self.x = float(child['x'])
		self.y = float(child['y'])
		self.z = float(child['z'])
		self.phix = float(child['phix'])
		self.phiy = float(child['phiy'])
		self.phiz = float(child['phiz'])


		
		

class ChamberInfo:
	def __init__(self, name, reports, xml):
		self.name = name
		self.chambers = []
		tree = ET.ElementTree(file=xml)
		root = tree.getroot()
		self.TH1F_X = r.TH1F("TH1F_X_{}".format(name), ";X position (cm);  count", 100, -1, 1)
		self.TH1F_Y = r.TH1F("TH1F_Y_{}".format(name), ";Y position (cm);  count", 100, -1, 1)
		self.TH1F_Z = r.TH1F("TH1F_Z_{}".format(name), ";Z position (cm);  count", 100, -1, 1)
		self.TH1F_phiX = r.TH1F("TH1F_phiX_{}".format(name), ";#phi X position (cm);  count", 100, -.02, .02)
		self.TH1F_phiY = r.TH1F("TH1F_phiY_{}".format(name), ";#phi Y position (cm);  count", 100, -.04, .04)
		self.TH1F_phiZ = r.TH1F("TH1F_phiZ_{}".format(name), ";#phi Z position (cm);  count", 100, -.01, .01)
		self.totalMuons = 0
		self.absAverageX = 0
		self.absAverageY = 0
		self.absAverageZ = 0
		self.absAveragePhiX = 0
		self.absAveragePhiY = 0
		self.absAveragePhiZ = 0

		self.set_values(reports, root)
		self.c2 = r.TCanvas()


	def set_values(self,reports, root):
		for count,report in enumerate(reports):
			if report.postal_address[0] == "DT":
				count = 0 
				for child in root.findall("./operation/*[@wheel='{}'][@station='{}'][@sector='{}']/../setposition".format(report.postal_address[1],report.postal_address[2], report.postal_address[3])):
					if(count == 0): 
						self.chambers.append(Chamber(report,child.attrib))
					count = count + 1

		for thing in enumerate(self.chambers):
			 self.TH1F_X.Fill(float(thing[1].x))
			 self.TH1F_Y.Fill(float(thing[1].y))
			 self.TH1F_Z.Fill(float(thing[1].z))
			 self.TH1F_phiX.Fill(float(thing[1].phix))
			 self.TH1F_phiY.Fill(float(thing[1].phiy))
			 self.TH1F_phiZ.Fill(float(thing[1].phiz))
			 self.totalMuons = self.totalMuons + float(thing[1].stats)
			 self.absAverageX = self.absAverageX + abs(float(thing[1].x))
			 self.absAverageY = self.absAverageY + abs(float(thing[1].y))
			 self.absAverageZ = self.absAverageZ + abs(float(thing[1].z))
			 self.absAveragePhiX = self.absAveragePhiX + abs(float(thing[1].phix))
			 self.absAveragePhiY = self.absAveragePhiY + abs(float(thing[1].phiy))
			 self.absAveragePhiZ = self.absAveragePhiZ + abs(float(thing[1].phiz))
		self.absAverageX = self.absAverageX/len(self.chambers)
		self.absAverageY = self.absAverageY/len(self.chambers)
		self.absAverageZ = self.absAverageZ/len(self.chambers)
		self.absAveragePhiX = self.absAveragePhiX/len(self.chambers)
		self.absAveragePhiY = self.absAveragePhiY/len(self.chambers)
		self.absAveragePhiZ = self.absAveragePhiZ/len(self.chambers)

	def drawHist(self):
		self.TH1F_X.Draw()
		self.c2.SaveAs("output_mc/TH1F_X_{}.png".format(self.name))

		self.TH1F_Y.Draw()
		self.c2.SaveAs("output_mc/TH1F_Y_{}.png".format(self.name))
		
		self.TH1F_Z.Draw()
		self.c2.SaveAs("output_mc/TH1F_Z_{}.png".format(self.name))
	
		self.TH1F_phiX.Draw()
		self.c2.SaveAs("output_mc/TH1F_phiX_{}.png".format(self.name))
	
		self.TH1F_phiY.Draw()
		self.c2.SaveAs("output_mc/TH1F_phiY_{}.png".format(self.name))
		
		self.TH1F_phiZ.Draw()
		self.c2.SaveAs("output_mc/TH1F_phiZ_{}.png".format(self.name))
		#print "stats: {} rms: {} mean: {}".format(self.totalMuons , self.TH1F_X.GetRMS(), self.TH1F_X.GetMean())
		print "{} \t {} \t {}".format(self.totalMuons , self.TH1F_X.GetRMS(), self.TH1F_X.GetMean())


				
		#for count, chamber in enumerate(self.chambers):
		#	print chamber.detector, chamber.wheel, chamber.station, chamber.sector, chamber.stats, chamber.x
	#def drawHistX():



class WheelSectorHistograms:
	def __init__(self, name, chamber_class):
		self.name = name
		self.TH2F_sector_x = []
		self.TH2F_sector_y = []
		self.TH2F_sector_z = []
		self.TH2F_sector_phix = []
		self.TH2F_sector_phiy = []
		self.TH2F_sector_phiz = []
		for wheel in range(5):
			self.TH2F_sector_x.append([])
			self.TH2F_sector_y.append([])
			self.TH2F_sector_z.append([])
			self.TH2F_sector_phix.append([])
			self.TH2F_sector_phiy.append([])
			self.TH2F_sector_phiz.append([])
			for station in range(4):
				self.TH2F_sector_x[wheel].append( r.TH2F("{}_TH2F_sector_x_{}_{}".format(self.name, wheel-2,station+1),"x wheel {} station {}".format(wheel-2,station+1), 100, 0, 500000, 100, -.3,.3 ) )
				self.TH2F_sector_y[wheel].append( r.TH2F("{}_TH2F_sector_y_{}_{}".format(self.name, wheel-2,station+1),"y wheel {} station {}".format(wheel-2,station+1), 100, 0, 500000, 100, -.3,.3 ) )
				self.TH2F_sector_z[wheel].append( r.TH2F("{}_TH2F_sector_z_{}_{}".format(self.name, wheel-2,station+1),"z wheel {} station {}".format(wheel-2,station+1), 100, 0, 500000, 100, -.3,.3 ) )
				self.TH2F_sector_phix[wheel].append( r.TH2F("{}_TH2F_sector_phix_{}_{}".format(self.name, wheel-2,station+1),"#phi x wheel {} station {}".format(wheel-2,station+1), 100, 0, 500000, 100, -.3,.3 ) )
				self.TH2F_sector_phiy[wheel].append( r.TH2F("{}_TH2F_sector_phiy_{}_{}".format(self.name, wheel-2,station+1),"#phi ywheel {} station {}".format(wheel-2,station+1), 100, 0, 500000, 100, -.3,.3 ) )
				self.TH2F_sector_phiz[wheel].append( r.TH2F("{}_TH2F_sector_phiz_{}_{}".format(self.name, wheel-2,station+1),"#phi zwheel {} station {}".format(wheel-2,station+1), 100, 0, 500000, 100, -.3,.3 ) )

		for count, chamber in enumerate(chamber_class.chambers):
			#print chamber.wheel, chamber.station, chamber.sector, chamber.x
			self.TH2F_sector_x[chamber.wheel+2][chamber.station-1].Fill(float(chamber.stats), float(chamber.x))
			self.TH2F_sector_y[chamber.wheel+2][chamber.station-1].Fill(float(chamber.stats), float(chamber.y))
			self.TH2F_sector_z[chamber.wheel+2][chamber.station-1].Fill(float(chamber.stats), float(chamber.z))
			self.TH2F_sector_phix[chamber.wheel+2][chamber.station-1].Fill(float(chamber.stats), float(chamber.phix))
			self.TH2F_sector_phiy[chamber.wheel+2][chamber.station-1].Fill(float(chamber.stats), float(chamber.phiy))
			self.TH2F_sector_phiz[chamber.wheel+2][chamber.station-1].Fill(float(chamber.stats), float(chamber.phiz))




	def draw_hists(self):
		c4 = r.TCanvas()
		for wheel in range(5):
			for sector in range(4):
				self.TH2F_sector_x[wheel][sector].ProjectionY().Draw()
				c4.SaveAs("output_mc/{}_TH2F_sector_x_{}_{}.png".format(self.name,wheel-2,sector+1))
				self.TH2F_sector_y[wheel][sector].ProjectionY().Draw()
				c4.SaveAs("output_mc/{}_TH2F_sector_y_{}_{}.png".format(self.name,wheel-2,sector+1))
				self.TH2F_sector_z[wheel][sector].ProjectionY().Draw()
				c4.SaveAs("output_mc/{}_TH2F_sector_z_{}_{}.png".format(self.name,wheel-2,sector+1))
				self.TH2F_sector_phix[wheel][sector].ProjectionY().Draw()
				c4.SaveAs("output_mc/{}_TH2F_sector_phix_{}_{}.png".format(self.name,wheel-2,sector+1))
				self.TH2F_sector_phiy[wheel][sector].ProjectionY().Draw()
				c4.SaveAs("output_mc/{}_TH2F_sector_phiy_{}_{}.png".format(self.name,wheel-2,sector+1))
				self.TH2F_sector_phiz[wheel][sector].ProjectionY().Draw()
				c4.SaveAs("output_mc/{}_TH2F_sector_phiz_{}_{}.png".format(self.name,wheel-2,sector+1))

				#print self.TH2F_sector_x[wheel][sector].GetRMS()

	#def getRMSStats(self,wheel, sector):
	#	return self.TH2F_sector_x[wheel+2][sector-1].GetRMS(1)

	def getMeanStats(self,wheel, sector):
		return self.TH2F_sector_x[wheel+2][sector-1].GetMean(1)

	def getRMSX(self,wheel, sector):
		return self.TH2F_sector_x[wheel+2][sector-1].GetRMS(2), self.TH2F_sector_x[wheel+2][sector-1].GetRMSError(2)

	def getRMSY(self,wheel, sector):
		return self.TH2F_sector_y[wheel+2][sector-1].GetRMS(2), self.TH2F_sector_y[wheel+2][sector-1].GetRMSError(2)

	def getRMSZ(self,wheel, sector):
		return self.TH2F_sector_z[wheel+2][sector-1].GetRMS(2), self.TH2F_sector_z[wheel+2][sector-1].GetRMSError(2)

	def getRMSPHIX(self,wheel, sector):
		return self.TH2F_sector_phix[wheel+2][sector-1].GetRMS(2), self.TH2F_sector_phix[wheel+2][sector-1].GetRMSError(2)

	def getRMSPHIY(self,wheel, sector):
		return self.TH2F_sector_phiy[wheel+2][sector-1].GetRMS(2), self.TH2F_sector_phiy[wheel+2][sector-1].GetRMSError(2)

	def getRMSPHIZ(self,wheel, sector):
		return self.TH2F_sector_phiz[wheel+2][sector-1].GetRMS(2), self.TH2F_sector_phiz[wheel+2][sector-1].GetRMSError(2)

def make2dStatsPlots(hist_array, name, rms_range):
	#conv_gaussian =r.TF1("conv_gaussian","TMath::Sqrt(-[0]^2/x+[1]^2)",0,200000)
	conv_gaussian =r.TF1("conv_gaussian","TMath::Sqrt([0]/x+[1])",0,200000)
	conv_gaussian.SetParameters(1.0, .01)
	#conv_gaussian.SetParLimits(1, 0, 100)
	conv_gaussian.SetParLimits(1, .0000000000000001, 100)
	conv_gaussian.SetParLimits(0, .0000000000000001, 100)
	conv_gaussian.SetParNames("slope", "offset")
	
	TH2F_stats_v_rms = []
	TLine_cutoff = []
	color = 1
	for sector in range(4):
		color = 1
		TH2F_stats_v_rms.append([])
		TLine_cutoff.append([])
		for wheel in range(5):
			TH2F_stats_v_rms[sector].append( r.TH2F("TH2F_stats_v_rms_{}_{}_{}".format(name, wheel-2, sector+1), "TH2F_stats_v_rms_{}_{}_{}".format(name, wheel-2, sector+1), 100, 0, 200000, 100, 0, rms_range))
			#for hist in enumerate(hist_array):
			for count in range(len(hist_array)):
				fill_command = "TH2F_stats_v_rms[sector][wheel].Fill(hist_array[count].getMeanStats(wheel-2,sector+1),hist_array[count].getRMS{}(wheel-2,sector+1)[0])".format(name)
				exec(fill_command)
				exception_catch_rms = "rms_value = hist_array[count].getRMS{}(wheel-2,sector+1)[0]".format(name)
				exec(exception_catch_rms)
				if  rms_value > rms_range:
					print "out of range"


			TH2F_stats_v_rms[sector][wheel].SetMarkerStyle(8)
			TH2F_stats_v_rms[sector][wheel].SetMarkerColor(color)
			fit = TH2F_stats_v_rms[sector][wheel].Fit("conv_gaussian", "BSQ") 
			#TH2F_stats_v_rms[sector][wheel].Fit("expo", "Q") 
			cutoff = abs((TH2F_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(0)/TH2F_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(1)))
			rand_const = TH2F_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(0)
			sys_cons = TH2F_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(1)
			chi2 = TH2F_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetChisquare()
			#cov = fit.GetCovarianceMatrix()
			#print cov
			#Cut_error = math.sqrt(math.pow(cutoff,2)*(math.pow(cov(0,0)/rand_const,2) + math.pow(cov(1,1)/sys_cons,2) -2*cov(0,1)/(rand_const*sys_cons)  ))
			#print  "cuttoff for {} RMS /{}/{}: random: {} sys: {} cutoff: {}".format(name, wheel-2, sector+1, rand_const, sys_cons, cutoff)
			Cut_error = 0
			print  "{} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {}".format(name, wheel-2, sector+1, rand_const, sys_cons, cutoff, hist_array[1].getMeanStats(wheel-2,sector+1),Cut_error, chi2) 
			TLine_cutoff[sector].append(r.TLine(cutoff,0,cutoff,rms_range))
			TLine_cutoff[sector][wheel].SetLineColor(color)
			TH2F_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").SetLineColor(color)
			TH2F_stats_v_rms[sector][wheel].SetLineColor(color)
			color = color + 1
	
	
	for sector in range(4):
		legend =  r.TLegend(0.82,0.68,0.9,0.88)
		for wheel in range(5):
			if(wheel == 0):	
				TH2F_stats_v_rms[sector][wheel].Draw()
			else:
				TH2F_stats_v_rms[sector][wheel].Draw("same")
			TLine_cutoff[sector][wheel].Draw()
			legend.AddEntry(TH2F_stats_v_rms[sector][wheel], "{} {}".format( wheel -2, sector+1), "lep")
		legend.Draw()
		c1.SaveAs("output_mc/TH2F_stats_v_rms_{}_sector{}.png".format(name, sector+1))
		



	
hist_array = []

report_array = []

execfile("mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01_report.py")
example = ChamberInfo("test", reports, "mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01.xml")
#example.drawHist()
#report_array.append(example)

hist_array.append(WheelSectorHistograms("example", example))


#example2.draw_hists()

execfile("full_data.py")
full_data = ChamberInfo("full_data", reports, "full_data.xml")
stats_7_5_fb = full_data.totalMuons

#hist_array.append(WheelSectorHistograms("full_data", full_data))


execfile("full.py")
full = ChamberInfo("full", reports, "full.xml")
hist_array.append(WheelSectorHistograms("full", full))
#full.drawHist()
report_array.append(full)
hist_array[1].draw_hists()


execfile("half.py")
half = ChamberInfo("half", reports, "half.xml")
hist_array.append(WheelSectorHistograms("half", half))
#hist_array[1].draw_hists()
#half.drawHist()
report_array.append(half)


execfile("one_third.py")
one_third = ChamberInfo("one_third", reports, "one_third.xml")
#hist_array.append(WheelSectorHistograms("one_third", one_third))
#one_third.drawHist()
report_array.append(one_third)


execfile("one_sixth.py")
one_sixth = ChamberInfo("one_sixth", reports, "one_sixth.xml")
hist_array.append(WheelSectorHistograms("one_sixth", one_sixth))
#one_sixth.drawHist()
report_array.append(one_sixth)



execfile("super_small.py")
super_small = ChamberInfo("super_small", reports, "super_small.xml")
report_array.append(super_small)

#hist_array.append(WheelSectorHistograms("super_small", super_small))
super_small.drawHist()

execfile("superduper_small.py")
superduper_small = ChamberInfo("superduper_small", reports, "superduper_small.xml")
#superduper_small.drawHist()
report_array.append(superduper_small)

#hist_array.append(WheelSectorHistograms("superduper_small", superduper_small))

#print dir(hist_array[0])


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
TH1F_distance_histograms = []

for i in range(len(report_array)):
	#for j in range(len(report_array[i].chambers)):
	TH1F_distance_histograms.append(r.TH1F("distance_histograms_{}".format(i), "distance {}".format(report_array[i].name), 100, -.08,.08) )

	for j in range(len(report_array[i].chambers)):
		#print (report_array[i-1].chambers[j-1].stats+ .0)/(full_data.chambers[j].stats+.0)*7.5, report_array[i-1].chambers[j-1].x- full.chambers[j].x
		TH1F_distance_histograms[i].Fill(report_array[i].chambers[j].x- full.chambers[j].x )

	print report_array[i].totalMuons, TH1F_distance_histograms[i].GetRMS()
	TH1F_distance_histograms[i].Draw()
	c4.SaveAs("TH1F_distance_histograms_{}.png".format(i))


#def drawFunction(hist, name, rmsRange):
#	conv_gaussian =r.TF1("conv_gaussian","TMath::Sqrt([0]/x+[1])",0,200000)
#	conv_gaussian.SetParameters(1.0, .01)
#	#conv_gaussian.SetParLimits(1, 0, 100)
#	conv_gaussian.SetParLimits(1, .0000000000000001, 100)
#	conv_gaussian.SetParLimits(0, .0000000000000001, 100)
#	conv_gaussian.SetParNames("slope", "offset")
#
#	hist.SetMarkerStyle(8)
#
#	c3 = r.TCanvas()
#	hist.Fit("conv_gaussian","BSQ")
#	cutoff = abs((hist.GetFunction("conv_gaussian").GetParameter(0)/hist.GetFunction("conv_gaussian").GetParameter(1)))
#	cutoff2 = abs((hist.GetFunction("conv_gaussian").GetParameter(0)*2/hist.GetFunction("conv_gaussian").GetParameter(1)))
#	cutoff4 = abs((hist.GetFunction("conv_gaussian").GetParameter(0)*4/hist.GetFunction("conv_gaussian").GetParameter(1)))
#	cutoffE = abs((hist.GetFunction("conv_gaussian").GetParameter(0)*4/hist.GetFunction("conv_gaussian").GetParError(1)))
#
#	TL_cutoff = r.TLine(cutoff, 0, cutoff,   rmsRange)
#	TL_cutoff2 = r.TLine(cutoff2, 0, cutoff2,   rmsRange)
#	TL_cutoff4 = r.TLine(cutoff4, 0, cutoff4,   rmsRange)
#	TL_cutoffE = r.TLine(cutoffE, 0, cutoffE,   rmsRange)
#
#	TL_cutoff.SetLineColor(2)
#	TL_cutoff2.SetLineColor(3)
#	TL_cutoff4.SetLineColor(4)
#	TL_cutoffE.SetLineColor(5)
#	leg = r.TLegend(0.7,0.68,0.9,0.88)
#	leg.AddEntry(TL_cutoff, "#sigma_{rand} = #sigma_{sys}" ,"le")
#	leg.AddEntry(TL_cutoff2, "2 x #sigma_{rand} = #sigma_{sys}" , "le")
#	leg.AddEntry(TL_cutoff4, "4 x #sigma_{rand} = #sigma_{sys}" , "le")
#	leg.AddEntry(TL_cutoffE, "#sigma_{rand} = #sigma_{sys} Error" , "le")
#	hist.Draw()
#	leg.Draw()
#	TL_cutoff.Draw()
#	TL_cutoff2.Draw()
#	TL_cutoff4.Draw()
#	TL_cutoffE.Draw()
#	c3.SaveAs("output_mc/TH2F_{}_rms_DTs.png".format(name))
#	print "{} {} {} {} {}".format(name ,cutoff, cutoff2, cutoff4, cutoffE)
#
#
#drawFunction(TH2F_X_rms_DTs, "X",rmsRangeX)
#
#drawFunction(TH2F_Y_rms_DTs, "Y",rmsRangeY)
#
#drawFunction(TH2F_Z_rms_DTs, "Z",rmsRangeZ)
#
#drawFunction(TH2F_phiX_rms_DTs, "phiX",rmsRangePhiX)
#
#drawFunction(TH2F_phiY_rms_DTs, "phiY",rmsRangePhiY)
#
#
#drawFunction(TH2F_X_mean_DTs, "absmean_X",meanRangeX)
#drawFunction(TH2F_Y_mean_DTs, "absmean_Y",meanRangeY)
#drawFunction(TH2F_Z_mean_DTs, "absmean_Z",meanRangeZ)
#
#drawFunction(TH2F_PhiX_mean_DTs, "absmean_PhiX",meanRangePhiX)
#drawFunction(TH2F_PhiY_mean_DTs, "absmean_PhiY",meanRangePhiY)
#drawFunction(TH2F_PhiZ_mean_DTs, "absmean_PhiZ",meanRangePhiZ)
#
##drawFunction(TH2F_X_absmean_DTs, "absmean_x",.04)
#
##drawFunction(TH2F_X_mean_DTs, "mean_x",.01)
#		
#
#
#
#