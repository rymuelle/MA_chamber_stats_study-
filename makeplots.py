import ROOT as r 
import xml.etree.ElementTree as ET
import math
from array import array
import wsh

r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(True)

c2 = r.TCanvas()

def make2dStatsPlots(hist_array, name, rms_range, output):
	conv_gaussian =r.TF1("conv_gaussian","TMath::Sqrt([0]*10^-4/x+[1]*10^-4)",0,10)
	conv_gaussian.SetParameters(1.0, .01)
	conv_gaussian.SetParNames("slope", "offset")
	conv_gaussian.SetParLimits(1, .0000000000000001, 100)
	conv_gaussian.SetParLimits(0, .0000000000000001, 100)
	TGraph_cutoffs = r.TGraphErrors()
	TH1F_cutoffs = r.TH1F("TH1F_cutoffs_{}".format(name), "{} cutoff values; {} rms".format(name,name), 100, 0, 20)
	colorArray = [1,2,3,4,6]
	TH2F_stats_v_rms = []
	TGraph_stats_v_rms = []
	TLine_cutoff = []
	TLine_cutoff_error = []
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
				rms_command = "rms, rmsError = hist_array[count].getRMSProtected{}(wheel,sector+1), hist_array[count].getRMSProtectedError{}(wheel,sector+1)".format(name,name)
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
		TLine_cutoff_error.append([])
		maxY = 0
		for wheel in range(3):
			multigraph[sector].Add(TGraph_stats_v_rms[sector][wheel])
			maxY =  max(TGraph_stats_v_rms[sector][wheel].GetYaxis().GetXmax(), maxY)
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
			TLine_cutoff_error[sector].append(r.TLine(cutoff-error,maxY/2.0,cutoff+error,maxY/2.0))
			TLine_cutoff_error[sector][wheel].SetLineColor(colorArray[color])

			TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").SetLineColor(colorArray[color])
			TGraph_stats_v_rms[sector][wheel].SetLineColor(colorArray[color])
			point_count = TGraph_cutoffs.GetN()
			TGraph_cutoffs.SetPoint(point_count, cutoff, wheel)
			TGraph_cutoffs.SetPointError(point_count, error, 0)
			if error < 15:  TH1F_cutoffs.Fill(cutoff*4)
			color = color + 1
			
			
		multigraph[sector].Draw("AP")
		for wheel in range(3):
			TLine_cutoff[sector][wheel].Draw()
			TLine_cutoff_error[sector][wheel].Draw()
			legend.AddEntry(TGraph_stats_v_rms[sector][wheel], "{} {}".format( wheel, sector+1), "lep")
		legend.Draw()
		c2.SaveAs("{}/TGraph_stats_v_rms_{}_sector{}.png".format(output,name, sector+1))
	TGraph_cutoffs.Draw()
	c2.SaveAs("{}/TGraph_cutoffs_{}.png".format(output,name, sector+1))
	TH1F_cutoffs.Draw()
	c2.SaveAs("{}/TH1F_cutoffs_{}.png".format(output,name, sector+1))




def make2dStatsPlotsPHI(hist_array, name, rms_range, output):
	conv_gaussian =r.TF1("conv_gaussian","TMath::Sqrt([0]*10^-4/x+[1]*10^-4)",0,10)
	conv_gaussian.SetParameters(1.0, .01)
	conv_gaussian.SetParNames("slope", "offset")
	conv_gaussian.SetParLimits(1, .0000000000000001, 100)
	conv_gaussian.SetParLimits(0, .0000000000000001, 100)
	TGraph_cutoffs = r.TGraphErrors()
	TH1F_cutoffs = r.TH1F("TH1F_cutoffs_{}".format(name), "{} cutoff values; {} rms".format(name,name), 100, 0, 20)
	colorArray = [1,2,3,4,6]
	TH2F_stats_v_rms = []
	TGraph_stats_v_rms = []
	TLine_cutoff = []
	TLine_cutoff_error = []
	fit = []
	for sector in range(4):
		color = 0
		TH2F_stats_v_rms.append([])
		TGraph_stats_v_rms.append([])
		fit.append([])
		for wheel in range(5):
			TGraph_stats_v_rms[sector].append (r.TGraphErrors())
			TH2F_stats_v_rms[sector].append( r.TH2F("TH2F_stats_v_rms_{}_{}_{}".format(name, wheel-2, sector+1), "TH2F_stats_v_rms_{}_{}_{}".format(name, wheel-2, sector+1), 100, 0, 200000, 100, 0, rms_range))

			#for hist in enumerate(hist_array):
			for count in range(len(hist_array)):
				#fill_command = "TH2F_stats_v_rms[sector][wheel].Fill(hist_array[count].getMeanStats(wheel,sector+1),hist_array[count].getRMS{}(wheel,sector+1))".format(name)
				stats, statsError = hist_array[count].getMeanStats(wheel-2,sector+1), hist_array[count].getMeanStatsError(wheel-2,sector+1)
				rms_command = "rms, rmsError = hist_array[count].getRMS{}(wheel-2,sector+1), hist_array[count].getRMS{}Error(wheel-2,sector+1)".format(name,name)
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
		TLine_cutoff_error.append([])
		maxY = 0
		for wheel in range(5):
			multigraph[sector].Add(TGraph_stats_v_rms[sector][wheel])
			maxY =  max(TGraph_stats_v_rms[sector][wheel].GetYaxis().GetXmax(), maxY)
		#multigraph[sector].Draw()
		#maxY= multigraph[sector].GetYaxis().GetXmax()
		#print maxY

		for wheel in range(5):

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

			print "cuttoff for {} RMS /{}/{}: {} +/- {}".format(name, wheel-2, sector+1, cutoff, error)
			#print math.sqrt(covMatrix[0][0]), TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParError(0)
			#print math.sqrt(covMatrix[1][1]), TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParError(1)

			TLine_cutoff[sector].append(r.TLine(cutoff,0,cutoff,maxY/2.0))
			TLine_cutoff[sector][wheel].SetLineColor(colorArray[color])
			TLine_cutoff_error[sector].append(r.TLine(cutoff-error,maxY/2.0,cutoff+error,maxY/2.0))
			TLine_cutoff_error[sector][wheel].SetLineColor(colorArray[color])


			TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").SetLineColor(colorArray[color])
			TGraph_stats_v_rms[sector][wheel].SetLineColor(colorArray[color])


			point_count = TGraph_cutoffs.GetN()
			TGraph_cutoffs.SetPoint(point_count, cutoff, wheel)
			TGraph_cutoffs.SetPointError(point_count, error, 0)
			if error < 15:  TH1F_cutoffs.Fill(cutoff*4)
			color = color + 1
			
			
		multigraph[sector].Draw("AP")
		for wheel in range(5):
			TLine_cutoff[sector][wheel].Draw()
			TLine_cutoff_error[sector][wheel].Draw()
			legend.AddEntry(TGraph_stats_v_rms[sector][wheel], "{} {}".format( wheel-2, sector+1), "lep")
		legend.Draw()
		c2.SaveAs("{}/TGraph_stats_v_rms_{}_sector{}.png".format(output,name, sector+1))
	TGraph_cutoffs.Draw()
	c2.SaveAs("{}/TGraph_cutoffs_{}.png".format(output,name, sector+1))
	TH1F_cutoffs.Draw()
	c2.SaveAs("{}/TH1F_cutoffs_{}.png".format(output,name, sector+1))

		