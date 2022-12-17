cat allclusterRankedPheno_0.0005.txt > dbgwas_data.csv 
rm converted_data.csv
rm converted_text.txt
python3 convertcsv.py
cat converted_data.csv > converted_text.txt
