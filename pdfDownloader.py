'''
Created on 16-Nov-2016

@author: kapil
'''
#! python3
import webbrowser, sys, pyperclip,requests,os,bs4,re

def downloadFile(filename,res):
    directry='/home/kapil/Downloads'
    file = open(os.path.join(directry, filename), 'wb')
    for chunk in res.iter_content(100000):
            file.write(chunk)

           
def checkValidLinks(linkElems):
    type='pdf'
    validlinks=[]
    if(type=='pdf'):
        for l in linkElems:
            trueLink=re.split(r'&',l.get('href'))
            filename, fileExt = os.path.splitext(trueLink[0])
            print(fileExt)
            #print(l.get('href'))
            if fileExt=='.pdf':
                validlinks.append(l.get('href'))
               
        
    if(type=='ppt'):
        for l in linkElems:
            filename, fileExt = os.path.splitext(l.get('href'))
            if fileExt=='.ppt'|'.pptx':
                validlinks.append(l.get('href'))
    return validlinks
    
        
def requestPage(urlAddress):
    try:
        res = requests.get(urlAddress)
    except Exception as exc:
        print('There was a problem in getting destination file: %s' % (exc)) 
        print('trying again...')
        return requestPage(urlAddress)
    return res  
            
if len(sys.argv) > 1:
# Get address from command line.
    address = ' '.join(sys.argv[1:])
else:
# Get address from clipboard.
    address = pyperclip.paste()
    #open the link in google
webbrowser.open('https://www.google.com/search?q=' + address)
#download the html page at the mentioned locatiin to read it
urlAddress='https://www.google.com/search?q=' + address
res=requestPage(urlAddress)
#genrate a filename to store the downloaded file file type pdf database management
filename=address.replace(' ', '.')
#filename+='.html'
downloadFile(filename, res)
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))
soup = bs4.BeautifulSoup(res.text,"html.parser")
linkElems = soup.select('.r a')
validlinks=checkValidLinks(linkElems)
print(linkElems)
print(validlinks)
if(validlinks!=None):
    numOpen = min(5, len(validlinks))
else:
    numOpen=0
for i in range(numOpen):
    webbrowser.open('http://google.com' + validlinks[i])
    
    
    #TODO
    #create folder on search term in downloads and save all foles in there
    
    
    
    