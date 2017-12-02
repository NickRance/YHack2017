import numpy as np
import csv, sys

###Constants###
centralAmericaDestinations = {'Mexico': ['CUN', 'MEX'], 'Costa Rica': ['SJO', 'LIR']}
southAmericaDestinations = {'Colombia': ['BOG', 'CTG', 'MDE'], 'Peru': ['LIM'], 'Ecuador': ['UIO']}
caribbeanDestinations = {'Puerto Rico': ['BQN', 'PSE', 'SJU'], 'Antigua and Barbuda': ['ANU'], 'Aruba': ['AUA'],
                  'Bahamas': ['NAS'], 'Bermuda': ['BDA'], 'Barbados': ['BGI'], 'Cuba': ['CMW', 'HAV', 'HOG', 'SNU'],
                  'Curacao': ['CUR'], 'Cayman Islands': ['GCM'],
                  'Dominican Republic': ['LRM', 'POP', 'PUJ', 'STI', 'SDQ'], 'Grenada': ['GND'],
                  'Jamaica': ['KIN', 'MBJ'], 'Haiti': ['PAP'], 'Trinidad & Tobago': ['POS'],
                  'Turks and Caicos Islands': ['PLS'], 'St. Croix': ['STX'], 'St. Lucia': ['UVF'],
                  'St. Maarten': ['SXM'], 'St. Thomas': ['STT']}

medicalProcedures = {'Heart Bypass':{'USA':123000,'Costa Rica':27000,'Colombia':14800,'Mexico':27000}
,'Angioplasty':{'USA':28000, 'Costa Rica':13800, 'Colombia':7100, 'Mexico':10400}
,'Heart Valve Replacement':{'USA':170000, 'Costa Rica':30000, 'Colombia':10450, 'Mexico':28200}
,'Hip Replacement':{'USA':40364, 'Costa Rica':13600, 'Colombia':8400, 'Mexico':13500},
'Hip Resurfacing':{'USA':28000, 'Costa Rica':13200, 'Colombia':10500, 'Mexico':12500},
'Knee Replacement':{'USA':35000, 'Costa Rica':12500, 'Colombia':12900, 'Mexico':6600},
'Spinal Fusion':{'USA':110000, 'Costa Rica':15700, 'Colombia':14500, 'Mexico':15400},
'Dental Implant':{'USA':2500, 'Costa Rica':800, 'Colombia':1200, 'Mexico':900},
'Lap Band':{'USA':14000, 'Costa Rica':9450, 'Colombia':8500, 'Mexico':6500},
'Gastric Sleeve': {'USA':16500, 'Costa Rica':11500, 'Colombia': 11200, 'Mexico':8900},
'Gastric Bypass': {'USA':25000, 'Costa Rica':12900, 'Colombia': 12200, 'Mexico':11500},
'Hysterectomy': {'USA':15400, 'Costa Rica':6900, 'Colombia': 2900, 'Mexico':4500},
'Breast Implants': {'USA':6400, 'Costa Rica':3500, 'Colombia':2500, 'Mexico':3800},
'Rhinoplasty': {'USA':6500, 'Costa Rica':3800, 'Colombia': 4500, 'Mexico':3800},
'Face Lift': {'USA':11000, 'Costa Rica':4500, 'Colombia': 4000, 'Mexico':4900},
'Liposuction':{'USA':5500, 'Costa Rica':2800, 'Colombia': 2500, 'Mexico':3000},
'Tummy Tuck':{'USA':8000, 'Costa Rica':5000, 'Colombia': 3500, 'Mexico':4500},
'Lasik (both eyes)':{'USA':4000, 'Costa Rica':2400, 'Colombia':2400, 'Mexico':1900},
'Cornea(per eye)':{'USA':17500, 'Costa Rica':9800, 'Colombia':None, 'Mexico':None},
'Cataract Surgery (per eye)': {'USA': 3500, 'Costa Rica': 1700, 'Colombia': 1600, 'Mexico':2100},
'IVF Treatment':{'USA':12400, 'Costa Rica': None, 'Colombia': 5540, 'Mexico': 5000}}

def main():
    operation = getargs()
    deals = readDataSetFile('./data/Deals.csv')
    # fares = readDataSetFile('./data/LowestFares.csv')
    destinations = {**centralAmericaDestinations, **southAmericaDestinations, **caribbeanDestinations}
    destination,cost = getDestination(operation)
    airports = countryToAirports(destination)
    print("Operation: %s" % (operation))
    print("Destination: %s"% (destination))
    print("Operation Cost: %s"% (cost))
    # print("Airports: %s"% (airports))
    originAirport = 'JFK'
    matches = []
    for row in deals:
        if row[1]==originAirport and row[2] in airports:
            matches.append(row)
    sorted(matches, key=lambda match:match[7])
    # matches = np.ndarray.sort(np.asarray(matches), axis=7)
    print('Destination Airport: %s' % (matches[0][2]))
    print('Flight Cost: %s' % (matches[0][7]))
    print('Flight Time: %s' % (matches[0][3]))
    print('Amount Saved: %s' % (medicalProcedures[operation]['USA'] - (cost + float(matches[0][7]) ) ))

def readDataSetFile(filename):
    #Had to do this because some column error. It was splitting the weekdays field because there
    output = []
    with open(filename,'r') as fp:
        reader = csv.reader(fp)
        next(reader, None)
        for row in reader:
            output.append(row)
    return np.asarray(output)

def getDestination(procedure):
    cheapest = min(medicalProcedures[procedure])
    return cheapest, medicalProcedures[procedure][cheapest]

def countryToAirports(country):
    for region in [centralAmericaDestinations,southAmericaDestinations,caribbeanDestinations]:
        if country in region:
            return region[country]

def getargs():
   return sys.argv[1]

if __name__ == '__main__':
    main()