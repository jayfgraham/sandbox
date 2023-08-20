import tabula
import pandas as pd

tabula.read_pdf("Giselle_Amortization.pdf",pages='all')
tabula.convert_into("Giselle_Amortization.pdf","output.csv", output_format='csv',pages='all')
csv = pd.read_csv("GiselleAmortization.csv")
csv = pd.DataFrame(csv)

#
# tabula.read_pdf("Sample_Amortization.pdf",pages='all')
# tabula.convert_into("Sample_Amortization.pdf","SL_output.csv", output_format='csv',pages='all')
# csv = pd.read_csv("SL_output.csv")
# csv = pd.DataFrame(csv)
