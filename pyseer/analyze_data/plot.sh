cat <(paste <(sed '1d' assoc.out | cut -d "_" -f 3) \
<(sed '1d' assoc.out | cut -f 3) | \
awk '{p = -log($2)/log(10); print $1,p}' ) | \
tr ' ' '\t' > manhattan.plot

