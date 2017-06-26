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
		#	print chamber.detector, chamber.wheel, chamber.station, chamber.sector, chamber.stats, chamber.x


class WheelSectorHistograms:
	def __init__(self, name, chamber_class):
		self.name = name
		self.TH2F_sector_x = []
		for wheel in range(5):
			self.TH2F_sector_x.append([])
			for station in range(4):
				self.TH2F_sector_x[wheel].append( r.TH2F("{}_TH2F_sector_x_{}_{}".format(self.name, wheel-2,station+1),"wheel {} station {}".format(wheel-2,station+1), 100, 0, 500000, 100, -.3,.3 ) )

		for count, chamber in enumerate(chamber_class.chambers):
			#print chamber.wheel, chamber.station, chamber.sector, chamber.x
			self.TH2F_sector_x[chamber.wheel+2][chamber.station-1].Fill(float(chamber.stats), float(chamber.x))

	def draw_hists(self):
		for wheel in range(5):
			for sector in range(4):
				self.TH2F_sector_x[wheel][sector].Draw()
				c1.SaveAs("output/{}_TH2F_sector_x_{}_{}.png".format(self.name,wheel-2,sector+1))
				print self.TH2F_sector_x[wheel][sector].GetRMS()

	def getRMSStats(self,wheel, sector):
		return self.TH2F_sector_x[wheel+2][sector-1].GetRMS(1)

	def getMeanStats(self,wheel, sector):
		return self.TH2F_sector_x[wheel+2][sector-1].GetMean(1)

	def getRMSX(self,wheel, sector):
		return self.TH2F_sector_x[wheel+2][sector-1].GetRMS(2)
	
hist_array = []

execfile("mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01_report.py")
example = ChamberInfo("test", reports, "mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01.xml")

hist_array.append(WheelSectorHistograms("example", example))

#example2.draw_hists()

execfile("full.py")
full = ChamberInfo("full", reports, "full.xml")
hist_array.append(WheelSectorHistograms("full", full))

execfile("half.py")
half = ChamberInfo("half", reports, "half.xml")
hist_array.append(WheelSectorHistograms("half", half))
#half_hist.draw_hists()

execfile("one_third.py")
one_third = ChamberInfo("one_third", reports, "one_third.xml")
hist_array.append(WheelSectorHistograms("one_third", one_third))


execfile("one_sixth.py")
one_sixth = ChamberInfo("one_sixth", reports, "one_sixth.xml")
hist_array.append(WheelSectorHistograms("one_sixth", one_sixth))



execfile("super_small.py")
super_small = ChamberInfo("super_small", reports, "super_small.xml")
hist_array.append(WheelSectorHistograms("super_small", super_small))


execfile("superduper_small.py")
superduper_small = ChamberInfo("superduper_small", reports, "superduper_small.xml")
hist_array.append(WheelSectorHistograms("superduper_small", superduper_small))

#print dir(hist_array[0])

conv_gaussian =r.TF1("conv_gaussian","TMath::Sqrt([0]^2/x+[1]^2)",0,200000)
conv_gaussian.SetParameters(1.0, .01)
conv_gaussian.SetParNames("slope", "offset")

Th2F_stats_v_rms = []
TLine_cutoff = []
color = 1
for sector in range(4):
	color = 1
	Th2F_stats_v_rms.append([])
	TLine_cutoff.append([])
	for wheel in range(5):
		Th2F_stats_v_rms[sector].append( r.TH2F("Th2F_stats_v_rms_{}_{}".format(wheel-2, sector+1), "Th2F_stats_v_rms_{}_{}".format(wheel-2, sector+1), 100, 0, 200000, 100, 0, 0.05))
		#for hist in enumerate(hist_array):
		for count in range(len(hist_array)):
			Th2F_stats_v_rms[sector][wheel].Fill(hist_array[count].getMeanStats(wheel-2,sector+1),hist_array[count].getRMSX(wheel-2,sector+1))

		Th2F_stats_v_rms[sector][wheel].SetMarkerStyle(8)
		Th2F_stats_v_rms[sector][wheel].SetMarkerColor(color)
		Th2F_stats_v_rms[sector][wheel].Fit("conv_gaussian", "Q")
		cutoff = math.pow((Th2F_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(0)/Th2F_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(1)),2)
		TLine_cutoff[sector].append(r.TLine(cutoff,0,cutoff,.05))
		TLine_cutoff[sector][wheel].SetLineColor(color)
		Th2F_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").SetLineColor(color)
		Th2F_stats_v_rms[sector][wheel].SetLineColor(color)
		color = color + 1


for sector in range(4):
	legend =  r.TLegend(0.82,0.68,0.9,0.88)
	for wheel in range(5):
		if(wheel == 0):	
			Th2F_stats_v_rms[sector][wheel].Draw()
		else:
			Th2F_stats_v_rms[sector][wheel].Draw("same")
		TLine_cutoff[sector][wheel].Draw()
		legend.AddEntry(Th2F_stats_v_rms[sector][wheel], "{} {}".format( wheel -2, sector+1), "lep")
	legend.Draw()
	c1.SaveAs("output/Th2F_stats_v_rms_sector{}.png".format( sector+1))
		
	
		





	


#Th2F_stats_v_rms_1_1 =  r.TH2F("Th2F_stats_v_rms_1_1", "Th2F_stats_v_rms_1_1 wheels +/- 1", 100, 0, 200000, 100, 0, 0.05)
#Th2F_stats_v_rms_1_2 =  r.TH2F("Th2F_stats_v_rms_1_2", "Th2F_stats_v_rms_1_2", 100, 0, 200000, 100, 0, 0.05)
#Th2F_stats_v_rms_1_3 =  r.TH2F("Th2F_stats_v_rms_1_3", "Th2F_stats_v_rms_1_3", 100, 0, 200000, 100, 0, 0.05)
#Th2F_stats_v_rms_1_4 =  r.TH2F("Th2F_stats_v_rms_1_4", "Th2F_stats_v_rms_1_4", 100, 0, 200000, 100, 0, 0.05)
#
#
#Th2F_stats_v_rms_n1_1 =  r.TH2F("Th2F_stats_v_rms_n1_1", "Th2F_stats_v_rms_n1_1", 100, 0, 200000, 100, 0, 0.05)
#Th2F_stats_v_rms_n1_2 =  r.TH2F("Th2F_stats_v_rms_n1_2", "Th2F_stats_v_rms_n1_2", 100, 0, 200000, 100, 0, 0.05)
#Th2F_stats_v_rms_n1_3 =  r.TH2F("Th2F_stats_v_rms_n1_3", "Th2F_stats_v_rms_n1_3", 100, 0, 200000, 100, 0, 0.05)
#Th2F_stats_v_rms_n1_4 =  r.TH2F("Th2F_stats_v_rms_n1_4", "Th2F_stats_v_rms_n1_4", 100, 0, 200000, 100, 0, 0.05)
#
#conv_gaussian =r.TF1("conv_gaussian","TMath::Sqrt([0]^2/x+[1]^2)",0,200000)
#
#conv_gaussian.SetParameters(1.0, .01)
#conv_gaussian.SetParNames("slope", "offset")
#
#Th2F_stats_v_rms_1_1.Fill(full_hist.getMeanStats(1,1),  full_hist.getRMSX(1,1))
#Th2F_stats_v_rms_1_1.Fill(example2.getMeanStats(1,1),   example2.getRMSX(1,1))
#Th2F_stats_v_rms_1_1.Fill(half_hist.getMeanStats(1,1),   half_hist.getRMSX(1,1))
#Th2F_stats_v_rms_1_1.Fill(one_sixth_hist.getMeanStats(1,1),   one_sixth_hist.getRMSX(1,1))
##Th2F_stats_v_rms_1_1.Fill(super_small_hist.getMeanStats(1,1),   super_small_hist.getRMSX(1,1))
##Th2F_stats_v_rms_1_1.Fill(superduper_small_hist.getMeanStats(1,1),   superduper_small_hist.getRMSX(1,1))
#
#
#Th2F_stats_v_rms_n1_1.Fill(full_hist.getMeanStats(-1,1),  full_hist.getRMSX(-1,1))
#Th2F_stats_v_rms_n1_1.Fill(example2.getMeanStats(-1,1),   example2.getRMSX(-1,1))
#Th2F_stats_v_rms_n1_1.Fill(half_hist.getMeanStats(-1,1),   half_hist.getRMSX(-1,1))
#Th2F_stats_v_rms_n1_1.Fill(one_sixth_hist.getMeanStats(-1,1),   one_sixth_hist.getRMSX(-1,1))
##Th2F_stats_v_rms_n1_1.Fill(super_small_hist.getMeanStats(-1,1),   super_small_hist.getRMSX(-1,1))
##Th2F_stats_v_rms_n1_1.Fill(superduper_small_hist.getMeanStats(-1,1),   superduper_small_hist.getRMSX(-1,1))
#
#
#Th2F_stats_v_rms_1_2.Fill(full_hist.getMeanStats(1,2),  full_hist.getRMSX(1,2))
#Th2F_stats_v_rms_1_2.Fill(example2.getMeanStats(1,2),   example2.getRMSX(1,2))
#Th2F_stats_v_rms_1_2.Fill(half_hist.getMeanStats(1,2),   half_hist.getRMSX(1,2))
#Th2F_stats_v_rms_1_2.Fill(one_sixth_hist.getMeanStats(1,2),   one_sixth_hist.getRMSX(1,2))
##Th2F_stats_v_rms_1_2.Fill(super_small_hist.getMeanStats(1,2),   super_small_hist.getRMSX(1,2))
##Th2F_stats_v_rms_1_2.Fill(superduper_small_hist.getMeanStats(1,2),   superduper_small_hist.getRMSX(1,2))
#
#Th2F_stats_v_rms_n1_2.Fill(full_hist.getMeanStats(-1,2),  full_hist.getRMSX(-1,2))
#Th2F_stats_v_rms_n1_2.Fill(example2.getMeanStats(-1,2),   example2.getRMSX(-1,2))
#Th2F_stats_v_rms_n1_2.Fill(half_hist.getMeanStats(-1,2),   half_hist.getRMSX(-1,2))
#Th2F_stats_v_rms_n1_2.Fill(one_sixth_hist.getMeanStats(-1,2),   one_sixth_hist.getRMSX(-1,2))
##Th2F_stats_v_rms_n1_2.Fill(super_small_hist.getMeanStats(-1,2),   super_small_hist.getRMSX(-1,2))
##Th2F_stats_v_rms_n1_2.Fill(superduper_small_hist.getMeanStats(-1,2),   superduper_small_hist.getRMSX(-1,2))
#
#
#
#Th2F_stats_v_rms_1_3.Fill(full_hist.getMeanStats(1,3),  full_hist.getRMSX(1,3))
#Th2F_stats_v_rms_1_3.Fill(example2.getMeanStats(1,3),   example2.getRMSX(1,3))
#Th2F_stats_v_rms_1_3.Fill(half_hist.getMeanStats(1,3),   half_hist.getRMSX(1,3))
#Th2F_stats_v_rms_1_3.Fill(one_sixth_hist.getMeanStats(1,3),   one_sixth_hist.getRMSX(1,3))
##Th2F_stats_v_rms_1_3.Fill(super_small_hist.getMeanStats(1,3),   super_small_hist.getRMSX(1,3))
##Th2F_stats_v_rms_1_3.Fill(superduper_small_hist.getMeanStats(1,3),   superduper_small_hist.getRMSX(1,3))
#
#Th2F_stats_v_rms_n1_3.Fill(full_hist.getMeanStats(-1,3),  full_hist.getRMSX(-1,3))
#Th2F_stats_v_rms_n1_3.Fill(example2.getMeanStats(-1,3),   example2.getRMSX(-1,3))
#Th2F_stats_v_rms_n1_3.Fill(half_hist.getMeanStats(-1,3),   half_hist.getRMSX(-1,3))
#Th2F_stats_v_rms_n1_3.Fill(one_sixth_hist.getMeanStats(-1,3),   one_sixth_hist.getRMSX(-1,3))
#Th2F_stats_v_rms_n1_3.Fill(super_small_hist.getMeanStats(-1,3),   super_small_hist.getRMSX(-1,3))
#Th2F_stats_v_rms_n1_3.Fill(superduper_small_hist.getMeanStats(-1,3),   superduper_small_hist.getRMSX(-1,3))
#
#
#Th2F_stats_v_rms_1_4.Fill(full_hist.getMeanStats(1,4),  full_hist.getRMSX(1,4))
#Th2F_stats_v_rms_1_4.Fill(example2.getMeanStats(1,4),   example2.getRMSX(1,4))
#Th2F_stats_v_rms_1_4.Fill(half_hist.getMeanStats(1,4),   half_hist.getRMSX(1,4))
#Th2F_stats_v_rms_1_4.Fill(one_sixth_hist.getMeanStats(1,4),   one_sixth_hist.getRMSX(1,4))
#Th2F_stats_v_rms_1_4.Fill(super_small_hist.getMeanStats(1,4),   super_small_hist.getRMSX(1,4))
#Th2F_stats_v_rms_1_4.Fill(superduper_small_hist.getMeanStats(1,4),   superduper_small_hist.getRMSX(1,4))
#
#Th2F_stats_v_rms_n1_4.Fill(full_hist.getMeanStats(-1,4),  full_hist.getRMSX(-1,4))
#Th2F_stats_v_rms_n1_4.Fill(example2.getMeanStats(-1,4),   example2.getRMSX(-1,4))
#Th2F_stats_v_rms_n1_4.Fill(half_hist.getMeanStats(-1,4),   half_hist.getRMSX(-1,4))
#Th2F_stats_v_rms_n1_4.Fill(one_sixth_hist.getMeanStats(-1,4),   one_sixth_hist.getRMSX(-1,4))
#Th2F_stats_v_rms_n1_4.Fill(super_small_hist.getMeanStats(-1,4),   super_small_hist.getRMSX(-1,4))
#Th2F_stats_v_rms_n1_4.Fill(superduper_small_hist.getMeanStats(-1,4),   superduper_small_hist.getRMSX(-1,4))
#
#
#Th2F_stats_v_rms_1_1.SetMarkerStyle(8)
#Th2F_stats_v_rms_n1_1.SetMarkerStyle(8)
#Th2F_stats_v_rms_1_2.SetMarkerStyle(8)
#Th2F_stats_v_rms_n1_2.SetMarkerStyle(8)
#Th2F_stats_v_rms_1_3.SetMarkerStyle(8)
#Th2F_stats_v_rms_n1_3.SetMarkerStyle(8)
#Th2F_stats_v_rms_1_4.SetMarkerStyle(8)
#Th2F_stats_v_rms_n1_4.SetMarkerStyle(8)
#
#Th2F_stats_v_rms_1_1.SetMarkerColor(1)
#Th2F_stats_v_rms_n1_1.SetMarkerColor(2)
#Th2F_stats_v_rms_1_2.SetMarkerColor(3)
#Th2F_stats_v_rms_n1_2.SetMarkerColor(4)
#Th2F_stats_v_rms_1_3.SetMarkerColor(5)
#Th2F_stats_v_rms_n1_3.SetMarkerColor(6)
#Th2F_stats_v_rms_1_4.SetMarkerColor(7)
#Th2F_stats_v_rms_n1_4.SetMarkerColor(8)
#
#
#
#Th2F_stats_v_rms_1_1.Fit("conv_gaussian")
#Th2F_stats_v_rms_n1_1.Fit("conv_gaussian")
#Th2F_stats_v_rms_1_2.Fit("conv_gaussian")
#Th2F_stats_v_rms_n1_2.Fit("conv_gaussian")
#Th2F_stats_v_rms_1_3.Fit("conv_gaussian")
#Th2F_stats_v_rms_n1_3.Fit("conv_gaussian")
#Th2F_stats_v_rms_1_4.Fit("conv_gaussian")
#Th2F_stats_v_rms_n1_4.Fit("conv_gaussian")
#
#
#
#Th2F_stats_v_rms_1_1.GetFunction("conv_gaussian").SetLineColor(1)
#Th2F_stats_v_rms_n1_1.GetFunction("conv_gaussian").SetLineColor(2)
#Th2F_stats_v_rms_1_2.GetFunction("conv_gaussian").SetLineColor(3)
#Th2F_stats_v_rms_n1_2.GetFunction("conv_gaussian").SetLineColor(4)
#Th2F_stats_v_rms_1_3.GetFunction("conv_gaussian").SetLineColor(5)
#Th2F_stats_v_rms_n1_3.GetFunction("conv_gaussian").SetLineColor(6)
#Th2F_stats_v_rms_1_4.GetFunction("conv_gaussian").SetLineColor(7)
#Th2F_stats_v_rms_n1_4.GetFunction("conv_gaussian").SetLineColor(8)
#
#
#Th2F_stats_v_rms_1_1.Draw()
#Th2F_stats_v_rms_n1_1.Draw("same")
#Th2F_stats_v_rms_1_2.Draw("same")
#Th2F_stats_v_rms_n1_2.Draw("same")
#Th2F_stats_v_rms_1_3.Draw("same")
#Th2F_stats_v_rms_n1_3.Draw("same")
#Th2F_stats_v_rms_1_4.Draw("same")
#Th2F_stats_v_rms_n1_4.Draw("same")
#
#legend =  r.TLegend(0.82,0.68,0.9,0.88)
#legend.AddEntry(Th2F_stats_v_rms_1_1,"1_1","lep")
#legend.AddEntry(Th2F_stats_v_rms_n1_1,"n1_1","lep")
#legend.AddEntry(Th2F_stats_v_rms_1_2,"1_2","lep")
#legend.AddEntry(Th2F_stats_v_rms_n1_2,"n1_2","lep")
#legend.AddEntry(Th2F_stats_v_rms_1_3,"1_3","lep")
#legend.AddEntry(Th2F_stats_v_rms_n1_3,"n1_3","lep")
#legend.AddEntry(Th2F_stats_v_rms_1_4,"1_4","lep")
#legend.AddEntry(Th2F_stats_v_rms_n1_4,"n1_4","lep")
#legend.Draw()
#
#
#stats_cutoff_1_1 = math.pow((Th2F_stats_v_rms_1_1.GetFunction("conv_gaussian").GetParameter(0)/Th2F_stats_v_rms_1_1.GetFunction("conv_gaussian").GetParameter(1)),2)
#stats_cutoff_1_2 = math.pow((Th2F_stats_v_rms_1_2.GetFunction("conv_gaussian").GetParameter(0)/Th2F_stats_v_rms_1_2.GetFunction("conv_gaussian").GetParameter(1)),2)
#stats_cutoff_1_3 = math.pow((Th2F_stats_v_rms_1_3.GetFunction("conv_gaussian").GetParameter(0)/Th2F_stats_v_rms_1_3.GetFunction("conv_gaussian").GetParameter(1)),2)
#stats_cutoff_1_4 = math.pow((Th2F_stats_v_rms_1_4.GetFunction("conv_gaussian").GetParameter(0)/Th2F_stats_v_rms_1_4.GetFunction("conv_gaussian").GetParameter(1)),2)
#stats_cutoff_n1_1 =	math.pow((Th2F_stats_v_rms_n1_1.GetFunction("conv_gaussian").GetParameter(0)/Th2F_stats_v_rms_n1_1.GetFunction("conv_gaussian").GetParameter(1)),2)
#stats_cutoff_n1_2 =	math.pow((Th2F_stats_v_rms_n1_2.GetFunction("conv_gaussian").GetParameter(0)/Th2F_stats_v_rms_n1_2.GetFunction("conv_gaussian").GetParameter(1)),2)
#stats_cutoff_n1_3 =	math.pow((Th2F_stats_v_rms_n1_3.GetFunction("conv_gaussian").GetParameter(0)/Th2F_stats_v_rms_n1_3.GetFunction("conv_gaussian").GetParameter(1)),2)
#stats_cutoff_n1_4 =	math.pow((Th2F_stats_v_rms_n1_4.GetFunction("conv_gaussian").GetParameter(0)/Th2F_stats_v_rms_n1_4.GetFunction("conv_gaussian").GetParameter(1)),2)
#
#print stats_cutoff_1_4 , stats_cutoff_n1_3
#
#line_1_1 = r.TLine(stats_cutoff_1_1,0,stats_cutoff_1_1,0.05)
#line_n1_1 = r.TLine(stats_cutoff_n1_1,0,stats_cutoff_n1_1,0.05)
#line_1_2 = r.TLine(stats_cutoff_1_2,0,stats_cutoff_1_2,0.05)
#line_n1_2 = r.TLine(stats_cutoff_n1_2,0,stats_cutoff_n1_2,0.05)
#line_1_3 = r.TLine(stats_cutoff_1_3,0,stats_cutoff_1_3,0.05)
#line_n1_3 = r.TLine(stats_cutoff_n1_3,0,stats_cutoff_n1_3,0.05)
#line_1_4 = r.TLine(stats_cutoff_1_4,0,stats_cutoff_1_4,0.05)
#line_n1_4 = r.TLine(stats_cutoff_n1_4,0,stats_cutoff_n1_4,0.05)
#
#
#line_1_1.SetLineColor(1)
#line_n1_1.SetLineColor(2)
#line_1_2.SetLineColor(3)
#line_n1_2.SetLineColor(4)
#line_1_3.SetLineColor(5)
#line_n1_3.SetLineColor(6)
#line_1_4.SetLineColor(7)
#line_n1_4.SetLineColor(8)
#
#line_1_1.Draw()
#line_n1_1.Draw()
#line_1_2.Draw()
#line_n1_2.Draw()
#line_1_3.Draw()
#line_n1_3.Draw()
#line_1_4.Draw()
#line_n1_4.Draw()
#
#c1.SetLogX()
#
#c1.SaveAs("output/Th2F_stats_v_rms.png")
#
#
#
#
##Th2F_stats_v_rms.Fit("conv_gaussian")
##Th2F_stats_v_rms_2.SetMarkerStyle(8)
##Th2F_stats_v_rms_2.SetMarkerColor(2)
##Th2F_stats_v_rms_2.Fit("conv_gaussian")
##Th2F_stats_v_rms.Draw()
##Th2F_stats_v_rms_2.Draw("same")
##c1.SaveAs("output/Th2F_stats_v_rms.png")
#
#
##print full_hist.getMeanStats(2,1), "\t", full_hist.getRMSX(2,1)
##
##print example2.getMeanStats(2,1), "\t",  example2.getRMSX(2,1)
##
##
##print half_hist.getMeanStats(2,1), "\t",  half_hist.getRMSX(2,1)
##
##
##print one_sixth_hist.getMeanStats(2,1), "\t",  one_sixth_hist.getRMSX(2,1)
##
##
##print one_third_hist.getMeanStats(2,1), "\t",  one_third_hist.getRMSX(2,1)
##
##
##print full_hist.getMeanStats(2,2), "\t", full_hist.getRMSX(2,2)
##
##print example2.getMeanStats(2,2), "\t",  example2.getRMSX(2,2)
##
##
##print half_hist.getMeanStats(2,2), "\t",  half_hist.getRMSX(2,2)
##
##
##print one_sixth_hist.getMeanStats(2,2), "\t",  one_sixth_hist.getRMSX(2,2)
##
##
##print one_third_hist.getMeanStats(2,2), "\t",  one_third_hist.getRMSX(2,2)
##
##
##
##
##print full_hist.getMeanStats(2,3), "\t", full_hist.getRMSX(2,3)
##
##print example2.getMeanStats(2,3), "\t",  example2.getRMSX(2,3)
##
##
##print half_hist.getMeanStats(2,3), "\t",  half_hist.getRMSX(2,3)
##
##
##print one_sixth_hist.getMeanStats(2,3), "\t",  one_sixth_hist.getRMSX(2,3)
##
##
##print one_third_hist.getMeanStats(2,3), "\t",  one_third_hist.getRMSX(2,3)
##
##
##
##print full_hist.getMeanStats(2,4), "\t", full_hist.getRMSX(2,4)
##
##print example2.getMeanStats(2,4), "\t",  example2.getRMSX(2,4)
##
##
##print half_hist.getMeanStats(2,4), "\t",  half_hist.getRMSX(2,4)
#
#
#print one_sixth_hist.getMeanStats(2,4), "\t",  one_sixth_hist.getRMSX(2,4)
#
#
#print one_third_hist.getMeanStats(2,4), "\t",  one_third_hist.getRMSX(2,4)
#
#
#print full_hist.getMeanStats(-2,1), "\t", full_hist.getRMSX(-2,1)
#
#print example2.getMeanStats(-2,1), "\t",  example2.getRMSX(-2,1)
#
#
#print half_hist.getMeanStats(-2,1), "\t",  half_hist.getRMSX(-2,1)
#
#
#print one_sixth_hist.getMeanStats(-2,1), "\t",  one_sixth_hist.getRMSX(-2,1)
#
#
#print one_third_hist.getMeanStats(-2,1), "\t",  one_third_hist.getRMSX(-2,1)
#
#
#print full_hist.getMeanStats(-2,2), "\t", full_hist.getRMSX(-2,2)
#
#print example2.getMeanStats(-2,2), "\t",  example2.getRMSX(-2,2)
#
#
#print half_hist.getMeanStats(-2,2), "\t",  half_hist.getRMSX(-2,2)
#
#
#print one_sixth_hist.getMeanStats(-2,2), "\t",  one_sixth_hist.getRMSX(-2,2)
#
#
#print one_third_hist.getMeanStats(-2,2), "\t",  one_third_hist.getRMSX(-2,2)
#
#
#
#
#print full_hist.getMeanStats(-2,3), "\t", full_hist.getRMSX(-2,3)
#
#print example2.getMeanStats(-2,3), "\t",  example2.getRMSX(-2,3)
#
#
#print half_hist.getMeanStats(-2,3), "\t",  half_hist.getRMSX(-2,3)
#
#
#print one_sixth_hist.getMeanStats(-2,3), "\t",  one_sixth_hist.getRMSX(-2,3)
#
#
#print one_third_hist.getMeanStats(-2,3), "\t",  one_third_hist.getRMSX(-2,3)
#
#
#
#print full_hist.getMeanStats(-2,4), "\t", full_hist.getRMSX(-2,4)
#
#print example2.getMeanStats(-2,4), "\t",  example2.getRMSX(-2,4)
#
#
#print half_hist.getMeanStats(-2,4), "\t",  half_hist.getRMSX(-2,4)
#
#
#print one_sixth_hist.getMeanStats(-2,4), "\t",  one_sixth_hist.getRMSX(-2,4)
#
#
#print one_third_hist.getMeanStats(-2,4), "\t",  one_third_hist.getRMSX(-2,4)
#
##execfile("mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01_report.py")
##tree = ET.parse('mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01.xml')
##tree = ET.ElementTree(file='mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01.xml')
##root = tree.getroot()
#
##example.set_values(reports, root)
#
#
#
#
#
#
##print "0,4", example2.getMeanStats(0,4), example2.getRMSStats(0,4)
#
##for wheel in range(5):
##	TH1F_sector_x.append([])
##	for station in range(4):
##		TH1F_sector_x[wheel].append( r.TH2F("TH1F_sector_x_{}_{}".format(wheel-2,station+1),"wheel {} station {}".format(wheel-2,station+1), 100, 0, 20000, 100, -.3,.3 ) )
##
##for count, chamber in enumerate(example.chambers):
##	#print chamber.wheel, chamber.station, chamber.sector, chamber.x
##	TH1F_sector_x[chamber.wheel+2][chamber.station-1].Fill(float(chamber.stats), float(chamber.x))
##
##
##for wheel in range(5):
##	for station in range(4):
##		TH1F_sector_x[wheel][station].Draw()
##		c1.SaveAs("output/TH1F_sector_x_{}_{}.png".format(wheel-2,station+1))
##		print TH1F_sector_x[wheel][station].GetRMS()
##
##
##
###TH2F_stats_v_x = r.TH2F("TH2F_stats_v_x", "TH2F_stats_v_x", 100, 0,20000, 100, -.3,.3)
###
###for count, chamber in enumerate(example.chambers):
###	TH2F_stats_v_x.Fill(chamber.stats, abs(float(chamber.x)))
###
###print TH2F_stats_v_x.GetRMS(1), TH2F_stats_v_x.GetRMS(2)
###
###TH2F_stats_v_x.Draw("colz")
##c1.SaveAs("output/TH2F_stats_v_x.png")
##
###