import requests
from bs4 import BeautifulSoup
import csv

# List of symbols to search for
symbols = [
    "ACLBSL", "ADBL", "ADBLD83", "AHL", "AHPC", "AKJCL", "AKPL", "ALBSL", "ALICL", "ANLB", 
    "API", "AVYAN", "BARUN", "BBC", "BEDC", "BFC", "BGWT", "BHDC", "BHL", "BHPL", 
    "BNHC", "BNL", "BNT", "BOKD86", "BPCL", "C30MF", "CBBL", "CBLD88", "CCBD88", "CFCL", 
    "CGH", "CHCL", "CHDC", "CHL", "CIT", "CITY", "CIZBD90", "CKHL", "CLI", "CMF1", 
    "CMF2", "CORBL", "CYCL", "CZBIL", "DDBL", "DHPL", "DLBS", "DOLTI", "DORDI", "EBL", 
    "EBLD85", "EBLD86", "EDBL", "EHPL", "ENL", "FMDBL", "FOWAD", "GBBD85", "GBBL", "GBILD86/87", 
    "GBIME", "GBLBS", "GCIL", "GFCL", "GHL", "GIBF1", "GILB", "GLBSL", "GLH", "GMFBS", 
    "GMFIL", "GRDBL", "GUFL", "GVL", "H8020", "HATHY", "HBL", "HBLD83", "HDHPC", "HDL", 
    "HEI", "HEIP", "HHL", "HIDCL", "HIDCLP", "HLBSL", "HLI", "HPPL", "HRL", "HURJA", 
    "ICFC", "ICFCD83", "IGI", "IHL", "ILBS", "ILI", "JBBD87", "JBBL", "JBLB", "JFL", 
    "JOSHI", "JSLBB", "KBL", "KBSH", "KDBY", "KDL", "KEF", "KKHC", "KMCDB", "KPCL", 
    "KRBL", "KSBBL", "KSBBLD87", "KSY", "LBBL", "LBBLD89", "LBLD86", "LEC", "LICN", "LLBS", 
    "LSL", "LUK", "LVF2", "MAKAR", "MANDU", "MBJC", "MBL", "MBLD87", "MCHL", "MDB", 
    "MEHL", "MEL", "MEN", "MERO", "MFIL", "MFLD85", "MHCL", "MHL", "MHNL", "MKCL", 
    "MKHC", "MKHL", "MKJC", "MLBBL", "MLBL", "MLBS", "MLBSL", "MMF1", "MMKJL", "MNBBL", 
    "MND84/85", "MPFL", "MSHL", "MSLB", "NABBC", "NABIL", "NABILD87", "NADEP", "NBF2", "NBF3", 
    "NBL", "NBLD85", "NBLD87", "NESDO", "NFS", "NGPL", "NHDL", "NHPC", "NIBD84", "NIBLGF", 
    "NIBLSTF", "NIBSF2", "NICA", "NICAD8182", "NICAD85/86", "NICBF", "NICD88", "NICFC", "NICGF", "NICGF2", 
    "NICL", "NICLBSL", "NICSF", "NIFRA", "NIFRAUR85/86", "NIL", "NIMB", "NIMBD90", "NIMBPO", "NLG", 
    "NLIC", "NLICL", "NMB", "NMB50", "NMBMF", "NMFBS", "NMLBBL", "NRIC", "NRM", "NRN", 
    "NSIF2", "NTC", "NUBL", "NWCL", "NYADI", "OHL", "PBD84", "PBD85", "PBD88", "PCBL", 
    "PFL", "PHCL", "PMHPL", "PMLI", "PMLIP", "PPCL", "PPL", "PRIN", "PROFL", "PRSF", 
    "PRVU", "PSF", "RADHI", "RAWA", "RBBD83", "RBCL", "RBCLPO", "RFPL", "RHGCL", "RHPL", 
    "RIDI", "RLFL", "RMF1", "RMF2", "RNLI", "RSDC", "RURU", "SADBL", "SAEF", "SAGF", 
    "SAHAS", "SALICO", "SAMAJ", "SAND2085", "SANIMA", "SAPDBL", "SARBTM", "SBCF", "SBD87", "SBI", 
    "SBID83", "SBID89", "SBL", "SBLD2082", "SBLD84", "SBLD89", "SCB", "SEF", "SFCL", "SFEF", 
    "SFMF", "SGHC", "SGIC", "SHEL", "SHINE", "SHIVM", "SHL", "SHLB", "SHPC", "SICL", 
    "SIFC", "SIGS2", "SIGS3", "SIKLES", "SINDU", "SJCL", "SJLIC", "SKBBL", "SLBBL", "SLBSL", 
    "SLCF", "SMATA", "SMB", "SMFBS", "SMH", "SMHL", "SMJC", "SNLI", "SONA", "SPC", 
    "SPDL", "SPHL", "SPIL", "SPL", "SRBLD83", "SRLI", "SSHL", "STC", "SWBBL", "SWMF", 
    "TAMOR", "TPC", "TRH", "TSHL", "TVCL", "UAIL", "UHEWA", "ULBSL", "ULHC", "UMHL", 
    "UMRH", "UNHPL", "UNL", "UNLB", "UPCL", "UPPER", "USHEC", "USHL", "USLB", "VLBS", 
    "VLUCL", "WNLB"
]

# Base URL
base_url = 'https://merolagani.com/CompanyDetail.aspx?symbol='

# Initialize a list to store all the data
all_data = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
# Iterate over the symbols and fetch the data for each one
for symbol in symbols:
    url = f"{base_url}{symbol}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize a dictionary to store the data for each symbol
    data = {'Symbol': symbol}

    # Extract the specific values based on the <th> text
    rows = soup.find_all('tr')
    for row in rows:
        th = row.find('th')
       
        td = row.find('td')
        if th and td:
            header = th.text.strip()
            value = td.text.strip()
            if header in ["1 Year Yield", "EPS", "P/E Ratio", "Book Value", "PBV", "% Dividend", "% Bonus", "Right Share"]:
                data[header] = value

    # Append the data dictionary to the list
    all_data.append(data)

# Define the CSV file name
file_name = 'company_data_transposed.csv'

# Write the data to a CSV file in transposed form
with open(file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write headers (including Symbol)
    headers = ["Symbol", "1 Year Yield", "EPS", "P/E Ratio", "Book Value", "PBV", "% Dividend", "% Bonus", "Right Share"]
    writer.writerow(headers)
    
    # Write data rows
    for data in all_data:
        row = [data.get(header, '') for header in headers]
        writer.writerow(row)

print(f"Data saved to {file_name}")

#  import requests
# from bs4 import BeautifulSoup
# import csv

# # Define the URL
# url = 'https://merolagani.com/CompanyDetail.aspx?symbol=CGH'

# # Define the headers to mimic a browser request
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
# }

# # Send the request
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, 'html.parser')

# # Initialize a dictionary to store the data
# data = {}

# # Extract the specific values based on the <th> text
# rows = soup.find_all('tr')
# for row in rows:
#     th = row.find('th')
#     td = row.find('td')
#     if th and td:
#         header = th.text.strip()
#         value = td.text.strip()
#         if header in ["1 Year Yield", "EPS", "P/E Ratio", "Book Value", "PBV", "% Dividend", "% Bonus", "Right Share"]:
#             data[header] = value

# # Print the extracted data
# print(data)

# # Save the data to a CSV file in transposed form
# file_name = 'company_data_transposed.csv'

# # Write the data to a CSV file in transposed form
# with open(file_name, mode='w', newline='') as file:
#     writer = csv.writer(file)
    
#     # Write headers
#     writer.writerow(data.keys())
    
#     # Write values
#     writer.writerow(data.values())

# print(f"Data saved to {file_name}")

#  import requests
# from  bs4 import BeautifulSoup

# url = 'https://merolagani.com/CompanyDetail.aspx?symbol=CGH'
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, 'html.parser')


# data = {}

# # Extract the specific values based on the <th> text
# rows = soup.find_all('tr')
# for row in rows:
#     th = row.find('th')
#     td = row.find('td')

#     if th and td:
#         header = th.text.strip()
#         value = td.text.strip()
#         if header in ["1 Year Yield", "EPS", "P/E Ratio", "Book Value", "PBV""% Dividend", "% Bonus", "Right Share"]:
#             data[header] = value

# print(data)

# import csv

# # Define the file name
# file_name = 'company_data_app.csv'

# # Write the data to a CSV file
# with open(file_name, mode='w', newline='') as file:
#     writer = csv.writer(file)
    
#     # Write headers
#     writer.writerow(data.keys())
    
#     # Write values
#     writer.writerow(data.values())

# print(f"Data saved to {file_name}")
# print(soup.prettify())
# text-decrease,text-primary,
# span = soup.find(class_="panel panel-default")
# print(span)
# ACLBSL, ADBL, ADBLD83, AHL, AHPC, AKJCL, AKPL, ALBSL, ALICL, ANLB, API, AVYAN, BARUN, BBC, BEDC, BFC, BGWT, BHDC, BHL, BHPL, BNHC, BNL, BNT, BOKD86, BPCL, C30MF, CBBL, CBLD88, CCBD88, CFCL, CGH, CHCL, CHDC, CHL, CIT, CITY, CIZBD90, CKHL, CLI, CMF1, CMF2, CORBL, CYCL, CZBIL, DDBL, DHPL, DLBS, DOLTI, DORDI, EBL, EBLD85, EBLD86, EDBL, EHPL, ENL, FMDBL, FOWAD, GBBD85, GBBL, GBILD86/87, GBIME, GBLBS, GCIL, GFCL, GHL, GIBF1, GILB, GLBSL, GLH, GMFBS, GMFIL, GRDBL, GUFL, GVL, H8020, HATHY, HBL, HBLD83, HDHPC, HDL, HEI, HEIP, HHL, HIDCL, HIDCLP, HLBSL, HLI, HPPL, HRL, HURJA, ICFC, ICFCD83, IGI, IHL, ILBS, ILI, JBBD87, JBBL, JBLB, JFL, JOSHI, JSLBB, KBL, KBSH, KDBY, KDL, KEF, KKHC, KMCDB, KPCL, KRBL, KSBBL, KSBBLD87, KSY, LBBL, LBBLD89, LBLD86, LEC, LICN, LLBS, LSL, LUK, LVF2, MAKAR, MANDU, MBJC, MBL, MBLD87, MCHL, MDB, MEHL, MEL, MEN, MERO, MFIL, MFLD85, MHCL, MHL, MHNL, MKCL, MKHC, MKHL, MKJC, MLBBL, MLBL, MLBS, MLBSL, MMF1, MMKJL, MNBBL, MND84/85, MPFL, MSHL, MSLB, NABBC, NABIL, NABILD87, NADEP, NBF2, NBF3, NBL, NBLD85, NBLD87, NESDO, NFS, NGPL, NHDL, NHPC, NIBD84, NIBLGF, NIBLSTF, NIBSF2, NICA, NICAD8182, NICAD85/86, NICBF, NICD88, NICFC, NICGF, NICGF2, NICL, NICLBSL, NICSF, NIFRA, NIFRAUR85/86, NIL, NIMB, NIMBD90, NIMBPO, NLG, NLIC, NLICL, NMB, NMB50, NMBMF, NMFBS, NMLBBL, NRIC, NRM, NRN, NSIF2, NTC, NUBL, NWCL, NYADI, OHL, PBD84, PBD85, PBD88, PCBL, PFL, PHCL, PMHPL, PMLI, PMLIP, PPCL, PPL, PRIN, PROFL, PRSF, PRVU, PSF, RADHI, RAWA, RBBD83, RBCL, RBCLPO, RFPL, RHGCL, RHPL, RIDI, RLFL, RMF1, RMF2, RNLI, RSDC, RURU, SADBL, SAEF, SAGF, SAHAS, SALICO, SAMAJ, SAND2085, SANIMA, SAPDBL, SARBTM, SBCF, SBD87, SBI, SBID83, SBID89, SBL, SBLD2082, SBLD84, SBLD89, SCB, SEF, SFCL, SFEF, SFMF, SGHC, SGIC, SHEL, SHINE, SHIVM, SHL, SHLB, SHPC, SICL, SIFC, SIGS2, SIGS3, SIKLES, SINDU, SJCL, SJLIC, SKBBL, SLBBL, SLBSL, SLCF, SMATA, SMB, SMFBS, SMH, SMHL, SMJC, SNLI, SONA, SPC, SPDL, SPHL, SPIL, SPL, SRBLD83, SRLI, SSHL, STC, SWBBL, SWMF, TAMOR, TPC, TRH, TSHL, TVCL, UAIL, UHEWA, ULBSL, ULHC, UMHL, UMRH, UNHPL, UNL, UNLB, UPCL, UPPER, USHEC, USHL, USLB, VLBS, VLUCL, WNLB

# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# # Base URL for the product details
# base_url = 'https://merolagani.com/CompanyDetail.aspx?symbol=CGH'

# # URL to fetch the main page containing the dropdown
# # dropdown_url = 'https://merolagani.com/CompanyList.aspx'
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# # Fetch the main page and parse it
# response = requests.get(base_url, headers=headers)
# soup = BeautifulSoup(response.text, 'html.parser')

# # Find the dropdown containing the product symbols
# dropdown = soup.find('select', {'id':"ctl00_Panel1"})
# print(dropdown)
# Extract all options (symbols) from the dropdown
# options = dropdown.find_all('option')

# # List to store product details
# product_details = []

# # Iterate over each option (symbol)
# for option in options:
#     symbol = option['value']
#     if symbol:  # Skip if the value is empty
#         product_url = base_url + symbol
#         response = requests.get(product_url, headers=headers)
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         # Extract the product details (customize based on the actual structure of the product details page)
#         product_name = soup.find('span', class_='company-name').text.strip()
#         product_price = soup.find('span', class_='text-increase').text.strip()
        
#         # Append the details to the list
#         product_details.append({'Symbol': symbol, 'Name': product_name, 'Price': product_price})

# # Create a DataFrame from the list
# df = pd.DataFrame(product_details)

# # Save the DataFrame to a CSV file
# df.to_csv('product_details.csv', index=False)

# print("Product details saved to product_details.csv")
