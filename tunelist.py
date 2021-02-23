#This script accepts a list of urls, applies tuning, & removes redundancies, and outputs the normalized list

import sys, getopt
import os.path
import configparser
import re

#check for duplicates, duplicates with a tailing / and blank entries
def readFromScreen():
    print("Enter/Paste URLS, to finish, from a new line press Ctrl+d on Linux on Crtl+z on less superior Operating Systems/Windows")
    urls = []
    try:
        while True:
            urls.append(input())#for python2 use raw_input())
    except EOFError:
        pass
    urls = "\n".join(urls)
    listUrls=urls.split("\n")
    return listUrls

#apply normalization based on mode to data
def normalizebymode(m,data, delim, nav):
    #how does python still not have proper case statements? kinda ridiculous
    if int(m)==2:
        for i in range(len(data)):
            #Find start of query
            res = None
            ini_string=data[i]
            for j in range(0, len(ini_string)): 
                if ini_string[j] == '?': 
                    res = j
                    break
            #strip it out
            if res != None: 
                #query parms exist, strip out values
                data[i] = re.sub(delim, "\g<1>*", data[i]) #match query param value and replace with *
        
    elif int(m)==3:
        for i in range(len(data)):
            #Find start of query
            res = None
            ini_string=data[i]
            for j in range(0, len(ini_string)): 
                if ini_string[j] == '?': 
                    res = j
                    break
            #strip it out
            if res != None:
                scrubquery="[\?&]+([^\=]+\=)([^&]+)"
                #query parms exist, strip out values                                
                temp = re.sub(scrubquery, "", data[i]) #strip out other params
                if re.findall(nav,data[i]):
                    match=re.search(nav,data[i])
                    data[i]=temp+"?"+match.group(1)+match.group(2)
                else:
                    data[i]=temp
         
    elif int(m)==4:
        a="leave the data alone for this one ;)"
                
    else:
        #its either a 1 or we assume its a 1        
        for i in range(len(data)):
            #Find start of query
            res = None
            ini_string=data[i]
            for j in range(0, len(ini_string)): 
                if ini_string[j] == '?': 
                    res = j
                    break
            #strip it out
            if res != None: 
                #d
                data[i]=ini_string[0:res]
                
    return data

def normalizerewrites(data, rwp):
    
    for i in range(len(data)): 
          
        if re.findall(rwp,data[i]):
            data[i] = re.sub(rwp, "\g<1>\g<2><VAL>", data[i])  
             
    
    return data

def basicCompare(string1,string2):
    if string1.lower()==string2.lower() or string1.lower()==string2.lower()+'/' or string1.lower()+'/'==string2.lower() or string1.lower()==string2.lower()+'\n' or string1.lower()+'\n'==string2.lower() or string1.lower()=='\n'+string2.lower() or '\n'+string1.lower()==string2.lower() or string1.lower()==string2.lower()+' ' or string1.lower()+' '==string2.lower() or len(string2)<2:
        return True
    else:
        return False
 
def main(argv):
    
    filein = ""#"urlsin.txt"
    interactive=0
    inScopeDomains={"demo.testfire.net"}
    
    mode=1 
    #Mode 1 url path only, 
    #Mode 2 URL path and query params without values, 
    #Mode 3 URL and query with selected navigational values only, 
    #Mode 4 all URL paths params and values
    
    #possible future modes to check methods and post body data
    
    config="tunelist.cfg"
    
    #defining arguments
    try:
        opts, args = getopt.getopt(argv,"hi:c:n",["filepath=","configfile=","interactive"])
    except getopt.GetoptError:
        print ('Error, please use the syntax: tunelist.py -i <filein (Default urlsin.txt)> -c <configfile (Default tunelist.cfg)> -n <interactive mode>')
        sys.exit(2)
      
    #reading arguments
    for opt, arg in opts:
        if opt == '-h':
            print ('tunelist.py -i <filein (Default urlsin.txt)> -c <configfile (Default tunelist.cfg)> -n <interactive mode>')
            sys.exit()
        elif opt in ("-i", "--filein"):
            filein = arg
        elif opt in ("-c", "--configfile"):
            config = arg
        elif opt in ("-n", "--interactive"):
            interactive=1        

    #apply any custom configuration from config file
    configparse=configparser.ConfigParser()
    if os.path.isfile(config):
        configparse=configparser.ConfigParser()
        configparse.read(config)
        filein = configparse['DEFAULT']['filein'] #ADD FILE IN CONDITION AND FILE PATH CHECK
        outputfile=configparse['DEFAULT']['outputfile']
        mode=configparse['DEFAULT']['mode']
        iterations=configparse['DEFAULT']['iterations']
        delimeter=configparse.get("PATTERNS", "delimeter")
        navPattern=configparse.get("PATTERNS", "navPattern")
        rewritePattern=configparse.get("PATTERNS", "rewritePattern")
        filetypefilter=configparse.get("PATTERNS", "filetypefilter")
        if interactive==0:
            interactive=int(configparse['DEFAULT']['interactive'])
        
    else:
        response=input("No config file found, create one with default properties (y/n)?")
        if response =='y' or response=='Y':
            #build new config file
            configparse['DEFAULT'] = {'filein': 'urlsin.txt','interactive': '0','outputfile': 'urlsout.txt','mode': '1','iterations': '20'}
            configparse['PATTERNS'] = {'delimeter':'(\=)([^&]+)','navPattern':'(?i)(page|redirect|content|target|EVENTTARGET|EVENTARGUMENT|goto|node|action|ctrl|source)(=[^&]+)','rewritePattern':'(?i)(blog|size|products)(\/)([^\/\?\.]+)','filetypefilter':'(?i)(\.jpg|\.png|\.gif)'}
            with open(config, 'w') as configfile:
                configparse.write(configfile)
            configparse.read(config)
            filein = configparse['DEFAULT']['filein']
            outputfile=configparse['DEFAULT']['outputfile']
            mode=configparse['DEFAULT']['mode']
            iterations=configparse['DEFAULT']['iterations']
            delimeter=configparse.get("PATTERNS", "delimeter")
            navPattern=configparse.get("PATTERNS", "navPattern")
            rewritePattern=configparse.get("PATTERNS", "rewritePattern")
            filetypefilter=configparse.get("PATTERNS", "filetypefilter")
            if interactive==0:
                interactive=configparse['DEFAULT']['interactive']
            
        else:
            print("Please manually create a config file with the name tunelist.cfg or run the script again and specify an alternate config file with the -c argument")
            return
        
        
    
    #get the list of input urls either by file or interactively
    if interactive==1:
        #Read from screen
        urlsraw=readFromScreen()
        
    else:
        #Read from file
        if os.path.isfile(filein):
            
            with open(filein) as f:
                urlsraw = f.read().splitlines()
        else:
            print("Input file does not exist or was not specified.  Please either specify file with -i or create ",filein) #change fro python2: print 'Input file does not exist or was not specified.  Please either specify file with -i or create',filein
            return
    
    #tune parameters by mode
    urlsraw=normalizebymode(mode,urlsraw, delimeter, navPattern)
    #tune out url rewrites
    urlsraw=normalizerewrites(urlsraw, rewritePattern)
    
    for l in range(0,int(iterations)): #account for any multipass updates
    
        #pass 1 remove straight duplicates
        c2=0 
        #current list length
        k=len(urlsraw)
        for i in range(len(urlsraw)):
            #current length check
            if i>=k:
                break
            else:
                s1=urlsraw[i]
                c2=i+1
                for j in range(i+1,len(urlsraw), 1):
                    #current length check
                    if j>=k:
                        break
                        
                    #Where the action happens
                    else:
                        s2=urlsraw[c2]
                        if basicCompare(s1, s2) or re.findall(filetypefilter,s2):
                            del urlsraw[c2]  #remove dup
                            j=j-1           #index shift to account for missing entry
                            k=k-1           #list length update
                        else:
                            c2=c2+1
    #check

    #print output to screen and file
    fileout=open(outputfile,'w')
    print("Normalized List:") 
    for x in urlsraw: 
        print(x) 
        fileout.write(x+'\n') 
    fileout.close()
    
    print("\nFile written to", outputfile) 
    
if __name__ == "__main__":
    main(sys.argv[1:])

 
