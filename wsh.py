import ROOT as r 
import xml.etree.ElementTree as ET
import math
from array import array

#self.c2 = r.TCanvas("test")

r.gROOT.SetBatch(True)
#r.gStyle.SetOptStat(0)


def fitCut(hist, sigmas, opts):

	lower, upper = -1,1 #hist.GetMean()-sigmas*hist.GetRMS(), hist.GetMean()+sigmas*hist.GetRMS()
	mean, rms = hist.GetMean(), hist.GetRMS()
	entries = hist.GetEntries()
	max_val = hist.GetMaximum()
	cust_gauss = r.TF1("cust_gauss","gaus(0)", -10,10)
	cust_gauss.SetParameters( 10, mean, rms)
	cust_gauss.SetParNames("peak", "mean", "sigma")
	cust_gauss.SetParLimits(1, -mean*3,mean*3)
	cust_gauss.SetParLimits(0, max_val/2, entries)
	cust_gauss.SetParLimits(2, 0, rms*3)

	hist.Fit("cust_gauss",opts, "", lower, upper)
	#hist.Fit("cust_gauss",opts)


def reBinBool(th1f):
	rebin = False
	rms = th1f.GetRMS()
	th1f_range = th1f.GetXaxis().GetXmax() - th1f.GetXaxis().GetXmin()+.0
	nBins = th1f.GetXaxis().GetNbins() +.0
	bin_width = th1f_range/(nBins)
	goal_width = rms/4.0
	print th1f_range, bin_width, goal_width, rms
	if goal_width > bin_width:
		rebin = True
	return rebin

def reBinViaRMS(th1f):
	while(reBinBool(th1f)):
		th1f.Rebin(2)

	


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



class WheelSectorHistograms5:
	def __init__(self, name, chamber_class, ref_chambers, ref_lumi, sys_comparison):
		self.name = name 
		self.TH2F_sector_x = []
		self.TH2F_sector_x_offset = []
		self.TH2F_sector_y_offset = []
		self.TH2F_sector_z_offset = []
		self.TH2F_sector_phix_offset = []
		self.TH2F_sector_phiy_offset = []
		self.TH2F_sector_phiz_offset = []

		self.TH2F_sector_y = []
		self.TH2F_sector_z = []
		self.TH2F_sector_phix = []
		self.TH2F_sector_phiy = []
		self.TH2F_sector_phiz = []
		self.TH1F_sector_x = []
		self.TH1F_sector_y = []
		self.TH1F_sector_z = []
		self.TH1F_sector_phix = []
		self.TH1F_sector_phiy = []
		self.TH1F_sector_phiz = []
		self.TH2F_fit_x_sector_station = []
		self.TH2F_fit_y_sector_station = []
		self.TH2F_fit_z_sector_station = []
		self.TH2F_fit_phix_sector_station = []
		self.TH2F_fit_phiy_sector_station = []
		self.TH2F_fit_phiz_sector_station = []

		self.TH1F_sector_x_offset = []
		self.TH1F_sector_y_offset = []
		self.TH1F_sector_z_offset = []
		self.TH1F_sector_phix_offset = []
		self.TH1F_sector_phiy_offset = []
		self.TH1F_sector_phiz_offset = []
		#self.c2 = r.TCanvas()
		self.black_list = [(1,5), (2,5)  ]
		#self.black_list = []

		for station in range(4):
			self.TH2F_fit_x_sector_station.append( r.TH2F("{}TH2F_fit_x_sector_station_{}".format(self.name, station+1),"x fit position v sector, wheel for station {}; sector; wheel".format(station+1), 12, .5, 12.5, 5, -2, 2) )

		for wheel in range(5):
			self.TH2F_sector_x.append([])
			self.TH2F_sector_x_offset.append([])
			self.TH2F_sector_y_offset.append([])
			self.TH2F_sector_z_offset.append([])
			self.TH2F_sector_phix_offset.append([])
			self.TH2F_sector_phiy_offset.append([])
			self.TH2F_sector_phiz_offset.append([])
			self.TH2F_sector_y.append([])
			self.TH2F_sector_z.append([])
			self.TH2F_sector_phix.append([])
			self.TH2F_sector_phiy.append([])
			self.TH2F_sector_phiz.append([])
			for station in range(4):
				self.TH2F_sector_x[wheel].append( r.TH2F("{}_TH2F_sector_x_{}_{}".format(self.name, wheel-2,station+1),"x wheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 200, -.07,.07 ) )
				self.TH2F_sector_x_offset[wheel].append( r.TH2F("{}_TH2F_sector_x_offset_{}_{}".format(self.name, wheel-2,station+1),"x wheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 200, -.5,.5 ) )
				self.TH2F_sector_y_offset[wheel].append( r.TH2F("{}_TH2F_sector_y_offset_{}_{}".format(self.name, wheel-2,station+1),"x wheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 200, -.5,.5 ) )
				self.TH2F_sector_z_offset[wheel].append( r.TH2F("{}_TH2F_sector_z_offset_{}_{}".format(self.name, wheel-2,station+1),"x wheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 200, -.5,.5 ) )
				self.TH2F_sector_phix_offset[wheel].append( r.TH2F("{}_TH2F_sector_phix_offset_{}_{}".format(self.name, wheel-2,station+1),"x wheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 200, -.5,.5 ) )
				self.TH2F_sector_phiy_offset[wheel].append( r.TH2F("{}_TH2F_sector_phiy_offset_{}_{}".format(self.name, wheel-2,station+1),"x wheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 200, -.5,.5 ) )
				self.TH2F_sector_phiz_offset[wheel].append( r.TH2F("{}_TH2F_sector_phiz_offset_{}_{}".format(self.name, wheel-2,station+1),"x wheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 200, -.5,.5 ) )
				self.TH2F_sector_y[wheel].append( r.TH2F("{}_TH2F_sector_y_{}_{}".format(self.name, wheel-2,station+1),"y wheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 200, -.5,.5 ) )
				self.TH2F_sector_z[wheel].append( r.TH2F("{}_TH2F_sector_z_{}_{}".format(self.name, wheel-2,station+1),"z wheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 200, -.5,.5 ) )
				self.TH2F_sector_phix[wheel].append( r.TH2F("{}_TH2F_sector_phix_{}_{}".format(self.name, wheel-2,station+1),"#phi x wheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 200, -.02,.02 ) )
				self.TH2F_sector_phiy[wheel].append( r.TH2F("{}_TH2F_sector_phiy_{}_{}".format(self.name, wheel-2,station+1),"#phi ywheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 200, -.02,.02 ) )
				self.TH2F_sector_phiz[wheel].append( r.TH2F("{}_TH2F_sector_phiz_{}_{}".format(self.name, wheel-2,station+1),"#phi zwheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 200, -.01,.01 ) )

		for count, chamber in enumerate(chamber_class.chambers):
			fill = True
			for bad_chamber in self.black_list:
				if chamber.wheel == bad_chamber[0] and chamber.sector == bad_chamber[1]:
					#print "did not fill: ", chamber.wheel, chamber.sector , chamber.station
					fill = False
			if fill:
				comp_chamber = sys_comparison.chambers[count] 
				#print comp_chamber.wheel, comp_chamber.sector, comp_chamber.station
				eqv_lumi = float(chamber.stats)/float(ref_chambers.chambers[count].stats)*ref_lumi
				self.TH2F_sector_x[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.x) - float(comp_chamber.x))
				self.TH2F_sector_x[-chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.x)- float(comp_chamber.x) )

				#self.TH2F_sector_x[-chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.x)- float(comp_chamber.x) )
				self.TH2F_sector_x_offset[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(comp_chamber.x))
				self.TH2F_sector_y_offset[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(comp_chamber.y))
				self.TH2F_sector_z_offset[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(comp_chamber.z))
				self.TH2F_sector_phix_offset[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(comp_chamber.phix))
				self.TH2F_sector_phiy_offset[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(comp_chamber.phiy))
				self.TH2F_sector_phiz_offset[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(comp_chamber.phiz))

				#self.TH2F_sector_x_offset[-chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(comp_chamber.x))
				#self.TH2F_sector_x_offset[2-chamber.wheel][chamber.station-1].Fill(float(eqv_lumi), float(comp_chamber.x))
				#self.TH2F_sector_x[2-chamber.wheel][chamber.station-1].Fill(float(eqv_lumi), float(chamber.x))
				self.TH2F_sector_y[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.y) - float(comp_chamber.y))
				self.TH2F_sector_y[-chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.y) - float(comp_chamber.y))
				self.TH2F_sector_z[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.z) - float(comp_chamber.z))
				self.TH2F_sector_z[-chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.z) - float(comp_chamber.z))
				self.TH2F_sector_phix[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.phix) - float(comp_chamber.phix))
				self.TH2F_sector_phix[-chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.phix) - float(comp_chamber.phix))
				self.TH2F_sector_phiy[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.phiy) - float(comp_chamber.phiy))
				self.TH2F_sector_phiy[-chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.phiy) - float(comp_chamber.phiy))
				self.TH2F_sector_phiz[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.phiz) - float(comp_chamber.phiz))
				self.TH2F_sector_phiz[-chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.phiz) - float(comp_chamber.phiz))

				self.TH2F_fit_x_sector_station[chamber.station-1].SetBinContent(chamber.sector, chamber.wheel+3, float(chamber.x) - float(comp_chamber.x))
				#print float(chamber.x)
				#print "filled: ", chamber.wheel, chamber.sector , chamber.station

		for wheel in range(5):
			self.TH1F_sector_x.append([])
			self.TH1F_sector_y.append([])
			self.TH1F_sector_z.append([])
			self.TH1F_sector_phix.append([])
			self.TH1F_sector_phiy.append([])
			self.TH1F_sector_phiz.append([])

			self.TH1F_sector_x_offset.append([])
			self.TH1F_sector_y_offset.append([])
			self.TH1F_sector_z_offset.append([])
			self.TH1F_sector_phix_offset.append([])
			self.TH1F_sector_phiy_offset.append([])
			self.TH1F_sector_phiz_offset.append([])
			for station in range(4):
				self.TH1F_sector_x[wheel].append( self.TH2F_sector_x[wheel][station].ProjectionY() )
				self.TH1F_sector_x_offset[wheel].append( self.TH2F_sector_x_offset[wheel][station].ProjectionY() )
				self.TH1F_sector_x[wheel].append( self.TH2F_sector_x[wheel][station].ProjectionY() )
				self.TH1F_sector_y[wheel].append( self.TH2F_sector_y[wheel][station].ProjectionY() )
				self.TH1F_sector_z[wheel].append( self.TH2F_sector_z[wheel][station].ProjectionY() )
				self.TH1F_sector_phix[wheel].append( self.TH2F_sector_phix[wheel][station].ProjectionY() )
				self.TH1F_sector_phiy[wheel].append( self.TH2F_sector_phiy[wheel][station].ProjectionY() )
				self.TH1F_sector_phiz[wheel].append( self.TH2F_sector_phiz[wheel][station].ProjectionY() )
				self.TH1F_sector_y_offset[wheel].append( self.TH2F_sector_y_offset[wheel][station].ProjectionY() )
				self.TH1F_sector_z_offset[wheel].append( self.TH2F_sector_z_offset[wheel][station].ProjectionY() )
				self.TH1F_sector_phix_offset[wheel].append( self.TH2F_sector_phix_offset[wheel][station].ProjectionY() )
				self.TH1F_sector_phiy_offset[wheel].append( self.TH2F_sector_phiy_offset[wheel][station].ProjectionY() )
				self.TH1F_sector_phiz_offset[wheel].append( self.TH2F_sector_phiz_offset[wheel][station].ProjectionY() )

				




	def add(self, other_wsh):
		for wheel in range(5):
			for sector in range(4):
				self.TH2F_sector_x[wheel][sector].Add(other_wsh.TH2F_sector_x[wheel][sector])
				self.TH2F_sector_y[wheel][sector].Add(other_wsh.TH2F_sector_y[wheel][sector])
				self.TH2F_sector_z[wheel][sector].Add(other_wsh.TH2F_sector_z[wheel][sector])
				self.TH2F_sector_phix[wheel][sector].Add(other_wsh.TH2F_sector_phix[wheel][sector])
				self.TH2F_sector_phiy[wheel][sector].Add(other_wsh.TH2F_sector_phiy[wheel][sector])
				self.TH2F_sector_phiz[wheel][sector].Add(other_wsh.TH2F_sector_phiz[wheel][sector])

				
				self.TH1F_sector_x[wheel][sector].Add(other_wsh.TH1F_sector_x[wheel][sector])
				self.TH1F_sector_y[wheel][sector].Add(other_wsh.TH1F_sector_y[wheel][sector])
				self.TH1F_sector_z[wheel][sector].Add(other_wsh.TH1F_sector_z[wheel][sector])
				self.TH1F_sector_phix[wheel][sector].Add(other_wsh.TH1F_sector_phix[wheel][sector])
				self.TH1F_sector_phiy[wheel][sector].Add(other_wsh.TH1F_sector_phiy[wheel][sector])
				self.TH1F_sector_phiz[wheel][sector].Add(other_wsh.TH1F_sector_phiz[wheel][sector])


				
	def draw_hists(self, c1):
		for station in range(4):
			self.TH2F_fit_x_sector_station[station].Draw("colz TEXT")
			c1.SaveAs("output_mc_2/{}_TH2F_fit_x_sector_station_{}.png".format(self.name, station+1))
		temp_hist = self.TH2F_fit_x_sector_station[0].Clone()
		temp_hist.Add(self.TH2F_fit_x_sector_station[1])
		temp_hist.Add(self.TH2F_fit_x_sector_station[2])
		temp_hist.Add(self.TH2F_fit_x_sector_station[3])
		temp_hist.Draw("colz TEXT")
		c1.SaveAs("output_mc_2/{}_TH2F_fit_x_sector_added.png".format(self.name))






		#for wheel in range(5):
		#	for sector in range(4):
#
		#		fit_hist_x = self.TH2F_sector_x[wheel][sector].ProjectionY()
		#		fitCut(fit_hist_x, 1.5, "QC")
		#		fit_hist_x.Draw()
		#		self.c2.SaveAs("output_mc_2/{}_TH2F_sector_x_{}_{}.png".format(self.name,wheel-2,sector+1))
#
		#		fit_hist_y = self.TH2F_sector_y[wheel][sector].ProjectionY()
		#		fitCut(fit_hist_y, 1.5, "QC")
		#		fit_hist_y.Draw()
		#		self.c2.SaveAs("output_mc_2/{}_TH2F_sector_y_{}_{}.png".format(self.name,wheel-2,sector+1))
#
		#		fit_hist_z = self.TH2F_sector_z[wheel][sector].ProjectionY()
		#		fitCut(fit_hist_z, 1.5, "QC")
		#		fit_hist_z.Draw()
		#		self.c2.SaveAs("output_mc_2/{}_TH2F_sector_z_{}_{}.png".format(self.name,wheel-2,sector+1))
#
		#		fit_hist_phix = self.TH2F_sector_phix[wheel][sector].ProjectionY()
		#		fitCut(fit_hist_phix, 1.5, "QC")
		#		fit_hist_phix.Draw()
		#		self.c2.SaveAs("output_mc_2/{}_TH2F_sector_phix_{}_{}.png".format(self.name,wheel-2,sector+1))
#
		#		fit_hist_phiy = self.TH2F_sector_phiy[wheel][sector].ProjectionY()
		#		fitCut(fit_hist_phiy, 1.5, "QC")
		#		fit_hist_phiy.Draw()
		#		self.c2.SaveAs("output_mc_2/{}_TH2F_sector_phiy_{}_{}.png".format(self.name,wheel-2,sector+1))
#
		#		fit_hist_phiz = self.TH2F_sector_phiz[wheel][sector].ProjectionY()
		#		fitCut(fit_hist_phiz, 1.5, "QC")
		#		fit_hist_phiz.Draw()
		#		self.c2.SaveAs("output_mc_2/{}_TH2F_sector_phiz_{}_{}.png".format(self.name,wheel-2,sector+1))

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


	def getMeanStats(self,wheel, sector):
		return self.TH2F_sector_x[wheel+2][sector-1].GetMean(1)

	def getMeanStatsError(self,wheel, sector):
		return self.TH2F_sector_x[wheel+2][sector-1].GetMeanError(1)


	def returnFitProtectedRMS(self, hist, sector, sigmas):
		reBinViaRMS(hist)
		fitCut(hist,1.5, "QC" )
		rms = hist.GetFunction("cust_gauss").GetParameter(2)
		rmsError = hist.GetFunction("cust_gauss").GetParError(2)
		mean = hist.GetFunction("cust_gauss").GetParameter(1)
		hist.GetXaxis().SetRangeUser(mean - 3.5*rms, mean + 3.5*rms)
		rms = hist.GetRMS()
		rmsError = hist.GetRMSError()
		return rms, rmsError


	def getFitX(self,wheel, sector, sigmas, canvas):
		
		rms, rmsError = self.returnFitProtectedRMS(self.TH1F_sector_x[wheel+2][sector-1], sector, sigmas)
		self.TH1F_sector_x[wheel+2][sector-1].Draw()
		canvas.SaveAs("output_mc_2/{}_TH2F_sector_x_{}_{}.png".format(self.name,wheel,sector))
		rms_offset, rmsError_offset = self.returnFitProtectedRMS(self.TH1F_sector_x_offset[wheel+2][sector-1], sector, sigmas)
		rms_offset2, rmsError_offset2 = self.returnFitProtectedRMS(self.TH1F_sector_x_offset[-wheel+2][sector-1], sector, sigmas)
		rms_offset = (rms_offset2 + rms_offset)/2
		return  rms, rmsError, self.TH1F_sector_x[wheel+2][sector-1].GetFunction("cust_gauss").GetChisquare(), rms_offset
		#reBinViaRMS(self.TH1F_sector_x[wheel+2][sector-1])
		##self.TH1F_sector_x[wheel+2][sector-1].Fit("cust_gauss", "QC")
		#fitCut(self.TH1F_sector_x[wheel+2][sector-1],1.5, "QC" )
		#self.TH1F_sector_x[wheel+2][sector-1].Draw()
		#canvas.SaveAs("output_mc_2/{}_TH2F_sector_x_{}_{}.png".format(self.name,wheel,sector))
		#rms = self.TH1F_sector_x[wheel+2][sector-1].GetFunction("cust_gauss").GetParameter(2)
		#mean = self.TH1F_sector_x[wheel+2][sector-1].GetFunction("cust_gauss").GetParameter(1)
		#self.TH1F_sector_x[wheel+2][sector-1].GetXaxis().SetRangeUser(mean - 2.5*rms, mean + 2.5*rms)
		#self.TH1F_sector_x[wheel+2][sector-1].Draw()
		#canvas.SaveAs("output_mc_2/{}_TH2F_sector_x_cut_{}_{}.png".format(self.name,wheel,sector))	
		#rms = self.TH1F_sector_x[wheel+2][sector-1].GetRMS()
		#rmsError = self.TH1F_sector_x[wheel+2][sector-1].GetRMSError()
		#return  rms, rmsError, self.TH1F_sector_x[wheel+2][sector-1].GetFunction("cust_gauss").GetChisquare()

	def getFitY(self,wheel, sector, sigmas, canvas):
		rms, rmsError = self.returnFitProtectedRMS(self.TH1F_sector_y[wheel+2][sector-1], sector, sigmas)
		self.TH1F_sector_y[wheel+2][sector-1].Draw()
		canvas.SaveAs("output_mc_2/{}_TH2F_sector_y_{}_{}.png".format(self.name,wheel,sector))
		rms_offset, rmsError_offset = self.returnFitProtectedRMS(self.TH1F_sector_y_offset[wheel+2][sector-1], sector, sigmas)
		rms_offset2, rmsError_offset2 = self.returnFitProtectedRMS(self.TH1F_sector_y_offset[-wheel+2][sector-1], sector, sigmas)
		rms_offset = (rms_offset2 + rms_offset)/2
		return  rms, rmsError, self.TH1F_sector_y[wheel+2][sector-1].GetFunction("cust_gauss").GetChisquare(), rms_offset
		#reBinViaRMS(self.TH1F_sector_y[wheel+2][sector-1])
		##self.TH1F_sector_y[wheel+2][sector-1].Fit("cust_gauss", "QC")
		#fitCut(self.TH1F_sector_y[wheel+2][sector-1],1.5, "QC" )
		#self.TH1F_sector_y[wheel+2][sector-1].Draw()
		#canvas.SaveAs("output_mc_2/{}_TH2F_sector_y_{}_{}.png".format(self.name,wheel,sector))
		##print "chi2: ", self.TH1F_sector_y[wheel+2][sector-1].GetFunction("cust_gauss").GetChisquare()
		#return self.TH1F_sector_y[wheel+2][sector-1].GetFunction("cust_gauss").GetParameter(2), self.TH1F_sector_y[wheel+2][sector-1].GetFunction("cust_gauss").GetParError(2), self.TH1F_sector_y[wheel+2][sector-1].GetFunction("cust_gauss").GetChisquare()

	def getFitZ(self,wheel, sector, sigmas, canvas):
		rms, rmsError = self.returnFitProtectedRMS(self.TH1F_sector_z[wheel+2][sector-1], sector, sigmas)
		self.TH1F_sector_z[wheel+2][sector-1].Draw()
		canvas.SaveAs("output_mc_2/{}_TH2F_sector_z_{}_{}.png".format(self.name,wheel,sector))
		rms_offset, rmsError_offset = self.returnFitProtectedRMS(self.TH1F_sector_z_offset[wheel+2][sector-1], sector, sigmas)
		rms_offset2, rmsError_offset2 = self.returnFitProtectedRMS(self.TH1F_sector_z_offset[-wheel+2][sector-1], sector, sigmas)
		rms_offset = (rms_offset2 + rms_offset)/2
		return  rms, rmsError, self.TH1F_sector_z[wheel+2][sector-1].GetFunction("cust_gauss").GetChisquare(), rms_offset

	def getFitPHIX(self,wheel, sector, sigmas, canvas):
		rms, rmsError = self.returnFitProtectedRMS(self.TH1F_sector_phix[wheel+2][sector-1], sector, sigmas)
		self.TH1F_sector_phix[wheel+2][sector-1].Draw()
		canvas.SaveAs("output_mc_2/{}_TH2F_sector_phix_{}_{}.png".format(self.name,wheel,sector))
		rms_offset, rmsError_offset = self.returnFitProtectedRMS(self.TH1F_sector_phix_offset[wheel+2][sector-1], sector, sigmas)
		rms_offset2, rmsError_offset2 = self.returnFitProtectedRMS(self.TH1F_sector_phix_offset[-wheel+2][sector-1], sector, sigmas)
		rms_offset = (rms_offset2 + rms_offset)/2
		return  rms, rmsError, self.TH1F_sector_phix[wheel+2][sector-1].GetFunction("cust_gauss").GetChisquare(), rms_offset

	def getFitPHIY(self,wheel, sector, sigmas, canvas):
		rms, rmsError = self.returnFitProtectedRMS(self.TH1F_sector_phiy[wheel+2][sector-1], sector, sigmas)
		self.TH1F_sector_phiy[wheel+2][sector-1].Draw()
		canvas.SaveAs("output_mc_2/{}_TH2F_sector_phiy_{}_{}.png".format(self.name,wheel,sector))
		rms_offset, rmsError_offset = self.returnFitProtectedRMS(self.TH1F_sector_phiy_offset[wheel+2][sector-1], sector, sigmas)
		rms_offset2, rmsError_offset2 = self.returnFitProtectedRMS(self.TH1F_sector_phiy_offset[-wheel+2][sector-1], sector, sigmas)
		rms_offset = (rms_offset2 + rms_offset)/2
		return  rms, rmsError, self.TH1F_sector_phiy[wheel+2][sector-1].GetFunction("cust_gauss").GetChisquare(), rms_offset

	def getFitPHIZ(self,wheel, sector, sigmas, canvas):
		rms, rmsError = self.returnFitProtectedRMS(self.TH1F_sector_phiz[wheel+2][sector-1], sector, sigmas)
		self.TH1F_sector_phiz[wheel+2][sector-1].Draw()
		canvas.SaveAs("output_mc_2/{}_TH2F_sector_phiZ_{}_{}.png".format(self.name,wheel,sector))
		rms_offset, rmsError_offset = self.returnFitProtectedRMS(self.TH1F_sector_phiz_offset[wheel+2][sector-1], sector, sigmas)
		rms_offset2, rmsError_offset2 = self.returnFitProtectedRMS(self.TH1F_sector_phiz_offset[-wheel+2][sector-1], sector, sigmas)
		rms_offset = (rms_offset2 + rms_offset)/2
		return  rms, rmsError, self.TH1F_sector_phiz[wheel+2][sector-1].GetFunction("cust_gauss").GetChisquare(), rms_offset

	def getRMSX(self,wheel, sector):
		return self.TH2F_sector_x[wheel+2][sector-1].GetRMS(2)

		#return self.getMedianofAbs(self.TH2F_sector_x[wheel+2][sector-1].ProjectionY()) 

	def getRMSY(self,wheel, sector):
		return self.TH2F_sector_y[wheel+2][sector-1].GetRMS(2)
		#return self.getMedianofAbs(self.TH2F_sector_y[wheel+2][sector-1].ProjectionY()) 

	def getRMSZ(self,wheel, sector):
		return self.TH2F_sector_z[wheel+2][sector-1].GetRMS(2)
		#return self.getMedianofAbs(self.TH2F_sector_z[wheel+2][sector-1].ProjectionY()) 

	def getRMSPHIX(self,wheel, sector):
		return self.TH2F_sector_phix[wheel+2][sector-1].GetRMS(2)
		#return self.getMedianofAbs(self.TH2F_sector_phix[wheel+2][sector-1].ProjectionY()) 

	def getRMSPHIY(self,wheel, sector):
		return self.TH2F_sector_phiy[wheel+2][sector-1].GetRMS(2)
		#return self.getMedianofAbs(self.TH2F_sector_phiy[wheel+2][sector-1].ProjectionY()) 

	def getRMSPHIZ(self,wheel, sector):
		return self.TH2F_sector_phiz[wheel+2][sector-1].GetRMS(2)
		#return self.getMedianofAbs(self.TH2F_sector_phiz[wheel+2][sector-1].ProjectionY()) 


	def getRMSXError(self,wheel, sector):
		return self.TH2F_sector_x[wheel+2][sector-1].GetRMSError(2)

	def getRMSYError(self,wheel, sector):
		return self.TH2F_sector_y[wheel+2][sector-1].GetRMSError(2)

	def getRMSZError(self,wheel, sector):
		return self.TH2F_sector_z[wheel+2][sector-1].GetRMSError(2)

	def getRMSPHIXError(self,wheel, sector):
		return self.TH2F_sector_phix[wheel+2][sector-1].GetRMSError(2)

	def getRMSPHIYError(self,wheel, sector):
		return self.TH2F_sector_phiy[wheel+2][sector-1].GetRMSError(2)

	def getRMSPHIZError(self,wheel, sector):
		return self.TH2F_sector_phiz[wheel+2][sector-1].GetRMSError(2)

