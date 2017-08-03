import ROOT as r 
import xml.etree.ElementTree as ET
import math
from array import array

c1 = r.TCanvas()

r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)


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
			for station in range(4):
				self.TH2F_sector_x[wheel].append( r.TH2F("{}_TH2F_sector_x_{}_{}".format(self.name, wheel,station+1),"x wheel {} station {}".format(wheel,station+1), 100, 0, ref_lumi*5, 100, -.3,.3 ) )
				self.TH2F_sector_y[wheel].append( r.TH2F("{}_TH2F_sector_y_{}_{}".format(self.name, wheel,station+1),"y wheel {} station {}".format(wheel,station+1), 100, 0, ref_lumi*5, 100, -.3,.3 ) )
				self.TH2F_sector_z[wheel].append( r.TH2F("{}_TH2F_sector_z_{}_{}".format(self.name, wheel,station+1),"z wheel {} station {}".format(wheel,station+1), 100, 0, ref_lumi*5, 100, -.3,.3 ) )		

		for wheel in range(5):
					self.TH2F_sector_phix.append([])
					self.TH2F_sector_phiy.append([])
					self.TH2F_sector_phiz.append([])
					for station in range(4):
						self.TH2F_sector_phix[wheel].append( r.TH2F("{}_TH2F_sector_phix_{}_{}".format(self.name, wheel-2,station+1),"#phi x wheel {} station {}".format(wheel-2,station+1), 100, 0, 200000, 100, -.3,.3 ) )
						self.TH2F_sector_phiy[wheel].append( r.TH2F("{}_TH2F_sector_phiy_{}_{}".format(self.name, wheel-2,station+1),"#phi ywheel {} station {}".format(wheel-2,station+1), 100, 0, 200000, 100, -.3,.3 ) )
						self.TH2F_sector_phiz[wheel].append( r.TH2F("{}_TH2F_sector_phiz_{}_{}".format(self.name, wheel-2,station+1),"#phi zwheel {} station {}".format(wheel-2,station+1), 100, 0, 200000, 100, -.3,.3 ) )

		for count, chamber in enumerate(chamber_class.chambers):
			#print ref_chambers.chambers[count].wheel, ref_chambers.chambers[count].station, chamber.wheel, chamber.station
			#print chamber.wheel, chamber.station, chamber.sector, chamber.x
			eqv_lumi = float(chamber.stats)/float(ref_chambers.chambers[count].stats)*ref_lumi
			self.TH2F_sector_x[abs(chamber.wheel)][chamber.station-1].Fill(eqv_lumi, float(chamber.x))
			self.TH2F_sector_y[abs(chamber.wheel)][chamber.station-1].Fill(eqv_lumi, float(chamber.y))
			self.TH2F_sector_z[abs(chamber.wheel)][chamber.station-1].Fill(eqv_lumi, float(chamber.z))
			self.TH2F_sector_phix[chamber.wheel+2][chamber.station-1].Fill(chamber.stats, float(chamber.phix))
			self.TH2F_sector_phiy[chamber.wheel+2][chamber.station-1].Fill(chamber.stats, float(chamber.phiy))
			self.TH2F_sector_phiz[chamber.wheel+2][chamber.station-1].Fill(chamber.stats, float(chamber.phiz))




	def add(self, other_wsh):
		for wheel in range(3):
			for sector in range(4):
				self.TH2F_sector_x[wheel][sector].Add(other_wsh.TH2F_sector_x[wheel][sector])
				self.TH2F_sector_y[wheel][sector].Add(other_wsh.TH2F_sector_y[wheel][sector])
				self.TH2F_sector_z[wheel][sector].Add(other_wsh.TH2F_sector_z[wheel][sector])
		for wheel in range(5):
			for sector in range(4):
				self.TH2F_sector_phix[wheel][sector].Add(other_wsh.TH2F_sector_phix[wheel][sector])
				self.TH2F_sector_phiy[wheel][sector].Add(other_wsh.TH2F_sector_phiy[wheel][sector])
				self.TH2F_sector_phiz[wheel][sector].Add(other_wsh.TH2F_sector_phiz[wheel][sector])
				
				
	def draw_hists(self):
		for wheel in range(3):
			for sector in range(4):
				self.TH2F_sector_x[wheel][sector].Draw()
				c1.SaveAs("output_mc_2/{}_TH2F_sector_x_{}_{}.png".format(self.name,wheel,sector+1))
				self.TH2F_sector_y[wheel][sector].Draw()
				c1.SaveAs("output_mc_2/{}_TH2F_sector_y_{}_{}.png".format(self.name,wheel,sector+1))
				self.TH2F_sector_z[wheel][sector].Draw()
				c1.SaveAs("output_mc_2/{}_TH2F_sector_z_{}_{}.png".format(self.name,wheel,sector+1))
		for wheel in range(5):
			for sector in range(4):
				self.TH2F_sector_phix[wheel][sector].Draw()
				c1.SaveAs("output_mc_2/{}_TH2F_sector_phix_{}_{}.png".format(self.name,wheel-2,sector+1))
				self.TH2F_sector_phiy[wheel][sector].Draw()
				c1.SaveAs("output_mc_2/{}_TH2F_sector_phiy_{}_{}.png".format(self.name,wheel-2,sector+1))
				self.TH2F_sector_phiz[wheel][sector].Draw()
				c1.SaveAs("output_mc_2/{}_TH2F_sector_phiz_{}_{}.png".format(self.name,wheel-2,sector+1))



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

	def getRMSOutlierProtectedError(self,hist, count):
		yq = self.getQuantilesAbs(hist, count)
		temp_hist = hist
		#print temp_hist.GetRMS()
		temp_hist.GetXaxis().SetRangeUser(yq[1], yq[count-2])
		#print temp_hist.GetRMS()
		return temp_hist.GetRMSError()

	def getRMSProtectedX(self,wheel, sector):
		return self.getRMSOutlierProtected(self.TH2F_sector_x[wheel][sector-1].ProjectionY(),10)

		#return self.getMedianofAbs(self.TH2F_sector_x[wheel][sector-1].ProjectionY()) 

	def getRMSProtectedY(self,wheel, sector):
		return self.getRMSOutlierProtected(self.TH2F_sector_y[wheel][sector-1].ProjectionY(),10)

	def getRMSProtectedZ(self,wheel, sector):
		return self.getRMSOutlierProtected(self.TH2F_sector_z[wheel][sector-1].ProjectionY(),10)

	def getRMSProtectedErrorX(self,wheel, sector):
		return self.getRMSOutlierProtectedError(self.TH2F_sector_x[wheel][sector-1].ProjectionY(),10)

		#return self.getMedianofAbs(self.TH2F_sector_x[wheel][sector-1].ProjectionY()) 

	def getRMSProtectedErrorY(self,wheel, sector):
		return self.getRMSOutlierProtectedError(self.TH2F_sector_y[wheel][sector-1].ProjectionY(),10)

	def getRMSProtectedErrorZ(self,wheel, sector):
		return self.getRMSOutlierProtectedError(self.TH2F_sector_z[wheel][sector-1].ProjectionY(),10)

	def getRMSProtectedErrorPHIX(self,wheel, sector):
		return self.getRMSOutlierProtectedError(self.TH2F_sector_phix[wheel+2][sector-1].ProjectionY(),10)

	def getRMSProtectedErrorPHIY(self,wheel, sector):		
		return self.getRMSOutlierProtectedError(self.TH2F_sector_phiy[wheel+2][sector-1].ProjectionY(),10)

	def getRMSProtectedErrorPHIZ(self,wheel, sector):
		return self.getRMSOutlierProtectedError(self.TH2F_sector_phiz[wheel+2][sector-1].ProjectionY(),10)

	def getRMSX(self,wheel, sector):
		return self.TH2F_sector_x[wheel][sector-1].GetRMS(2)

	def getRMSY(self,wheel, sector):
		return self.TH2F_sector_y[wheel][sector-1].GetRMS(2)

	def getRMSZ(self,wheel, sector):
		return self.TH2F_sector_z[wheel][sector-1].GetRMS(2)

	def getRMSPHIX(self,wheel, sector):
		return self.TH2F_sector_phix[wheel+2][sector-1].GetRMS(2)

	def getRMSPHIY(self,wheel, sector):
		return self.TH2F_sector_phiy[wheel+2][sector-1].GetRMS(2)

	def getRMSPHIZ(self,wheel, sector):
		return self.TH2F_sector_phiz[wheel+2][sector-1].GetRMSError(2)

	def getRMSXError(self,wheel, sector):
		return self.TH2F_sector_x[wheel][sector-1].GetRMSError(2)

	def getRMSYError(self,wheel, sector):
		return self.TH2F_sector_y[wheel][sector-1].GetRMSError(2)

	def getRMSZError(self,wheel, sector):
		return self.TH2F_sector_z[wheel][sector-1].GetRMSError(2)

	def getRMSPHIXError(self,wheel, sector):
		return self.TH2F_sector_phix[wheel+2][sector-1].GetRMSError(2)

	def getRMSPHIYError(self,wheel, sector):
		return self.TH2F_sector_phiy[wheel+2][sector-1].GetRMSError(2)

	def getRMSPHIZError(self,wheel, sector):
		return self.TH2F_sector_phiz[wheel+2][sector-1].GetRMSError(2)


class WheelSectorHistograms5:
	def __init__(self, name, chamber_class, ref_chambers, ref_lumi):
		self.name = name + "5"
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
				self.TH2F_sector_x[wheel].append( r.TH2F("{}_TH2F_sector_x_{}_{}".format(self.name, wheel-2,station+1),"x wheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 100, -.5,.5 ) )
				self.TH2F_sector_y[wheel].append( r.TH2F("{}_TH2F_sector_y_{}_{}".format(self.name, wheel-2,station+1),"y wheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 100, -.5,.5 ) )
				self.TH2F_sector_z[wheel].append( r.TH2F("{}_TH2F_sector_z_{}_{}".format(self.name, wheel-2,station+1),"z wheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 100, -.5,.5 ) )
				self.TH2F_sector_phix[wheel].append( r.TH2F("{}_TH2F_sector_phix_{}_{}".format(self.name, wheel-2,station+1),"#phi x wheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 100, -.02,.02 ) )
				self.TH2F_sector_phiy[wheel].append( r.TH2F("{}_TH2F_sector_phiy_{}_{}".format(self.name, wheel-2,station+1),"#phi ywheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 100, -.02,.02 ) )
				self.TH2F_sector_phiz[wheel].append( r.TH2F("{}_TH2F_sector_phiz_{}_{}".format(self.name, wheel-2,station+1),"#phi zwheel {} station {}".format(wheel-2,station+1), 100, 0, ref_lumi*5, 100, -.02,.02 ) )

		for count, chamber in enumerate(chamber_class.chambers):
			#print chamber.wheel, chamber.station, chamber.sector, chamber.x
			eqv_lumi = float(chamber.stats)/float(ref_chambers.chambers[count].stats)*ref_lumi
			self.TH2F_sector_x[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.x))
			self.TH2F_sector_y[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.y))
			self.TH2F_sector_z[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.z))
			self.TH2F_sector_phix[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.phix))
			self.TH2F_sector_phiy[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.phiy))
			self.TH2F_sector_phiz[chamber.wheel+2][chamber.station-1].Fill(float(eqv_lumi), float(chamber.phiz))




	def add(self, other_wsh):
		for wheel in range(5):
			for sector in range(4):
				self.TH2F_sector_x[wheel][sector].Add(other_wsh.TH2F_sector_x[wheel][sector])
				self.TH2F_sector_y[wheel][sector].Add(other_wsh.TH2F_sector_y[wheel][sector])
				self.TH2F_sector_z[wheel][sector].Add(other_wsh.TH2F_sector_z[wheel][sector])
				self.TH2F_sector_phix[wheel][sector].Add(other_wsh.TH2F_sector_phix[wheel][sector])
				self.TH2F_sector_phiy[wheel][sector].Add(other_wsh.TH2F_sector_phiy[wheel][sector])
				self.TH2F_sector_phiz[wheel][sector].Add(other_wsh.TH2F_sector_phiz[wheel][sector])
				
	def draw_hists(self):
		for wheel in range(5):
			for sector in range(4):

				fit_hist_x = self.TH2F_sector_x[wheel][sector].ProjectionY()
				fitCut(fit_hist_x, 1.5, "QC")
				fit_hist_x.Draw()
				c1.SaveAs("output_mc_2/{}_TH2F_sector_x_{}_{}.png".format(self.name,wheel-2,sector+1))

				fit_hist_y = self.TH2F_sector_y[wheel][sector].ProjectionY()
				fitCut(fit_hist_y, 1.5, "QC")
				fit_hist_y.Draw()
				c1.SaveAs("output_mc_2/{}_TH2F_sector_y_{}_{}.png".format(self.name,wheel-2,sector+1))

				fit_hist_z = self.TH2F_sector_z[wheel][sector].ProjectionY()
				fitCut(fit_hist_z, 1.5, "QC")
				fit_hist_z.Draw()
				c1.SaveAs("output_mc_2/{}_TH2F_sector_z_{}_{}.png".format(self.name,wheel-2,sector+1))

				fit_hist_phix = self.TH2F_sector_phix[wheel][sector].ProjectionY()
				fitCut(fit_hist_phix, 1.5, "QC")
				fit_hist_phix.Draw()
				c1.SaveAs("output_mc_2/{}_TH2F_sector_phix_{}_{}.png".format(self.name,wheel-2,sector+1))

				fit_hist_phiy = self.TH2F_sector_phiy[wheel][sector].ProjectionY()
				fitCut(fit_hist_phiy, 1.5, "QC")
				fit_hist_phiy.Draw()
				c1.SaveAs("output_mc_2/{}_TH2F_sector_phiy_{}_{}.png".format(self.name,wheel-2,sector+1))

				fit_hist_phiz = self.TH2F_sector_phiz[wheel][sector].ProjectionY()
				fitCut(fit_hist_phiz, 1.5, "QC")
				fit_hist_phiz.Draw()
				c1.SaveAs("output_mc_2/{}_TH2F_sector_phiz_{}_{}.png".format(self.name,wheel-2,sector+1))

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

	def getFitX(self,wheel, sector, sigmas):
		fit_hist_x = self.TH2F_sector_x[wheel+2][sector-1].ProjectionY()
		print fit_hist_x.GetEntries()
		fitCut(fit_hist_x, sigmas, "QC")
		return fit_hist_x.GetFunction("gaus").GetParameter(2)

	def getFitY(self,wheel, sector, sigmas):
		fit_hist_y = self.TH2F_sector_y[wheel+2][sector-1].ProjectionY()
		fitCut(fit_hist_y, sigmas, "QC")
		return fit_hist_y.GetFunction("gaus").GetParameter(2)

	def getFitZ(self,wheel, sector, sigmas):
		fit_hist_z = self.TH2F_sector_z[wheel+2][sector-1].ProjectionY()
		fitCut(fit_hist_z, sigmas, "QC")
		return fit_hist_z.GetFunction("gaus").GetParameter(2)

	def getFitPHIX(self,wheel, sector, sigmas):
		fit_hist_phix = self.TH2F_sector_phix[wheel+2][sector-1].ProjectionY()
		fitCut(fit_hist_phix, sigmas, "QC")
		return fit_hist_phix.GetFunction("gaus").GetParameter(2)

	def getFitPHIY(self,wheel, sector, sigmas):
		fit_hist_phiy = self.TH2F_sector_phiy[wheel+2][sector-1].ProjectionY()
		fitCut(fit_hist_phiy, sigmas, "QC")
		return fit_hist_phiy.GetFunction("gaus").GetParameter(2)

	def getFitPHIZ(self,wheel, sector, sigmas):
		fit_hist_phiz = self.TH2F_sector_phiz[wheel+2][sector-1].ProjectionY()
		fitCut(fit_hist_phiz, sigmas, "QC")
		return fit_hist_phiz.GetFunction("gaus").GetParameter(2)



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

