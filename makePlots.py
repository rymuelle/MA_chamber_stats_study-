import ROOT as r 
import xml.etree.ElementTree as ET


r.gROOT.SetBatch(True)


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
				
		for count, chamber in enumerate(self.chambers):
			print chamber.detector, chamber.wheel, chamber.station, chamber.sector, chamber.stats, chamber.x


class WheelSectorHistograms:
	def __init__(self, name, chamber_class):
		self.name = name
		self.TH1F_sector_x = []
		for wheel in range(5):
			self.TH1F_sector_x.append([])
			for station in range(4):
				self.TH1F_sector_x[wheel].append( r.TH2F("TH1F_sector_x_{}_{}".format(wheel-2,station+1),"wheel {} station {}".format(wheel-2,station+1), 100, 0, 20000, 100, -.3,.3 ) )

		for count, chamber in enumerate(chamber_class.chambers):
			#print chamber.wheel, chamber.station, chamber.sector, chamber.x
			self.TH1F_sector_x[chamber.wheel+2][chamber.station-1].Fill(float(chamber.stats), float(chamber.x))

	def draw_hists(self):
		for wheel in range(5):
			for station in range(4):
				self.TH1F_sector_x[wheel][station].Draw()
				c1.SaveAs("output/TH1F_sector_x_{}_{}.png".format(wheel-2,station+1))
				print self.TH1F_sector_x[wheel][station].GetRMS()
	



execfile("mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01_report.py")
example = ChamberInfo("test", reports, "mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01.xml")


#execfile("mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01_report.py")
#tree = ET.parse('mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01.xml')
#tree = ET.ElementTree(file='mc_DT-1100-111111_CMSSW_9_2_1_13TeV_39M_01.xml')
#root = tree.getroot()

#example.set_values(reports, root)

c1 = r.TCanvas()


example2 = WheelSectorHistograms("example", example)

example2.draw_hists()

#for wheel in range(5):
#	TH1F_sector_x.append([])
#	for station in range(4):
#		TH1F_sector_x[wheel].append( r.TH2F("TH1F_sector_x_{}_{}".format(wheel-2,station+1),"wheel {} station {}".format(wheel-2,station+1), 100, 0, 20000, 100, -.3,.3 ) )
#
#for count, chamber in enumerate(example.chambers):
#	#print chamber.wheel, chamber.station, chamber.sector, chamber.x
#	TH1F_sector_x[chamber.wheel+2][chamber.station-1].Fill(float(chamber.stats), float(chamber.x))
#
#
#for wheel in range(5):
#	for station in range(4):
#		TH1F_sector_x[wheel][station].Draw()
#		c1.SaveAs("output/TH1F_sector_x_{}_{}.png".format(wheel-2,station+1))
#		print TH1F_sector_x[wheel][station].GetRMS()
#
#
#
##TH2F_stats_v_x = r.TH2F("TH2F_stats_v_x", "TH2F_stats_v_x", 100, 0,20000, 100, -.3,.3)
##
##for count, chamber in enumerate(example.chambers):
##	TH2F_stats_v_x.Fill(chamber.stats, abs(float(chamber.x)))
##
##print TH2F_stats_v_x.GetRMS(1), TH2F_stats_v_x.GetRMS(2)
##
##TH2F_stats_v_x.Draw("colz")
#c1.SaveAs("output/TH2F_stats_v_x.png")
#
#