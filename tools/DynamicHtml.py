#! /usr/bin/env python
#---------------------------------------------------------------------------
# Copied from a command-line generator (I wrote),
# hence the structure:
# Pages are generated at import-time
#
# Cedric Adjih - Inria - Oct 2015
#---------------------------------------------------------------------------

#from shutil import *
import os, shutil
import argparse
J = os.path.join

#---------------------------------------------------------------------------

BaseDir = "www-template"
GeneratedDir = "www-generated"

TemplateFileName = "site.template-html"

FileList = [
    "andreas00.css",
    ("Home", "index.content.html", None),
    #("Odysse protocol", "odysse.content.html", None),
    #("Platform", "platform.content.html", None),
    #("Tilas", "overview.content.html", None),
    #("Publications", "publications.content.html", None),
    
    
    #("PhD/Post-Doc Positions", "phd-postdoc-position.content.html", None),
    (None, "logo-riot2-resized.png", "img/image-header.jpg"),
    #"img/D2D-figure.png"
]

#---------------------------------------------------------------------------

# <li><a class="current" href="index.html">Home</a></li>

#siteDir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
siteDir = os.path.dirname(os.path.realpath(__file__))
templateDir = J(siteDir, BaseDir)
templatePath = J(templateDir, TemplateFileName)
outDir = J(siteDir, GeneratedDir)
#outDir = "/auto"

# Template content
with open(templatePath) as f:
    templateContent = f.read()

# Clear output dir
#if os.path.exists(outDir):
#    shutil.rmtree(outDir)
if not os.path.exists(outDir):
    os.mkdir(outDir)

# Identify all files to be copied/generated
generatedFileList = []
for fileSpec in FileList:
    if type(fileSpec) == tuple:
        menuName, fileName,dstFileName = fileSpec
    else: menuName, fileName, dstFileName = None, fileSpec, fileSpec
    
    if dstFileName == None:
        dstFileName = fileName

    path = J(templateDir, fileName) 
    if not os.path.exists(path):
        path = J(siteDir, fileName)
    if not os.path.exists(path):
        raise RuntimeError("Cannot find file", fileName)

    #print path, dstFileName
    dstPath = J(outDir, dstFileName)
    dstParentPath = os.path.dirname(dstPath)
    if not os.path.exists(dstParentPath):
        os.mkdir(dstParentPath)

    generatedFileList.append((menuName, path, dstFileName))

        
# Create menu
def getDstPath(outDir, dstFileName, fullPath=True):
    if fullPath:
        dstPath = J(outDir, dstFileName)
    else: dstPath = dstFileName
    dstPath = dstPath.replace(".content.html", ".html")
    return dstPath

menuList = []
for (menuName, srcPath, dstFileName) in generatedFileList:
    if menuName != None:
        assert srcPath.endswith(".content.html")
        dstPath = getDstPath(outDir, dstFileName, fullPath=False)
        menuList.append((menuName, dstPath))

# Copy/generate files
def generateMenu(menuList, currentMenuName):
    menuStr = ""
    for menuName, dstPath in menuList:
        if menuName == currentMenuName:
            menuStr += '<li><a class="current" href="%s">%s</a></li>\n' % (
                dstPath, menuName)
        else: menuStr += '<li><a href="%s">%s</a></li>\n' % (dstPath, menuName)
    return menuStr

def generatePage(templateContent, menuList, menuName, content):
        # Generate from template
        pos1 = content.find("<h1>")
        pos2 = content.find("</h1>")
        if pos1 < 0 or pos2 < 0:
            raise ValueError("No title (<h1>...</h1>) in page", menuName)
        title = content[pos1+len("<h1>"):pos2]
        #print title
        #return generatedContent
        generatedContent = templateContent.replace(
            "<TEMPLATE-TITLE>", title
        ).replace(
            "<TEMPLATE-MENU>", generateMenu(menuList, menuName)
        ).replace(
            "<TEMPLATE-CONTENT>", content
        )
        return generatedContent

DynamicPageTable = {
}

for (menuName, srcPath, dstFileName) in generatedFileList:
    dstPath = getDstPath(outDir, dstFileName)
    if srcPath.endswith(".content.html"):
        with open(srcPath) as f:
            content = f.read()
        generatedContent = generatePage(templateContent, menuList, menuName,
                                        content)
        with open(dstPath, "w") as f:
            f.write(generatedContent)
        print "+", dstPath
    else: 
        # Copy file
        shutil.copy(srcPath, dstPath)
        print srcPath, dstPath

#---------------------------------------------------------------------------
