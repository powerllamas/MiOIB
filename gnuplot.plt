#!/gnuplot
#
#    
#    	G N U P L O T
#    	Version 4.4 patchlevel 3
#    	last modified March 2011
#    	System: MS-Windows 32 bit 
#    
#    	Copyright (C) 1986-1993, 1998, 2004, 2007-2010
#    	Thomas Williams, Colin Kelley and many others
#    
#    	gnuplot home:     http://www.gnuplot.info
#    	faq, bugs, etc:   type "help seeking-assistance"
#    	immediate help:   type "help"
#    	plot window:      hit 'h'
# set terminal wxt 0
# set output
unset clip points
set clip one
unset clip two
set bar 1.000000 front
set border 31 front linetype -1 linewidth 1.000
set xdata
set ydata
set zdata
set x2data
set y2data
set timefmt x "%d/%m/%y,%H:%M"
set timefmt y "%d/%m/%y,%H:%M"
set timefmt z "%d/%m/%y,%H:%M"
set timefmt x2 "%d/%m/%y,%H:%M"
set timefmt y2 "%d/%m/%y,%H:%M"
set timefmt cb "%d/%m/%y,%H:%M"
set boxwidth
set style fill  empty border
set style rectangle back fc lt -3 fillstyle   solid 1.00 border lt -1
set style circle radius graph 0.02, first 0, 0 
set dummy x,y
set format x "% g"
set format y "% g"
set format x2 "% g"
set format y2 "% g"
set format z "% g"
set format cb "% g"
set angles radians
unset grid
set key title ""
set key inside right top vertical Right noreverse enhanced autotitles nobox
set key noinvert samplen 4 spacing 1 width 0 height 0 
set key maxcolumns 0 maxrows 0
unset label
unset arrow
set style increment default
unset style line
unset style arrow
set style histogram clustered gap 2 title  offset character 0, 0, 0
unset logscale
set offsets 0, 0, 0, 0
set pointsize 1
set pointintervalbox 1
set encoding default
unset polar
unset parametric
unset decimalsign
set view 60, 30, 1, 1
set samples 100, 100
set isosamples 10, 10
set surface
unset contour
set clabel '%8.3g'
set mapping cartesian
set datafile separator whitespace
unset hidden3d
set cntrparam order 4
set cntrparam linear
set cntrparam levels auto 5
set cntrparam points 5
set size ratio 0 1,1
set origin 0,0
set style data points
set style function lines
set xzeroaxis linetype -2 linewidth 1.000
set yzeroaxis linetype -2 linewidth 1.000
set zzeroaxis linetype -2 linewidth 1.000
set x2zeroaxis linetype -2 linewidth 1.000
set y2zeroaxis linetype -2 linewidth 1.000
set ticslevel 0.5
set mxtics default
set mytics default
set mztics default
set mx2tics default
set my2tics default
set mcbtics default
set xtics border in scale 1,0.5 mirror norotate  offset character 0, 0, 0
set xtics  norangelimit
set xtics   ()
set ytics border in scale 1,0.5 mirror norotate  offset character 0, 0, 0
set ytics autofreq  norangelimit
set ztics border in scale 1,0.5 nomirror norotate  offset character 0, 0, 0
set ztics autofreq  norangelimit
set nox2tics
set noy2tics
set cbtics border in scale 1,0.5 mirror norotate  offset character 0, 0, 0
set cbtics autofreq  norangelimit
set title "" 
set title  offset character 0, 0, 0 font "" norotate
set timestamp bottom 
set timestamp "" 
set timestamp  offset character 0, 0, 0 font "" norotate
set rrange [ * : * ] noreverse nowriteback  # (currently [8.98847e+307:-8.98847e+307] )
set trange [ * : * ] noreverse nowriteback  # (currently [-5.00000:5.00000] )
set urange [ * : * ] noreverse nowriteback  # (currently [-10.0000:10.0000] )
set vrange [ * : * ] noreverse nowriteback  # (currently [-10.0000:10.0000] )
set xlabel "" 
set xlabel  offset character 0, 0, 0 font "" textcolor lt -1 norotate
set x2label "" 
set x2label  offset character 0, 0, 0 font "" textcolor lt -1 norotate
set xrange [ * : * ] noreverse nowriteback  # (currently [1.00000:5.00000] )
set x2range [ * : * ] noreverse nowriteback  # (currently [1.00000:5.00000] )
set ylabel "" 
set ylabel  offset character 0, 0, 0 font "" textcolor lt -1 rotate by -270
set y2label "" 
set y2label  offset character 0, 0, 0 font "" textcolor lt -1 rotate by -270
set yrange [ * : * ] noreverse nowriteback  # (currently [10.0000:100.000] )
set y2range [ * : * ] noreverse nowriteback  # (currently [17.1312:95.0433] )
set zlabel "" 
set zlabel  offset character 0, 0, 0 font "" textcolor lt -1 norotate
set zrange [ * : * ] noreverse nowriteback  # (currently [-10.0000:10.0000] )
set cblabel "" 
set cblabel  offset character 0, 0, 0 font "" textcolor lt -1 rotate by -270
set cbrange [ * : * ] noreverse nowriteback  # (currently [8.98847e+307:-8.98847e+307] )
set zero 1e-008
set lmargin  -1
set bmargin  -1
set rmargin  -1
set tmargin  -1
#set locale "Polish_Poland.1250"
set pm3d explicit at s
set pm3d scansautomatic
set pm3d interpolate 1,1 flush begin noftriangles nohidden3d corners2color mean
set palette positive nops_allcF maxcolors 0 gamma 1.5 color model RGB 
set palette rgbformulae 7, 5, 15
set colorbox default
set colorbox vertical origin screen 0.9, 0.2, 0 size screen 0.05, 0.6, 0 front bdefault
set loadpath 
set fontpath 
set fit noerrorvariables
GNUTERM = "wxt"
i = 5
f = ""
cd "results"
set terminal pdf
set xlabel "instance"
set xrange [0:12]
set xtics rotate by 45 
set xtics out
set xtics offset -0.75,-1
set key box
files = "random.dat heuristic.dat greedy.dat steepest.dat"

set output "quality.pdf"
set ylabel "Quality"
set key right bottom
plot for [f in files] f using 1:5:6:xticlabels(2) with yerrorlines title f  
unset output

set output "effectivenes.pdf"
set ylabel "Effectiveness"
plot for [f in files] f using 1:4:xticlabels(2) with linespoints title f   
unset output

set output "best_quality.pdf"
set ylabel "Best Quality"
plot for [f in files] f using 1:3:xticlabels(2) with linespoints title f  
unset output

set output "time.pdf"
set ylabel "Time"
set key left top
plot for [f in files] f using 1:7:xticlabels(2) with linespoints title f   
unset output

set key left top box
set yrange [0:1]

set output "binary_similarity.pdf"
set ylabel "Binary Similarity"
plot for [f in "greedy steepest"] f.".dat" using 1:8:xticlabels(2) title f   
unset output

set output "partial_similarity.pdf"
set ylabel "Partial Similarity"
plot for [f in "greedy steepest"] f.".dat" using 1:9:xticlabels(2) title f   
unset output

set xtics norotate
set xtics nooffset 
unset yrange

set yrange[0:105]
set xrange[0:105]
set ylabel "End quality"
set xlabel "Startpoint quality"
set nokey

set output "gs_comparision_nug30.pdf"
 plot "gs_comparision_nug30.dat" using 1:2 notitle
 unset output

set output "gs_comparision_kra30a.pdf"
 plot "gs_comparision_kra30a.dat" using 1:2 notitle
 unset output

set output "gs_comparision_nug24.pdf"
 plot "gs_comparision_nug24.dat" using 1:2 notitle
 unset output

set output "gs_comparision_had16.pdf"
 plot "gs_comparision_had16.dat" using 1:2 notitle
 unset output

set output "gs_comparision_had20.pdf"
 plot "gs_comparision_had20.dat" using 1:2 notitle
 unset output

set output "gs_comparision_bur26a.pdf"
 plot "gs_comparision_bur26a.dat" using 1:2 notitle
 unset output

set output "gs_comparision_rou20.pdf"
 plot "gs_comparision_rou20.dat" using 1:2 notitle
 unset output

set output "gs_comparision_lipa40a.pdf"
 plot "gs_comparision_lipa40a.dat" using 1:2 notitle
 unset output

set output "gs_comparision_esc16a.pdf"
 plot "gs_comparision_esc16a.dat" using 1:2 notitle
 unset output

set output "gs_comparision_chr12a.pdf"
 plot "gs_comparision_chr12a.dat" using 1:2 notitle
 unset output

set key right bottom
set ylabel "Quality"
set xlabel "Number of restarts"

set output "multirandom_kra30a.pdf"
 plot "multirandom_kra30a.dat" using 1:2 title columnheader, "multirandom_kra30a.dat" using 1:3 title columnheader, "multirandom_kra30a.dat" using 1:4 title columnheader with linespoints
 unset output

set output "multirandom_nug24.pdf"
 plot "multirandom_nug24.dat" using 1:2 title columnheader, "multirandom_nug24.dat" using 1:3 title columnheader, "multirandom_nug24.dat" using 1:4 title columnheader with linespoints
 unset output

set output "multirandom_had16.pdf"
 plot "multirandom_had16.dat" using 1:2 title columnheader, "multirandom_had16.dat" using 1:3 title columnheader, "multirandom_had16.dat" using 1:4 title columnheader with linespoints
 unset output

set output "multirandom_had20.pdf"
 plot "multirandom_had20.dat" using 1:2 title columnheader, "multirandom_had20.dat" using 1:3 title columnheader, "multirandom_had20.dat" using 1:4 title columnheader with linespoints
 unset output

set output "multirandom_bur26a.pdf"
 plot "multirandom_bur26a.dat" using 1:2 title columnheader, "multirandom_bur26a.dat" using 1:3 title columnheader, "multirandom_bur26a.dat" using 1:4 title columnheader with linespoints
 unset output

set output "multirandom_rou20.pdf"
 plot "multirandom_rou20.dat" using 1:2 title columnheader, "multirandom_rou20.dat" using 1:3 title columnheader, "multirandom_rou20.dat" using 1:4 title columnheader with linespoints
 unset output

set output "multirandom_lipa40a.pdf"
 plot "multirandom_lipa40a.dat" using 1:2 title columnheader, "multirandom_lipa40a.dat" using 1:3 title columnheader, "multirandom_lipa40a.dat" using 1:4 title columnheader with linespoints
 unset output

set output "multirandom_esc16a.pdf"
 plot "multirandom_esc16a.dat" using 1:2 title columnheader, "multirandom_esc16a.dat" using 1:3 title columnheader, "multirandom_esc16a.dat" using 1:4 title columnheader with linespoints
 unset output

set output "multirandom_chr12a.pdf"
 plot "multirandom_chr12a.dat" using 1:2 title columnheader, "multirandom_chr12a.dat" using 1:3 title columnheader, "multirandom_chr12a.dat" using 1:4 title columnheader with linespoints
 unset output

set output "multirandom_nug30.pdf"
 plot "multirandom_nug30.dat" using 1:2 title columnheader, "multirandom_nug30.dat" using 1:3 title columnheader, "multirandom_nug30.dat" using 1:4 title columnheader with linespoints 
 unset output


#    EOF
