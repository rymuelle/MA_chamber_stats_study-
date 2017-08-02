import ROOT as r 
import xml.etree.ElementTree as ET
import math
from array import array

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
		self.set_values(reports, root)

	def set_values(self,reports, root):
		for count,report in enumerate(reports):
			if report.postal_address[0] == "DT":
				#print report.postal_address[1],report.postal_address[2], report.postal_address[3]
				count = 0 
				for child in root.findall("./operation/*[@wheel='{}'][@station='{}'][@sector='{}']/../setposition".format(report.postal_address[1],report.postal_address[2], report.postal_address[3])):
					#print child.tag, child.attrib
					if(count == 0): 
						self.chambers.append(Chamber(report,child.attrib))
					count = count + 1
				
		#for count, chamber in enumerate(self.chambers):
		#   print chamber.detector, chamber.wheel, chamber.station, chamber.sector, chamber.stats, chamber.x


class WheelSectorHistograms:
	def __init__(self, name, chamber_class, ref_chambers, ref_lumi):
		self.name = name
		self.TH2F_sector_x = []
		self.TH2F_sector_y = []
		self.TH2F_sector_z = []
		self.TH2F_sector_phix = []
		self.TH2F_sector_phiy = []
		self.TH2F_sector_phiz = []
		for wheel in range(3):
			self.TH2F_sector_x.append([])
			self.TH2F_sector_y.append([])
			self.TH2F_sector_z.append([])
			self.TH2F_sector_phix.append([])
			self.TH2F_sector_phiy.append([])
			self.TH2F_sector_phiz.append([])
			for station in range(4):
				self.TH2F_sector_x[wheel].append( r.TH2F("{}_TH2F_sector_x_{}_{}".format(self.name, wheel,station+1),"x wheel {} station {}".format(wheel,station+1), 100, 0, ref_lumi*2, 100, -.3,.3 ) )
				self.TH2F_sector_y[wheel].append( r.TH2F("{}_TH2F_sector_y_{}_{}".format(self.name, wheel,station+1),"y wheel {} station {}".format(wheel,station+1), 100, 0, ref_lumi*2, 100, -.3,.3 ) )
				self.TH2F_sector_z[wheel].append( r.TH2F("{}_TH2F_sector_z_{}_{}".format(self.name, wheel,station+1),"z wheel {} station {}".format(wheel,station+1), 100, 0, ref_lumi*2, 100, -.3,.3 ) )
				self.TH2F_sector_phix[wheel].append( r.TH2F("{}_TH2F_sector_phix_{}_{}".format(self.name, wheel,station+1),"#phi x wheel {} station {}".format(wheel,station+1), 100, 0, ref_lumi*2, 100, -.02,.02 ) )
				self.TH2F_sector_phiy[wheel].append( r.TH2F("{}_TH2F_sector_phiy_{}_{}".format(self.name, wheel,station+1),"#phi ywheel {} station {}".format(wheel,station+1), 100, 0, ref_lumi*2, 100, -.02,.02 ) )
				self.TH2F_sector_phiz[wheel].append( r.TH2F("{}_TH2F_sector_phiz_{}_{}".format(self.name, wheel,station+1),"#phi zwheel {} station {}".format(wheel,station+1), 100, 0, ref_lumi*2, 100, -.02,.02 ) )

		for count, chamber in enumerate(chamber_class.chambers):
			#print ref_chambers.chambers[count].wheel, ref_chambers.chambers[count].station, chamber.wheel, chamber.station
			#print chamber.wheel, chamber.station, chamber.sector, chamber.x
			eqv_lumi = float(chamber.stats)/float(ref_chambers.chambers[count].stats)*ref_lumi
			self.TH2F_sector_x[abs(chamber.wheel)][chamber.station-1].Fill(eqv_lumi, float(chamber.x))
			self.TH2F_sector_y[abs(chamber.wheel)][chamber.station-1].Fill(eqv_lumi, float(chamber.y))
			self.TH2F_sector_z[abs(chamber.wheel)][chamber.station-1].Fill(eqv_lumi, float(chamber.z))
			self.TH2F_sector_phix[abs(chamber.wheel)][chamber.station-1].Fill(eqv_lumi, float(chamber.phix))
			self.TH2F_sector_phiy[abs(chamber.wheel)][chamber.station-1].Fill(eqv_lumi, float(chamber.phiy))
			self.TH2F_sector_phiz[abs(chamber.wheel)][chamber.station-1].Fill(eqv_lumi, float(chamber.phiz))




	def add(self, other_wsh):
		for wheel in range(3):
			for sector in range(4):
				self.TH2F_sector_x[wheel][sector].Add(other_wsh.TH2F_sector_x[wheel][sector])
				self.TH2F_sector_y[wheel][sector].Add(other_wsh.TH2F_sector_y[wheel][sector])
				self.TH2F_sector_z[wheel][sector].Add(other_wsh.TH2F_sector_z[wheel][sector])
				self.TH2F_sector_phix[wheel][sector].Add(other_wsh.TH2F_sector_phix[wheel][sector])
				self.TH2F_sector_phiy[wheel][sector].Add(other_wsh.TH2F_sector_phiy[wheel][sector])
				self.TH2F_sector_phiz[wheel][sector].Add(other_wsh.TH2F_sector_phiz[wheel][sector])
				
	def draw_hists(self):
		for wheel in range(3):
			for sector in range(4):
				self.TH2F_sector_x[wheel][sector].Draw()
				c1.SaveAs("output/{}_TH2F_sector_x_{}_{}.png".format(self.name,wheel,sector+1))
				self.TH2F_sector_y[wheel][sector].Draw()
				c1.SaveAs("output/{}_TH2F_sector_y_{}_{}.png".format(self.name,wheel,sector+1))
				self.TH2F_sector_z[wheel][sector].Draw()
				c1.SaveAs("output/{}_TH2F_sector_z_{}_{}.png".format(self.name,wheel,sector+1))
				self.TH2F_sector_phix[wheel][sector].Draw()
				c1.SaveAs("output/{}_TH2F_sector_phix_{}_{}.png".format(self.name,wheel,sector+1))
				self.TH2F_sector_phiy[wheel][sector].Draw()
				c1.SaveAs("output/{}_TH2F_sector_phiy_{}_{}.png".format(self.name,wheel,sector+1))
				self.TH2F_sector_phiz[wheel][sector].Draw()
				c1.SaveAs("output/{}_TH2F_sector_phiz_{}_{}.png".format(self.name,wheel,sector+1))

				#print self.TH2F_sector_x[wheel][sector].GetRMS()

	#def getRMSStats(self,wheel, sector):
	#   return self.TH2F_sector_x[wheel+2][sector-1].GetRMS(1)

	def getMedianofAbs(self, histogram):
		nq = 5
		xq = array('d', [0.] * nq)   # position where to compute the quantiles in [0,1]
		yq1 = array('d', [0.] * nq)  # array to contain the quantiles

		for i in xrange(nq):
			xq[i] = float(i + 1) / nq
		histogram.GetQuantiles(nq, yq1, xq)
		print "hi", yq1
		return  yq1[2]

	def getQuantilesAbs(self, histogram, nq):
		xq = array('d', [0.] * nq)   # position where to compute the quantiles in [0,1]
		yq1 = array('d', [0.] * nq)  # array to contain the quantiles

		for i in xrange(nq):
			xq[i] = float(i + 1) / nq
		histogram.GetQuantiles(nq, yq1, xq)
		#print "hi", yq1
		return  yq1


	def getMeanStats(self,wheel, sector):
		return self.TH2F_sector_x[wheel][sector-1].GetMean(1)

	def getMeanStatsError(self,wheel, sector):
		return self.TH2F_sector_x[wheel][sector-1].GetMeanError(1)

	def getRMSOutlierProtected(self,hist, count):
		yq = self.getQuantilesAbs(hist, count)
		temp_hist = hist
		#print temp_hist.GetRMS()
		temp_hist.GetXaxis().SetRangeUser(yq[1], yq[count-2])
		#print temp_hist.GetRMS()
		return temp_hist.GetRMS()

	def getRMSProtectedX(self,wheel, sector):
		return self.getRMSOutlierProtected(self.TH2F_sector_x[wheel][sector-1].ProjectionY(),10)

		#return self.getMedianofAbs(self.TH2F_sector_x[wheel][sector-1].ProjectionY()) 

	def getRMSProtectedY(self,wheel, sector):
		return self.getRMSOutlierProtected(self.TH2F_sector_y[wheel][sector-1].ProjectionY(),10)

	def getRMSProtectedZ(self,wheel, sector):
		return self.getRMSOutlierProtected(self.TH2F_sector_z[wheel][sector-1].ProjectionY(),10)

	def getRMSProtectedPHIX(self,wheel, sector):
		return self.getRMSOutlierProtected(self.TH2F_sector_phix[wheel][sector-1].ProjectionY(),10)

	def getRMSProtectedPHIY(self,wheel, sector):		
		return self.getRMSOutlierProtected(self.TH2F_sector_phiy[wheel][sector-1].ProjectionY(),10)

	def getRMSProtectedPHIZ(self,wheel, sector):
		return self.getRMSOutlierProtected(self.TH2F_sector_phiz[wheel][sector-1].ProjectionY(),10)

	def getRMSX(self,wheel, sector):
		return self.TH2F_sector_x[wheel][sector-1].GetRMS(2)

	def getRMSY(self,wheel, sector):
		return self.TH2F_sector_y[wheel][sector-1].GetRMS(2)

	def getRMSZ(self,wheel, sector):
		return self.TH2F_sector_z[wheel][sector-1].GetRMS(2)

	def getRMSPHIX(self,wheel, sector):
		return self.TH2F_sector_phix[wheel][sector-1].GetRMS(2)

	def getRMSPHIY(self,wheel, sector):
		return self.TH2F_sector_phiy[wheel][sector-1].GetRMS(2)

	def getRMSPHIZ(self,wheel, sector):
		return self.TH2F_sector_phiz[wheel][sector-1].GetRMSError(2)

	def getRMSXError(self,wheel, sector):
		return self.TH2F_sector_x[wheel][sector-1].GetRMSError(2)

	def getRMSYError(self,wheel, sector):
		return self.TH2F_sector_y[wheel][sector-1].GetRMSError(2)

	def getRMSZError(self,wheel, sector):
		return self.TH2F_sector_z[wheel][sector-1].GetRMSError(2)

	def getRMSPHIXError(self,wheel, sector):
		return self.TH2F_sector_phix[wheel][sector-1].GetRMSError(2)

	def getRMSPHIYError(self,wheel, sector):
		return self.TH2F_sector_phiy[wheel][sector-1].GetRMSError(2)

	def getRMSPHIZError(self,wheel, sector):
		return self.TH2F_sector_phiz[wheel][sector-1].GetRMSError(2)

def make2dStatsPlots(hist_array, name, rms_range, output):
	conv_gaussian =r.TF1("conv_gaussian","TMath::Sqrt([0]*10^-4/x+[1]*10^-4)",0,10)
	conv_gaussian.SetParameters(1.0, .01)
	conv_gaussian.SetParNames("slope", "offset")
	conv_gaussian.SetParLimits(1, .0000000000000001, 100)
	conv_gaussian.SetParLimits(0, .0000000000000001, 100)
	TGraph_cutoffs = r.TGraphErrors()
	colorArray = [1,2,3,4,6]
	TH2F_stats_v_rms = []
	TGraph_stats_v_rms = []
	TLine_cutoff = []
	fit = []
	for sector in range(4):
		color = 0
		TH2F_stats_v_rms.append([])
		TGraph_stats_v_rms.append([])
		fit.append([])
		for wheel in range(3):
			TGraph_stats_v_rms[sector].append (r.TGraphErrors())
			TH2F_stats_v_rms[sector].append( r.TH2F("TH2F_stats_v_rms_{}_{}_{}".format(name, wheel, sector+1), "TH2F_stats_v_rms_{}_{}_{}".format(name, wheel, sector+1), 100, 0, 200000, 100, 0, rms_range))

			#for hist in enumerate(hist_array):
			for count in range(len(hist_array)):
				#fill_command = "TH2F_stats_v_rms[sector][wheel].Fill(hist_array[count].getMeanStats(wheel,sector+1),hist_array[count].getRMS{}(wheel,sector+1))".format(name)
				stats, statsError = hist_array[count].getMeanStats(wheel,sector+1), hist_array[count].getMeanStatsError(wheel,sector+1)
				rms_command = "rms, rmsError = hist_array[count].getRMSProtected{}(wheel,sector+1), hist_array[count].getRMS{}Error(wheel,sector+1)".format(name,name)
				exec(rms_command)
				point_count = TGraph_stats_v_rms[sector][wheel].GetN()
				TGraph_stats_v_rms[sector][wheel].SetPoint(point_count, stats, rms)
				TGraph_stats_v_rms[sector][wheel].SetPointError(point_count, statsError, rmsError)
				
				
				#exception_catch_rms = "rms_value = hist_array[count].getRMS{}(wheel,sector+1)".format(name)
				#exec(exception_catch_rms)
				#if  rms_value > rms_range:
				#   print "out of range"


			TGraph_stats_v_rms[sector][wheel].SetMarkerStyle(8)
			TGraph_stats_v_rms[sector][wheel].SetMarkerColor(colorArray[color])
			fit[sector].append(TGraph_stats_v_rms[sector][wheel].Fit("conv_gaussian", "QS") )
			#cutoff = math.pow((TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(0)/TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(1)),2)
			#print "cuttoff for {} RMS /{}/{}: {}".format(name, wheel, sector+1, cutoff)
			#TLine_cutoff[sector].append(r.TLine(cutoff,0,cutoff,rms_range))
			#TLine_cutoff[sector][wheel].SetLineColor(colorArray[color])
			#TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").SetLineColor(colorArray[color])
			#TGraph_stats_v_rms[sector][wheel].SetLineColor(colorArray[color])
			color = color + 1
	
	multigraph = []
	for sector in range(4):
		color = 0
		multigraph.append(r.TMultiGraph())
		legend =  r.TLegend(0.82,0.68,0.9,0.88)
		TLine_cutoff.append([])
		for wheel in range(3):
			multigraph[sector].Add(TGraph_stats_v_rms[sector][wheel])
		for wheel in range(3):
			cutoff = math.pow((TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(0)/TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(1)),1)
			#print "cuttoff for {} RMS /{}/{}: {}".format(name, wheel, sector+1, cutoff)
			covMatrix =  fit[sector][wheel].GetCovarianceMatrix()
			#print covMatrix[0][0], covMatrix[1][0], covMatrix[1][1]
			sigma0, sigma10, sigma1 = covMatrix[0][0], covMatrix[1][0], covMatrix[1][1]
			par0, par1 = TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(0), TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(1)
			#print sigma0, sigma1, sigma10
			error = math.pow(abs(cutoff),1)*( math.pow(sigma0/par0,2) +math.pow(sigma1/par1,2) - 2*sigma10/(par0*par1) )
			if error > 0:
				error = math.sqrt(error)
			else : error = 0

			print "cuttoff for {} RMS /{}/{}: {} +/- {}".format(name, wheel, sector+1, cutoff, error)
			#print math.sqrt(covMatrix[0][0]), TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParError(0)
			#print math.sqrt(covMatrix[1][1]), TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParError(1)
			TLine_cutoff[sector].append(r.TLine(cutoff,0,cutoff,1))
			TLine_cutoff[sector][wheel].SetLineColor(colorArray[color])
			TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").SetLineColor(colorArray[color])
			TGraph_stats_v_rms[sector][wheel].SetLineColor(colorArray[color])
			point_count = TGraph_cutoffs.GetN()
			TGraph_cutoffs.SetPoint(point_count, cutoff, wheel)
			TGraph_cutoffs.SetPointError(point_count, error, 0)
			color = color + 1
			
			
		multigraph[sector].Draw("AP")
		for wheel in range(3):
			TLine_cutoff[sector][wheel].Draw()
			legend.AddEntry(TGraph_stats_v_rms[sector][wheel], "{} {}".format( wheel, sector+1), "lep")
		legend.Draw()
		c1.SaveAs("{}/TGraph_stats_v_rms_{}_sector{}.png".format(output,name, sector+1))
	TGraph_cutoffs.Draw()
	c1.SaveAs("{}/TGraph_cutoffs_{}.png".format(output,name, sector+1))
		



	
hist_array = []

#execfile("mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01_report.py")
#example = ChamberInfo("test", reports, "mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01.xml")

#hist_array.append(WheelSectorHistograms("example", example))

#example2.draw_hists()

execfile("full_data.py")
full_data = ChamberInfo("full_data", reports, "full_data.xml")
#stats_7_5_fb = full_data.totalMuons

execfile("full.py")
full = ChamberInfo("full", reports, "full.xml")
hist_array.append(WheelSectorHistograms("full", full, full_data, 7.5))

#execfile("half.py")
#half = ChamberInfo("half", reports, "half.xml")
##hist_array.append(WheelSectorHistograms("half", half))
##hist_array[1].draw_hists()
#
#execfile("one_third.py")
#one_third = ChamberInfo("one_third", reports, "one_third.xml")
##hist_array.append(WheelSectorHistograms("one_third", one_third))
#
#
#execfile("one_sixth.py")
#one_sixth = ChamberInfo("one_sixth", reports, "one_sixth.xml")
##hist_array.append(WheelSectorHistograms("one_sixth", one_sixth))
#
#
#
#execfile("super_small.py")
#super_small = ChamberInfo("super_small", reports, "super_small.xml")
##hist_array.append(WheelSectorHistograms("super_small", super_small))
#
#
#execfile("superduper_small.py")
#superduper_small = ChamberInfo("superduper_small", reports, "superduper_small.xml")
#hist_array.append(WheelSectorHistograms("superduper_small", superduper_small))


#fileArray = ["div_16_3", "div_16_2", "div_16_1", "div_2_1", "div_16_8", "div_16_7", "div_16_6", "div_16_5", "div_16_4", "div_4_2", "div_4_1", "div_2_4", "div_2_3", "div_2_2", "div_4_4", "div_4_3", "div_8_4", "div_8_3", "div_8_2", "div_8_1", "div_8_8", "div_8_7", "div_8_6", "div_8_5"]
fileArray = []
fileArray.append(["div_16_3", "div_16_2", "div_16_1", "div_16_8", "div_16_7", "div_16_6", "div_16_5", "div_16_4"])
fileArray.append(["div_8_4", "div_8_3", "div_8_2", "div_8_1", "div_8_8", "div_8_7", "div_8_6", "div_8_5"])
fileArray.append([  "div_4_2", "div_4_1",  "div_4_4", "div_4_3" ])
fileArray.append([  "div_2_1", "div_2_4", "div_2_3", "div_2_2" ])
#fileArray_8 = ["div_8_4", "div_8_3", "div_8_2", "div_8_1", "div_8_8", "div_8_7", "div_8_6", "div_8_5"]
#fileArray_4 = [  "div_4_2", "div_4_1",  "div_4_4", "div_4_3" ]
#fileArray_4 = [  "div_2_1", "div_2_4", "div_2_3", "div_2_2" ]

for l_array in fileArray:
	count = 0
	for file in l_array:
		print count
		execfile("{}.py".format(file))
		name = ChamberInfo(file, reports, "{}.xml".format(file))
		if count == 0:
			wsh =  WheelSectorHistograms(file, name, full_data, 7.5)
		else:
			wsh.add(WheelSectorHistograms(file, name, full_data, 7.5))
		count = count +1 
	
	hist_array.append(wsh)





#print dir(hist_array[0])


make2dStatsPlots(hist_array, "X", .1,"output_mc_2")
make2dStatsPlots(hist_array, "Y", .3,"output_mc_2")
make2dStatsPlots(hist_array, "Z", .3,"output_mc_2")
make2dStatsPlots(hist_array, "PHIX", .03,"output_mc_2")
make2dStatsPlots(hist_array, "PHIY", .014,"output_mc_2")
make2dStatsPlots(hist_array, "PHIZ", .002,"output_mc_2")
		


