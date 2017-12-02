import driver

def operationToRegions(operation):
    #Accepts a medical operation and returns the price ranges for each region
    regions = {'NA': (100, 10000), 'SA': (1, 5), 'CA': (50, 100), 'CB': (25, 50)}
    for region in driver.regions:

    return regions