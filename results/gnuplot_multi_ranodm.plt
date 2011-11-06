set ylabel "Quality"
set xlabel "Number of restarts"

set output "multirandom_nug30.pdf"
 plot "multirandom_nug30.dat" using 1:2 title columnheader, "multirandom_nug30.dat" using 1:3 title columnheader
 unset output

set output "multirandom_kra30a.pdf"
 plot "multirandom_kra30a.dat" using 1:2 title columnheader, "multirandom_kra30a.dat" using 1:3 title columnheader
 unset output

set output "multirandom_nug24.pdf"
 plot "multirandom_nug24.dat" using 1:2 title columnheader, "multirandom_nug24.dat" using 1:3 title columnheader
 unset output

set output "multirandom_had16.pdf"
 plot "multirandom_had16.dat" using 1:2 title columnheader, "multirandom_had16.dat" using 1:3 title columnheader
 unset output

set output "multirandom_had20.pdf"
 plot "multirandom_had20.dat" using 1:2 title columnheader, "multirandom_had20.dat" using 1:3 title columnheader
 unset output

set output "multirandom_bur26a.pdf"
 plot "multirandom_bur26a.dat" using 1:2 title columnheader, "multirandom_bur26a.dat" using 1:3 title columnheader
 unset output

set output "multirandom_rou20.pdf"
 plot "multirandom_rou20.dat" using 1:2 title columnheader, "multirandom_rou20.dat" using 1:3 title columnheader
 unset output

set output "multirandom_lipa40a.pdf"
 plot "multirandom_lipa40a.dat" using 1:2 title columnheader, "multirandom_lipa40a.dat" using 1:3 title columnheader
 unset output

set output "multirandom_esc16a.pdf"
 plot "multirandom_esc16a.dat" using 1:2 title columnheader, "multirandom_esc16a.dat" using 1:3 title columnheader
 unset output

set output "multirandom_chr12a.pdf"
 plot "multirandom_chr12a.dat" using 1:2 title columnheader, "multirandom_chr12a.dat" using 1:3 title columnheader
 unset output

