# -*- coding:utf-8-*-
# extracting data from links that are in the index file
# and saving it to a CSV format
import requests,os, random,sys,getopt
from bs4 import BeautifulSoup
from time import sleep
import unicodecsv as csv

pageRoot = 'http://myfigurecollection.net/item/'

# WINDOWS PATHS!!!
root = 'D:\Dropbox\CS\MyFigureCollection\git'
indexPath = os.path.join(root,'pythia','data','index')
outputPath = os.path.join(root,'pythia','data','csv')
error_file = os.path.join(outputPath,'error_log.txt')

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Referer": "https://www.google.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive"}

csvHeader = ['#ID','Category', 'Classification', 'Origin', 'Character',
            'Company', 'Artists', 'Version', 'Material','Scale',
            'Dimensions', 'Release date', 'Various']
# ----
def cleanText(text):
    # clean fields of text contained in wordsToDelete
    wordsToDelete = ['Search (+)','(Details)']
    for i in wordsToDelete:
        text = text.replace(i,'')
    return text

def figureDataExt(pageText):
    # Extract data card in a dictionary, each field name is a key
    pageSoup = BeautifulSoup(pageText,"html.parser")
    table = pageSoup.find( class_="db-details overlay")
    data = {}
    try:
        rows = table.select('ul > li')
        try:
            # rowCells = [ c.find('label') for c in rows]
            rowCells = [ c.contents for c in rows]
            for cell in rowCells:
                if cell:
                    field = cell[0].text
                    data[field] = cleanText(cell[1].text)
        except:
            "There are no columns"
    except:
        print "There is no main db table"
    return data

def getPageTxt(index):
    # Get text from a url, via requests
    url = pageRoot+index
    with requests.Session() as s:
        try:
            searchPage = s.get(url,headers=headers,timeout=5)
            searchPage.raise_for_status()
            requestedTxt = searchPage.text
        except requests.exceptions.RequestException as e:
            print e
            requestedTxt = ''
            sleep(20)
    return requestedTxt

def rowFromFigure(index,cat='prepainted'):
    # integrate methods to get a line of data from a figure url
    figureTxt =  getPageTxt(index)
    figureData = figureDataExt(figureTxt)
    if not figureData:
        errorLog(index,cat)
        return None
    orderedDatarow = orderFields(figureData)
    return orderedDatarow

def getFigureIds(cat='prepainted'):
    # create a list of links from the selected file ids
    prepaintedPath = os.path.join(indexPath, cat+'.t')
    with open(prepaintedPath) as f:
        # content = f.readline()[:-1]
        content = [x.strip('\n') for x in f.readlines()]
    return content
# --------------------------------------------------------------------------
# Handling  connection errors
# TODO separate error logs for different categories
def errorLog(index,cat='prepainted'):
    # Save indexes that couldnt be accessed
    with open(cat+'_'+error_file, 'wa') as logfile:
        logfile.write((index+'\n').encode('utf-8'))

def getMissingIndexes(cat='prepainted'):
    # return list of indexes from error_log file
    if os.path.isfile(cat+'_'+error_file):
        with open(cat+'_'+error_file,'r') as f:
            content = [x.strip('\n') for x in f.readlines()]
        return content
    else:
        return []

def checkDone(fileName,indexList):
    # getMissingIndexes ALTERNATIVE without reading errorLog
    # Compare extracted data csv with the index list to see which index is missing
    # return index list
    notSaved = []
    csvIds = []
    with open(fileName, 'rb') as csvfile:
        dataReader = csv.reader(csvfile, encoding='utf-8')
        for row in dataReader:
            csvIds.append(row[0][1:])
    equal = len(csvIds[1:])==len(indexList)
    return equal,list(set(indexList) - set(csvIds[1:]))

def addMissingIndexes(fileName,category='prepainted',indexes=[]):
    # Final extraction of entries that had error
    # getting indexes from error log
    if not indexes:
        indexes = getMissingIndexes(category)
    # then resetting the error log
    if os.path.isfile(category+'_'+error_file):
        with open(category+'error_log.txt', 'w') as logfile:
            pass
    # extracting missing data
    extractData(fileName,indexes,category)
    # ordering data
    csvRows = []
    idRows = []
    with open(fileName, 'rb') as csvfile:
        dataReader = csv.reader(csvfile, encoding='utf-8')
        for row in dataReader:
            # eliminate duplicates
            if (row[0][1:] not in idRows) and (row[0][1:]):
                csvRows.append(row)
                idRows.append(row[0][1:])
    newRows = sorted(csvRows[1:], key=lambda x:int(x[0][1:]))
    createBlankCsv(fileName)
    toCsv(fileName,newRows)


# --------------------------------------------------------------------------
def orderFields(rowDict):
    # convert dictionary to rows for a csv file, non existing
    # attributes will appear as blanks
    rowList = [rowDict.get('ID', ' '),
               rowDict.get('Category', ' '),
               rowDict.get('Classification', ' '),
               rowDict.get('Origin', ' '),
               rowDict.get('Character', ' '),
               rowDict.get('Company', ' '),
               rowDict.get('Artists', ' '),
               rowDict.get('Version', ' '),
               rowDict.get('Material', ' '),
               rowDict.get('Scale', ' '),
               rowDict.get('Dimensions', ' '),
               rowDict.get('Release date', ' '),
               rowDict.get('Various', ' ')]
    return rowList

def createBlankCsv(fileName,header=csvHeader):
    # create blank csv with only top title row
    with open(fileName, 'wb') as csvfile:
        dataWriter = csv.writer(csvfile,dialect='excel', encoding='utf-8')
        dataWriter.writerow(header)

def toCsv(name,rows):
    # write rows to csv
    with open(name, 'ab+') as csvfile:
        dataWriter = csv.writer(csvfile, encoding='utf-8')
        for row in rows:
            dataWriter.writerow(row)

def csvLen(fname):
    # return number of valid lines
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i
# -------------------------------------------------------------------

def extractData(fileName,indexes,cat='prepainted'):
    # integrating all to extract data from lines init to init+group of the
    infoRows = []
    for index in indexes:
        row = rowFromFigure(index,cat)
        # if there is information, add it to the rows to save
        if row:
            infoRows.append(row)
        sleep(random.random()*random.random()) # Time in seconds.
    # return infoRows
    if infoRows:
        toCsv(fileName,infoRows)

def batchExtract(fileName,batchSize=10,cat='prepainted',restart=False):
    # Divide a bit number of extractions in groups of 5 for saving
    # If necessary, restart with a blank fileName
    # Shows progress for every 5 items
    group = 5
    cycles = batchSize/group
    oddOut = batchSize%group
    indexList = getFigureIds(cat)
    indexSize = str(len(indexList))
    if restart or not os.path.isfile(fileName):
        createBlankCsv(fileName)
        init = 0
    else:
        csvIds = []
        with open(fileName, 'rb') as csvfile:
            dataReader = csv.reader(csvfile, encoding='utf-8')
            for row in dataReader:
                # append number, removing the '#'
                csvIds.append(row[0][1:])
        # init = indexList.index(csvIds[-1])+1
        init = len(csvIds)-1
    # indexes file
    cutIndexList = indexList[init:]
    fileSize = csvLen(fileName)
    if not cutIndexList:
        print 'Finished'
    else:
        # get only needed indexes
        show = 0
        print str(show) + " rows already saved"
        print 'Starting with index',
        print cutIndexList[0]

        for i in range(cycles):
            start = i*group
            end = min((i+1)*group,len(cutIndexList))
            infoRows = extractData(fileName,cutIndexList[start:end],cat)
            show += end-start
            print str(show)+' of '+str(min(len(cutIndexList),batchSize))
            if len(cutIndexList)<(i+1)*group:
                print 'Finished'
                break
        print 'Total: '+str(fileSize-1+show)+' of '+indexSize

        # if the division is not exact
        if oddOut and len(cutIndexList)>batchSize:
            completed = (cycles*group)
            infoRows = extractData(cutIndexList[completed:completed+oddOut],cat)
            print show+oddOut,
            print 'items read'
    addMissingIndexes(fileName,category=cat)

# ------------------------------------------------------------
prepFileName = 'prepaintedData.csv'
actionFileName = 'actionData.csv'

# batchExtract(prepFileName,5000,'prepainted')
# print checkDone(prepFileName,getFigureIds('prepainted'))

# # --
# batchExtract(actionFileName,10000,'action')
# print checkDone(actionFileName,getFigureIds('action'))
# check = checkDone(actionFileName,getFigureIds('action'))
# TODO add checkDone routine to final error check
# addMissingIndexes(actionFileName,'action',check[1])
# TODO check current path to determine root anywhere
def main(argv):
   '''Script takes the following arguments:
   -h: help
   -s: size of the batch to be extracted
   -c: category to be extracted, argument is action or prepainted
   -R: restarts extraction'''

   batchSize=10
   category='prepainted'
   restart=False
   check = False
   try:
      opts, args = getopt.getopt(argv,"hs:c:Rd",["size=","category=","restart", "done"])
      print opts
   except getopt.GetoptError:
      print 'extractToCsv.py -s <batchSize> -c <category>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'usage: extractToCsv.py -s <batchSize> -c <category>'
         sys.exit()
      elif opt in ("-s", "--size"):
         batchSize = int(arg)
      elif opt in ("-c", "--category"):
         if arg in ('prepainted','action'):
            category = arg
         else:
            print 'usage: extractToCsv.py -s <batchSize> -c <category>'
            print "category should be 'prepainted' or 'action'"
            sys.exit()
      elif opt in ("-d", "--done"):
         check = True
      elif opt == '-R':
         restart = True

   if check:
      print 'checkDone(category)[0]'
   else:
      batchExtract(batchSize,category,restart)

if __name__ == "__main__":
   main(sys.argv[1:])


#
# if __name__ == '__main__':
#     srcPath = os.path.dirname(os.path.realpath(__file__))
#     print os.path.split(srcPath)
#
#
#
