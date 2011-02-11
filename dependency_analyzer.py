#!/usr/bin/python
import os
import os.path
import sys

from lxml import etree

PROJECT_XML_FILE="project.xml"


def main():
    if len(sys.argv) == 1:
        print "Usage: python dependency_analyzer.py /root/of/netbeans/project"
        return -1
        
    project_root = sys.argv[1]
    
    projectXMLFiles = findProjectXMLFiles(project_root)
    
    module_dependencies = [analyzeProjectXMLFile(x) for x in projectXMLFiles]
    
    print "digraph {"
    
    for module in module_dependencies:
        for source, dependency in module:
            print '\t "%s" -> "%s";' %(source, dependency)
        pass
    pass
    print "}"



def findProjectXMLFiles(root):
    """ Given a root folder, walks the directory tree looking for all the
    'project.xml' files, and returns a list of all the matching file paths
    """
    projectFiles = []
    for dirpath, dirs, files in os.walk(root):
        if PROJECT_XML_FILE in files:
            theFile = os.path.join(dirpath, PROJECT_XML_FILE)
            projectFiles.append(theFile)
    
    return projectFiles
    
def analyzeProjectXMLFile(projectXMLFile):
    """ Given the path to a project.xml file, which declares all the
    dependencies of a give module, returns a list of tuples, where the first
    element is the current module's code base name, and the second element
    is the name of the dependency of the module.
    """
    # print "analyzing " + projectXMLFile
    namespaces = {
        "project":"http://www.netbeans.org/ns/project/1",
        "d":"http://www.netbeans.org/ns/nb-module-project/3"
    }
    # Load the XML
    tree = etree.parse(projectXMLFile)
    
    # Use XPath to isolate the code-base-name tag
    codenames = tree.xpath("//d:code-name-base", namespaces=namespaces)
    
    # We can't glean any information from this file; it should be the root
    # node's project.xml file.
    if len(codenames) == 0:
        return []
    
    codename = codenames[0].text
    
    # a list of text nodes
    dependencies = [x.text for x in tree.xpath("//d:dependency/d:code-name-base", namespaces=namespaces)]
    
    return [(codename, x) for x in dependencies]

if __name__ == '__main__':
    main()