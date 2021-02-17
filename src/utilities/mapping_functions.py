import csv
import sys
import numpy as np

project_directory = 'C:/Users/dtwiz/Documents/GitHub/Twitter-data-collector/'#Must be changed to your projectdirectory

# settings = {
#     'inputPath' : 'data\\KRAKEN_XRPUSD, 1D.csv',
#     'outPath' : 'XRP_ROI_1_Day',
#     'asset' : 'XRP',
#     'quote' : 'USD',
#     'cTime' : 1,
#     'cUnit' : 'D',#D for day
#     'function' : 'ROIInNCandles',
#     'params' : {'nCandles' : 7}
# }

settings = {
    'inputPath': project_directory + 'data\\ETH_1_Minute_COMP.csv',
    'outPath': project_directory + 'data\\ETH_1_Minute_COMP.csv',
    'asset': 'ETH',
    'quote': 'USD',
    'cTime': 1,
    'cUnit': 'm',  #D for day
    'function': 'combineData',
    'params': {
        'addPath' : project_directory + 'data\\ETH_volRatio_1_Minute.csv'
    }
}


# settings = {
#     'inputPath': project_directory + 'data/KRAKEN_XRPUSD, 1D.csv',
#     'outPath': project_directory + 'data/KRAKEN_XRPUSD, 1D COMP.csv',
#     'asset': 'XRP', #the asset being traded
#     'quote': 'USD', #the currency that the price is given in
#     'cTime': 1, #number of units of time in each time step
#     'cUnit': 'D',  #m for minute and D for day
#     'function': 'combineData',
#     'params': {
#         'addPath' : project_directory + 'data/XRP_ext_1_Day.csv',
#     }
# }

def dataMaker(inData, mapFunction):  #map functions take in a list of dictionaries and output a list of dictionaries
    return mapFunction(inData)


def saveData(data, fields, name):  #save 2d list as a csv
    with open(name, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(fields)
        writer.writerows(data)

def saveCSV(data, path):
    with open(path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, data[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(data)

def ROIInNCandles(data):
    outData = []
    nCandles = settings['params']['nCandles']
    for x in range(len(data)):
        outData.append([None])
    initPrices = []
    pricesIndex = 0  #index for circular indexing
    for x in range(nCandles):
        initPrices.append(float(data[x]['close']))
    for x in range(len(data) - nCandles):
        index = x + nCandles
        close = float(data[index]['close'])
        initPrice = initPrices[pricesIndex]
        outData[x][0] = close / initPrice - 1  #long roi
        initPrices[pricesIndex] = close
        pricesIndex += 1
        if pricesIndex >= nCandles:
            pricesIndex = 0
    return outData


def volume(data):
    outData = []
    for x in range(len(data)):
        outData.append(data[x]['vol'])
    return outData


def avgVolume(data):
    outData = []
    avgCandles = settings['params']['avgCandles']
    avgVols = []
    for x in range(avgCandles):
        outData.append([None])
        avgVols.append(float(data[x]['vol']))
    for x in range(len(data) - avgCandles):
        index = x + avgCandles
        outData.append([sum(avgVols) / len(avgVols)])
        avgVols[x % avgCandles] = float(data[index]['vol'])
    return outData

def stripData(data):
    outData = []
    for x in range(len(data)):
        temp = [data[x]['time'], data[x]['open'],data[x]['high'],data[x]['low'],data[x]['close'],data[x]['vol']]
        # temp = {
        #     'time' : data[x]['time'],
        #     'open': data[x]['open'],
        #     'high': data[x]['high'],
        #     'low': data[x]['low'],
        #     'close': data[x]['close'],
        #     'vol': data[x]['vol']
        # }
        outData.append(temp)
    return outData

def combineData(data):
    addData = loadData(settings['params']['addPath'])
    data = loadData(settings['inputPath'])
    for x in range(len(data)):
        for y in addData[0].keys():
            data[x][y] = addData[x][y]
    return data

def avgVolumeRatio(data):
    outData = []
    avgCandles = settings['params']['avgCandles']
    avgVols = avgVolume(data)
    for x in range(avgCandles):
        outData.append([None])
    for x in range(len(data) - avgCandles):
        index = x + avgCandles
        vol = float(data[index]['vol'])
        if abs(avgVols[index][0]) <= 0.00001:
            outData.append([50])#to avoid divide by zero add a large value
        else:
            outData.append([vol / avgVols[index][0]])
    return outData


def MA(data):
    outData = []
    period = settings['params']['period']
    for x in range(len(data)):
        outData.append([None])
    for x in range(len(data) - (period - 1)):
        index = x + (period - 1)
        ma = 0
        for y in range(period):
            ma += float(data[index - y]['close'])
        ma /= period
        outData[index][0] = ma
    return outData


def perATH(data):
    outData = []
    for x in range(len(data)):
        outData.append([None])
    pair = settings['asset'] + settings['quote']
    ath = 0
    aths = {'XRPUSD': 0.37175, 'XBTUSD': 19947.5, 'ETHUSD': 3}
    if pair in aths:
        ath = aths[pair]
    for x in range(len(data)):
        close = float(data[x]['close'])
        if close > ath:
            ath = close
            outData[x][0] = 1
        else:
            outData[x][0] = close / ath
    return outData


def extCandle(data):
    outData = []
    for x in range(len(data)):
        outData.append([None, None])
    highDict = {}
    lowDict = {}
    for x in range(len(data)):
        high = data[x]['high']
        low = data[x]['low']
        pops = []
        for top in highDict:  #check working tops to see if the new candle is higher
            if high > highDict[top][0]:
                outData[top] = highDict[top]
                pops.append(top)
            else:
                highDict[top][1] += 1
        for y in range(len(pops)):
            highDict.pop(pops[y])
        pops = []
        for bottom in lowDict:  #check working bottoms to see if the new candle is lower
            if low < lowDict[bottom][0]:
                if outData[bottom][1] != None and abs(
                        outData[bottom][1]) < abs(lowDict[bottom][1]):
                    outData[bottom] = lowDict[bottom]
                pops.append(bottom)
            else:
                lowDict[bottom][1] -= 1
        for y in range(len(pops)):
            lowDict.pop(pops[y])
        highDict[x] = [high, 0]
        lowDict[x] = [low, 0]
    return outData


def getCandles(self, asset, quote, cTime, cUnit, length):
    fileName = project_directory + "data/KRAKEN_" + asset + quote + ', '
    if cUnit == 'm':
        fileName += str(cTime) + '.csv'
    else:
        fileName += str(cTime) + cUnit + '.csv'
    tempArr = np.loadtxt(fileName,
                         delimiter=',',
                         skiprows=1,
                         usecols=(0, 1, 2, 3, 4, 5))
    candleList = []
    for x in range(len(tempArr)):
        candleList.append({
            'time': tempArr[x][0],
            'open': tempArr[x][1],
            'high': tempArr[x][2],
            'low': tempArr[x][3],
            'close': tempArr[x][4],
            'vol': tempArr[x][5]
        })
    return candleList[-length:]

def loadData(filename):
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        tempArr = list(reader)
    return tempArr

def getCandles(fileName):
    # tempArr = np.loadtxt(fileName,
    #                      delimiter=',',
    #                      skiprows=1,
    #                      usecols=(0, 1, 2, 3, 4, 5))
    candleList = []
    tempArr = loadData(fileName)
    for x in range(len(tempArr)):
        temp = {}
        if 'Unix Timestamp' in tempArr[x].keys():
            temp['time'] = tempArr[x]['Unix Timestamp']
        else:
            temp['time'] = tempArr[x]['time']
        if 'Open' in tempArr[x].keys():
            temp['open'] = tempArr[x]['Open']
        else:
            temp['open'] = tempArr[x]['open']
        if 'High' in tempArr[x].keys():
            temp['high'] = tempArr[x]['High']
        else:
            temp['high'] = tempArr[x]['high']
        if 'Low' in tempArr[x].keys():
            temp['low'] = tempArr[x]['Low']
        else:
            temp['low'] = tempArr[x]['low']
        if 'Close' in tempArr[x].keys():
            temp['close'] = tempArr[x]['Close']
        else:
            temp['close'] = tempArr[x]['close']
        if 'Volume' in tempArr[x].keys():
            temp['vol'] = tempArr[x]['Volume']
        else:
            temp['vol'] = tempArr[x]['vol']
        # candleList.append({
        #     'time': tempArr[x][0],
        #     'open': tempArr[x][1],
        #     'high': tempArr[x][2],
        #     'low': tempArr[x][3],
        #     'close': tempArr[x][4],
        #     'vol': tempArr[x][5]
        # })
        candleList.append(temp)
    return candleList

def combineFields(data):
    fields = []
    for y in data[0]:
        fields.append(y)
    return fields


nameToFuntion = {
    'extCandle': extCandle,
    'ROIInNCandles': ROIInNCandles,
    'MA': MA,
    'perATH': perATH,
    'avgVolumeRatio': avgVolumeRatio,
    'avgVolume': avgVolume,
    'volume': volume,
    'stripData' : stripData,
    'combineData': combineData
}

def nameToFields(name, data):
    if name == 'combineData':
        return combineFields(data)
    nameToFields = {
        'extCandle': ['extPrice', 'candles'],
        'ROIInNCandles': ['long roi'],
        'MA': ['MA'],
        'perATH': ['perATH'],
        'avgVolumeRatio': ['ratio'],
        'avgVolume': ['avgVol'],
        'volume': ['volume'],
        'stripData' : ['time', 'open', 'high', 'low', 'close', 'vol']
    }
    return nameToFields[name]

#Main code can be run by giving the input path and output file name in the
#command line when running this file or without which will use the default settings
if len(sys.argv) > 0:
    if len(sys.argv) > 1:
        inputPath = sys.argv[1]
    else:
        if settings['inputPath'] == None:
            inputPath = None
        else:
            inputPath = settings['inputPath']
    if len(sys.argv) > 2:
        outName = sys.argv[2]
    else:
        outName = settings['outPath']
    data = dataMaker(getCandles(inputPath),
                     nameToFuntion[settings['function']])
    if settings['function'] == 'combineData':
        saveCSV(data, outName)
    else:
        saveData(data, nameToFields(settings['function'], data), outName)
    print("File created and saved succesfully!")
