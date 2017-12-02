import numpy as np
import csv, sys, json, operator

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

def readProcedurePrices():
    with open('operations.json') as fp:
        return(json.load(fp))

medicalProcedures = readProcedurePrices()
# print(medicalProcedures)

def formatCurrency(currencyStr):
    # I truncate the medical procedures figure to get rid of $ sign
    return float(currencyStr.strip('$').replace(",", ''))

def main():
    operation = getargs()
    # fares = readDataSetFile('./data/LowestFares.csv')
    # destinations = {**centralAmericaDestinations, **southAmericaDestinations, **caribbeanDestinations}
    destinations = getCheapestDestination(operation)
    flights = generateDestinations(destinations,operation)
    printDestinations(flights,operation)
    # print(destination)

def findFlightPrices(origin,destinationAirports):
    if not destinationAirports:
        return False
    deals = readDataSetFile('./data/Deals.csv')
    matches = []
    for row in deals:
        # print(row)
        if row[1] == origin and row[2] in destinationAirports:
            matches.append(row)
    return(sorted(matches, key=lambda match: match[7]))
    # matches = np.ndarray.sort(np.asarray(matches), axis=7)
    # return(matches[0])

def generateDestinations(destinations,operation):
    output = []
    i = 1
    j = 1
    topN = 5
    visited = set()
    while i <= topN:
        if j >= len(destinations):
            return False
        d = destinations[j]
        destination = d[0]
        cost = d[1]
        destination = airportsToCountry(destination)
        airports = countryToAirports(destination)
        matches = findFlightPrices('JFK', airports)
        if matches and destination not in visited:
            visited.add(destination)
            USACost = formatCurrency(medicalProcedures[operation]['JFK'])
            cost = formatCurrency(cost)
            saved = USACost - (cost + float(matches[0][7]))
            match = {'destination':destination, 'opCost': cost, 'airports':airports,'destAirport':matches[0][2], 'flightCost':matches[0][7], 'flightTime': matches[0][3], 'amtSaved':saved}
            output.append(match)
            i += 1
        j += 1
    return output

def printDestinations(flightOptions,operation):
    print("Operation: %s" % (operation))
    for i, flight in enumerate(flightOptions):
        print("\n===== Rank %i =====" % (i+1))
        print("Destination: %s" % (flight['destination']))
        print("Operation Cost: %s" % (flight['opCost']))
        print("Airports: %s" % (flight['airports']))
        print('Destination Airport: %s' % (flight['destAirport']))
        print('Flight Cost: %s' % (flight['flightCost']))
        print('Flight Time: %s' % (flight['flightTime']))
        print('Amount Saved: %.2f' % (flight['amtSaved']))


def readDataSetFile(filename):
    #Had to do this because some column error. It was splitting the weekdays field because there
    output = []
    with open(filename,'r') as fp:
        reader = csv.reader(fp)
        next(reader, None)
        for row in reader:
            output.append(row)
    return np.asarray(output)

def getCheapestDestination(procedure):
    # print(medicalProcedures[procedure])
    # topN = 5
    cheapest  = sorted(medicalProcedures[procedure].items(), key=lambda x:float(x[1]))
    return cheapest
    # cheapest = min(medicalProcedures[procedure])
    # return cheapest, medicalProcedures[procedure][cheapest]

def countryToAirports(country):
    for region in [centralAmericaDestinations, southAmericaDestinations, caribbeanDestinations]:
        if country in region:
            return region[country]
    return False

def airportsToCountry(airport):
    for region in [centralAmericaDestinations, southAmericaDestinations, caribbeanDestinations]:
        for country,countryAirports in region.items():
            if airport in countryAirports:
                return country
    return False



def getargs():
   return sys.argv[1]

if __name__ == '__main__':
    main()