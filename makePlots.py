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
		self.x = child['x']
		self.y = child['y']
		self.z = child['z']
		self.phix = child['phix']
		self.phiy = child['phiy']
		self.phiz = child['phiz']
		
		

class ChamberInfo:
	def __init__(self, name, reports, xml):
		self.name = name
		self.chambers = []
		tree = ET.ElementTree(file=xml)
		root = tree.getroot()
		self.TH1F_X = r.TH1F("TH1F_X_{}".format(name), ";x position (cm);  count", 100, -1, 1)
		self.totalMuons = 0
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
			 self.totalMuons = self.totalMuons + float(thing[1].stats)

	def drawHist(self):
		self.TH1F_X.Draw()
		print "stats: {} rms: {} mean: {}".format(self.totalMuons , self.TH1F_X.GetRMS(), self.TH1F_X.GetMean())
		print "{} \t {} \t {}".format(self.totalMuons , self.TH1F_X.GetRMS(), self.TH1F_X.GetMean())
		self.c2.SaveAs("TH1F_x_{}.png".format(self.name))


				
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
		for wheel in range(5):
			for sector in range(4):
				self.TH2F_sector_x[wheel][sector].Draw()
				c1.SaveAs("output_mc/{}_TH2F_sector_x_{}_{}.png".format(self.name,wheel-2,sector+1))
				self.TH2F_sector_y[wheel][sector].Draw()
				c1.SaveAs("output_mc/{}_TH2F_sector_y_{}_{}.png".format(self.name,wheel-2,sector+1))
				self.TH2F_sector_z[wheel][sector].Draw()
				c1.SaveAs("output_mc/{}_TH2F_sector_z_{}_{}.png".format(self.name,wheel-2,sector+1))
				self.TH2F_sector_phix[wheel][sector].Draw()
				c1.SaveAs("output_mc/{}_TH2F_sector_phix_{}_{}.png".format(self.name,wheel-2,sector+1))
				self.TH2F_sector_phiy[wheel][sector].Draw()
				c1.SaveAs("output_mc/{}_TH2F_sector_phiy_{}_{}.png".format(self.name,wheel-2,sector+1))
				self.TH2F_sector_phiz[wheel][sector].Draw()
				c1.SaveAs("output_mc/{}_TH2F_sector_phiz_{}_{}.png".format(self.name,wheel-2,sector+1))

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

execfile("mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01_report.py")
example = ChamberInfo("test", reports, "mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01.xml")
example.drawHist()

hist_array.append(WheelSectorHistograms("example", example))


#example2.draw_hists()

execfile("full_data.py")
full_data = ChamberInfo("full_data", reports, "full_data.xml")
#hist_array.append(WheelSectorHistograms("full_data", full_data))

execfile("full.py")
full = ChamberInfo("full", reports, "full.xml")
hist_array.append(WheelSectorHistograms("full", full))
full.drawHist()


execfile("half.py")
half = ChamberInfo("half", reports, "half.xml")
hist_array.append(WheelSectorHistograms("half", half))
#hist_array[1].draw_hists()
half.drawHist()

execfile("one_third.py")
one_third = ChamberInfo("one_third", reports, "one_third.xml")
#hist_array.append(WheelSectorHistograms("one_third", one_third))
one_third.drawHist()


execfile("one_sixth.py")
one_sixth = ChamberInfo("one_sixth", reports, "one_sixth.xml")
hist_array.append(WheelSectorHistograms("one_sixth", one_sixth))
one_sixth.drawHist()



execfile("super_small.py")
super_small = ChamberInfo("super_small", reports, "super_small.xml")

#hist_array.append(WheelSectorHistograms("super_small", super_small))
super_small.drawHist()

execfile("superduper_small.py")
superduper_small = ChamberInfo("superduper_small", reports, "superduper_small.xml")
superduper_small.drawHist()
#hist_array.append(WheelSectorHistograms("superduper_small", superduper_small))

#print dir(hist_array[0])


make2dStatsPlots(hist_array, "X", .1)
make2dStatsPlots(hist_array, "Y", .2)
make2dStatsPlots(hist_array, "Z", .3)
make2dStatsPlots(hist_array, "PHIX", .01)
make2dStatsPlots(hist_array, "PHIY", .014)
make2dStatsPlots(hist_array, "PHIZ", .002)
		



