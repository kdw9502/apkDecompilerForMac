import os
import sys

global abspath
abspath = os.getcwd()
global DEX2JAR_URL
DEX2JAR_URL = 'https://jaist.dl.sourceforge.net/project/dex2jar/dex2jar-2.0.zip'
'''
global AXMLPrinter_URL
AXMLPrinter_URL = 'https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/android4me/AXMLPrinter2.jar'
'''
global APKTOOL_URL
APKTOOL_URL ='-L https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.3.1.jar'
global DOWNLOAD_COMMAND
DOWNLOAD_COMMAND = 'curl --retry 5 --retry-delay 5 -o '
global DEX2JAR_ZIP
DEX2JAR_ZIP = 'dex2jar-2.0.zip'
global APKTOOL_JAR
APKTOOL_JAR ='apktool_2.3.1.jar'
global DEPENDENCY_FOLDER
DEPENDENCY_FOLDER = 'Dependencies'
global LOGFILE
LOGFILE = 'apkDecompileLog.txt'
global LOAD_SUCCESS
LOAD_SUCCESS = 'success'


def DownloadDependency():

    if os.path.isdir(DEPENDENCY_FOLDER):
        if os.path.exists(DEPENDENCY_FOLDER + '/' + LOAD_SUCCESS):
            return
        else:
            CommandLine("rm -rf " + DEPENDENCY_FOLDER)
    print("Downloading Dependencies")

    loadSuccess = True
    loadSuccess = loadSuccess and CommandLine("mkdir " + DEPENDENCY_FOLDER)
    os.chdir(DEPENDENCY_FOLDER)
    loadSuccess = loadSuccess and CommandLine(DOWNLOAD_COMMAND + DEX2JAR_ZIP + " " + DEX2JAR_URL)
    print(DEX2JAR_ZIP+" downloaded")
    loadSuccess = loadSuccess and CommandLine(DOWNLOAD_COMMAND + APKTOOL_JAR + " " + APKTOOL_URL)
    print(APKTOOL_JAR+" downloaded")
    loadSuccess = loadSuccess and CommandLine("unzip -o " + DEX2JAR_ZIP)
    loadSuccess = loadSuccess and CommandLine("rm " + DEX2JAR_ZIP)
    loadSuccess = loadSuccess and CommandLine("chmod 744 " + DEX2JAR_ZIP.split('.zip')[0] + "/d2j_invoke.sh")
    if loadSuccess:
        fp_w = open(LOAD_SUCCESS,'w')
    print("Dependencies Download Success: " + str(loadSuccess))
    os.chdir("../")


def CommandLine(command):
    exitcode = os.system(command + ' >> ' + LOGFILE)
    if exitcode != 0:
        print('command line:' + command)
        print('fail, exit code:' + str(exitcode))
        return False
    return True

def DecompileApk(apkPath):
    if not os.path.exists(apkPath):
        print("apk doesn't exists")
        return
    if not apkPath.endswith('.apk'):
        print("this file is not apk")
        return
    ExtractFolderName = apkPath.split('/')[-1].split('.apk')[0]
    CommandLine("unzip -o -d " + ExtractFolderName + ' ' + apkPath)
    #inFolderXmlConvert(ExtractFolderName)
    print("Dex to Jar converting start")
    Dex2jar(ExtractFolderName)
    print("Dex to Jar converting done")
    print("xml decoding start")
    XmlReplace(ExtractFolderName, apkPath)
    print("xml decode done")

def Dex2jar(apkFolderName):
    CommandLine("sh " + DEPENDENCY_FOLDER + '/' + DEX2JAR_ZIP.split('.zip')[0] + '/d2j-dex2jar.sh -f -o '
                + apkFolderName + '/classes.jar ' + apkFolderName + '/classes.dex')


def UnpackAPK(apkPath):
    CommandLine("java -jar " + DEPENDENCY_FOLDER + "/" + APKTOOL_JAR + " -s -f d " + apkPath + " -o temp")


def XmlReplace(ExtractFolderName, apkPath):
    UnpackAPK(apkPath)
    for path,dir,files in os.walk(ExtractFolderName):
        for file in files:
            if file.endswith('.xml'):
                fullpath = path + '/' + file
                CommandLine('mv -f ' + fullpath.replace(ExtractFolderName, 'temp', 1) + " " + fullpath)
    CommandLine("rm -rf temp")
'''
def inFolderXmlConvert(FolderName):
    for path,dir,files in os.walk(FolderName):
        for file in files:
            if file.endswith('xml'):
                fullpath=path + '/' + file
                if os.path.exists('temp.xml'):
                    commandLine('rm temp.xml')
                commandLine('cp '+fullpath+' temp.xml')
                commandLine('rm '+fullpath)
                os.system('java -d64 -jar '+DEPENDENCY_FOLDER+'/AXMLPrinter2.jar '+'temp.xml'+' > '+fullpath )
'''
def main():
    if os.path.exists(LOGFILE) :
        ("rm " + LOGFILE)
    DownloadDependency()
    apkPath = input("Enter the file name(path) of apk : ")
    DecompileApk(apkPath)
    CommandLine("aapt list  -a %s | grep SdkVersion"%apkPath)

if __name__ == "__main__" :
    main()