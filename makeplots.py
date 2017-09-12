import ROOT as r 
import xml.etree.ElementTree as ET
import math
from array import array
import wsh
#import tdrstyle
import tdrstyle_mod14

r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(True)

#c2 = r.TCanvas()



def make2dStatsPlotsPHI(hist_array, name, rms_range, output, cutoff_value, c2):
	conv_gaussian =r.TF1("conv_gaussian","TMath::Sqrt([0]*10^-4/x+[1]*10^-4)",0,10)
	#conv_gaussian =r.TF1("conv_gaussian","([0]*10^-4/x+[1]*10^-4)",0,10)
	conv_gaussian.SetParameters(1.0, .01)
	conv_gaussian.SetParNames("slope", "offset")
	conv_gaussian.SetParLimits(1, .0000000001, 1000)
	conv_gaussian.SetParLimits(0, .0000000001, 2000)

	#conv_gaussian =r.TF1("conv_gaussian","sqrt([0]*abs([0])/(x*x) + [1]*[1]*pow(x,[3]) + [2]*[2])",0,10)
	#conv_gaussian.SetParameters(3.5,0.5,0.03,-1)


	TGraph_cutoffs = r.TGraphErrors()
	TH2F_cutoffs = r.TH2F("TH2F_cutoffs_{}".format(name), "{} cutoff values in Luminosity;  wheel; sectors".format(name), 3, 0,2, 4, 1,4)
	TH2F_cutoffs_text = r.TH2F("TH2F_cutoffs_text_{}".format(name), "{} cutoff values in Luminosity;  wheel; sectors".format(name), 3, 0,2, 4, 1,4)
	TH2F_rand = r.TH2F("TH2F_rand_{}".format(name), "{} random values in Luminosity bellow 200 #mu m;  wheel; sectors".format(name), 3, 0,2, 4, 1,4)
	TH2F_sys = r.TH2F("TH2F_sys_{}".format(name), "{} sys values RMS [cm];  wheel; sectors".format(name), 3, 0,2, 4, 1,4)
	TH1F_cutoffs = r.TH1F("TH1F_cutoffs_{}".format(name), "{} cutoff values; {} rms".format(name,name), 100, 0, 100)
	colorArray = [1,2,3,4,6]
	TH2F_stats_v_rms = []
	
	
	TGraph_stats_v_rms = []
	offset = []
	TLine_cutoff = []
	TLine_cutoff_error = []
	fit = []
	for sector in range(4):
		color = 0
		TH2F_stats_v_rms.append([])
		
		TGraph_stats_v_rms.append([])

		fit.append([])

		offset.append([])
		for wheel in range(3):
			TGraph_stats_v_rms[sector].append (r.TGraphErrors())
			TH2F_stats_v_rms[sector].append( r.TH2F("TH2F_stats_v_rms_{}_{}_{}".format(name, wheel, sector+1), "TH2F_stats_v_rms_{}_{}_{}; Integrated Luminosity; RMS [cm]".format(name, wheel, sector+1), 100, 0, 200000, 100, 0, rms_range))

			old_fit_rms, old_fit_rmsError, old_fit_chi2 = 1000, 1000, 1000
			print range(len(hist_array))
			#for hist in enumerate(hist_array):
			for count in range(len(hist_array)):
				#fill_command = "TH2F_stats_v_rms[sector][wheel].Fill(hist_array[count].getMeanStats(wheel,sector+1),hist_array[count].getRMS{}(wheel,sector+1))".format(name)
				stats, statsError = hist_array[count].getMeanStats(wheel,sector+1), hist_array[count].getMeanStatsError(wheel,sector+1)
				rms_command = "fit_rms, fit_rmsError, fit_chi2, RMS_offset = hist_array[count].getFit{}(wheel,sector+1, 2.5, c2)".format(name,name)

				exec(rms_command)
				rms_command = "rms, rmsError = hist_array[count].getRMS{}(wheel,sector+1), hist_array[count].getRMS{}Error(wheel,sector+1)".format(name,name)
				exec(rms_command)
				print rms, rmsError
				if abs(fit_rms-rms) > rmsError+fit_rmsError: print "out of range {} {} {}".format(name, wheel, sector)
				print "Chi2: {}, deltaRMS {} < {}".format(fit_chi2, abs(fit_rms-rms),  rmsError+fit_rmsError)
				if 1==1: #1.5*old_fit_rmsError > fit_rmsError and old_fit_rmsError < fit_rmsError:
					point_count = TGraph_stats_v_rms[sector][wheel].GetN()
					TGraph_stats_v_rms[sector][wheel].SetPoint(point_count, stats, fit_rms)
					TGraph_stats_v_rms[sector][wheel].SetPointError(point_count, statsError, fit_rmsError)
				old_fit_rms, old_fit_rmsError, old_fit_chi2 = fit_rms, fit_rmsError, fit_chi2
			RMS_offset = math.pow(RMS_offset,2)* math.pow(10,4)
			offset[sector].append(RMS_offset)
				
				
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
		legend =  r.TLegend(0.78,0.68,0.9,0.88)
		TLine_cutoff.append([])
		TLine_cutoff_error.append([])
		maxY = 0
		for wheel in range(3):
			multigraph[sector].Add(TGraph_stats_v_rms[sector][wheel])
			maxY =  max(TGraph_stats_v_rms[sector][wheel].GetYaxis().GetXmax(), maxY)
		#multigraph[sector].Draw()
		#maxY= multigraph[sector].GetYaxis().GetXmax()
		#print maxY

		for wheel in range(3):

			#cutoff = math.pow((TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(0)/(1/25000000-TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(1))),1)
			#print "cuttoff for {} RMS /{}/{}: {}".format(name, wheel, sector+1, cutoff)
			covMatrix =  fit[sector][wheel].GetCovarianceMatrix()
			#print covMatrix[0][0], covMatrix[1][0], covMatrix[1][1]
			sigma0, sigma10, sigma1 = covMatrix[0][0], covMatrix[1][0], covMatrix[1][1]
			#par0, par1 = TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(0),  math.pow(cutoff_value,2)*10000 - TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(1)
			par0, par1 = TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(0),   TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParameter(1)
			par0Error, par1Error = TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParError(0),TGraph_stats_v_rms[sector][wheel].GetFunction("conv_gaussian").GetParError(1)
			#par1 = offset[sector][wheel] + par1
			cutoff = math.pow(par0/par1,1)
			#cutoff =  math.pow( par1/10000.0 + par0/50000.0  ,.5)
			#print sigma0, sigma1, sigma10
			error = 1 #math.pow(abs(cutoff),1)*( math.pow(sigma0/par0,2) +math.pow(sigma1/par1,2) - 2*sigma10/(par0*par1) )
			if error > 0:
				error = math.sqrt(error)
			else : error = 0
			print "rand lumi {} +/- {}".format( par0/(math.pow(cutoff_value,2)*10000), par0Error/(math.pow(cutoff_value,2)*10000) ) 
			print "sys lumi {} +/- {} ".format( math.pow(abs(par1) *math.pow(10,-4) ,.5)* par1/abs(par1), par1Error ) 
			print "cuttoff for {} RMS /{}/{}: {} +/- {}".format(name, wheel, sector+1, cutoff, error)
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
			TH2F_rand.SetBinContent(wheel + 1, sector +1, par0/(math.pow(cutoff_value,2)*10000))
			TH2F_sys.SetBinContent(wheel + 1, sector +1, math.pow(abs(par1) *math.pow(10,-4) ,.5)* par1/abs(par1) )
			if error < 15: 
				TH1F_cutoffs.Fill(cutoff*4)
				TH2F_cutoffs.SetBinContent(wheel+1, sector+1 , cutoff)
			TH2F_cutoffs_text.SetBinContent(wheel+1, sector+1 , cutoff)
				#print cutoff, wheel, sector+1
			color = color + 1
			


		multigraph[sector].Draw("AP")
		#tdrstyle_mod14.tdrDraw(multigraph[sector],"AP")
		multigraph[sector].SetTitle("Chamber Distribtuion in {} for Station {}".format(name, sector+1))
		multigraph[sector].GetXaxis().SetTitle("Integrated Luminosity [fb^{-1}]")
		multigraph[sector].GetYaxis().SetTitleOffset(1.5)
		r.TGaxis.SetMaxDigits(3)
		#multigraph[sector].GetYaxis().SetMaxDigits(3)
		multigraph[sector].GetYaxis().SetTitle("RMS [cm]")
		multigraph[sector].GetYaxis().SetNoExponent(False)
		if "PHI" in name:
			multigraph[sector].GetYaxis().SetTitle("#phi RMS [mRad]")
		leg2 = tdrstyle_mod14.tdrLeg(0.78,0.68,0.9,0.88)
		leg2.SetHeader("{}".format(name))
		for wheel in range(3):
			#TLine_cutoff[sector][wheel].Draw()
			#TLine_cutoff_error[sector][wheel].Draw()
			leg2.AddEntry(TGraph_stats_v_rms[sector][wheel], "/{}/{}".format( wheel, sector+1), "lep")
		#leg2.Draw()
		c2.SaveAs("{}/TGraph_stats_v_rms_{}_sector{}.png".format(output,name, sector+1))
	c2.Clear()
	TGraph_cutoffs.Draw("AP")
	c2.SaveAs("{}/TGraph_cutoffs_{}.png".format(output,name, sector+1))

	TH1F_cutoffs.Draw()
	c2.SaveAs("{}/TH1F_cutoffs_{}.png".format(output,name, sector+1))

	TH2F_cutoffs.Draw("colz")
	TH2F_cutoffs_text.Draw("same TEXT")
	TH2F_cutoffs_text.SetMarkerSize(2)
	c2.SaveAs("{}/TH2F_cutoffs_{}.png".format(output,name, sector+1))
	TH2F_rand.Draw("colz TEXT")
	TH2F_rand.SetMarkerSize(2)
	c2.SaveAs("{}/TH2F_rand{}.png".format(output,name, sector+1))
	TH2F_sys.Draw("colz TEXT")
	TH2F_sys.SetMarkerSize(2)
	c2.SaveAs("{}/TH2F_sys{}.png".format(output,name, sector+1))

	print "{} Safe by: {} +/- {}".format(name, 1*(TH1F_cutoffs.GetMean() ), 1* TH1F_cutoffs.GetMeanError()   )

	return TGraph_stats_v_rms

		