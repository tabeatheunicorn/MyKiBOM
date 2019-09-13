import LatexModule as Latex
import kicad_netlist_reader

import sys
import os
import glob

# The path to the picture is the optional third commandline parameter. If there is a file for the given path, it can be used as path which is returned form that function
def testForPicture():
    if len(sys.argv) > 3:
        if os.path.isfile(sys.argv[3]):
            path_to_AI_logo = sys.argv[3]
        else:
            print("this isn't a picture")
    elif os.path.isfile('C:/Bilder/AI_Stencil.png'):   
        path_to_AI_logo = 'C:/Bilder/AI_Stencil.png'
    return path_to_AI_logo


# If a certain name is given as command line parameter, this one is set as filename. other than that, the default filename ist choosen
def testForCustomFilename():
    if len(sys.argv) > 4:
        filename = sys.argv[4]
    else:
        filename = 'Version' + str(date_of_netlist).replace('.', '_').replace(' ', '_').replace(':','_')  + '.tex'
    return filename


# This function tests if the file that should contain the tex file that is compiled later is writeable. It returns the absolute path to the file to compile later if that was possible
def testIfFileIsWriteable():
    try:
        name_of_document = testForCustomFilename()
        print(name_of_document)
        doku_directory = sys.argv[2]  # second commandlineparamter selects the output directoryy
        print('Will write here: ', doku_directory)
        test_tex_file = doku_directory + '/' + name_of_document
        print('I want to write to:')
        print(test_tex_file)
        open_test_tex_file = open(test_tex_file, 'w')
        open_test_tex_file.close()
        return test_tex_file
    except IOError:
        e = "Can't open output file for writing: " + test_tex_file
        print( __file__, ":", e, sys.stderr )
        test_tex_file = sys.stdout
        return False

# Creates a list with all important information of the netlist given to it, also returns number of components
# Structure of the list elements is: getRef(), getValue(), getFootprint(), getDatasheet(), getField("Manufacturer"), getField("Vendor")
def getComponentsFromNetlist(netlist):
    print('Entering getComponentsFromNetlist')
    components = netlist.getInterestingComponents()
    return_components = [['Referenz', 'Wert', 'Footprint', 'Datenblatt', 'Manufacturer', 'Vendor'], ['\\midrule \\\\'], ['\\endhead'] ] # if this is initialised with a first list element, this can be used as a header later on
    total_amount_of_components = 0
    for comp in components:
        total_amount_of_components += 1
        return_components.append([comp.getRef(), 
            comp.getValue(), 
            comp.getFootprint(),
            comp.getDatasheet(),
            comp.getField("Manufacturer"),
            comp.getField("Vendor")])
    print('Leaving getComponentsFromNetlist')
    return return_components, total_amount_of_components


# this function returns document relevant data like author, date etc.
def getNetlistInformation(netlist):
    print('Entering getNetlistInformation')
    source  = netlist.getSource()
    date    = netlist.getDate()
    tool    = netlist.getTool()
    print('Leaving getNetlistInformation')
    return source, date, tool


# fromats away all crazy characters that latex can't deal with
def formatNetlist(components_of_netlist):
    formatted_components_of_netlist = []
    for component in components_of_netlist:
        formatted_componten = []
        #print('editing')
        #print(component)
        for info in component:
            info = str(info).replace('_', ' ')
            info = Latex.createHREFlinkIfLink(info, 'link')
            formatted_componten.append(info)
            #print(info)
        formatted_components_of_netlist.append(formatted_componten)
    return formatted_components_of_netlist


# this function formats the components from the netlist to go into a LaTeX usable string. The components should be in the format they are in after using the function getComponentsFromNetlist()
def formatComponentsIntoTable(component_list):
    print('Entering formatComponentsIntoTable')
    # this was used for a normal table
    # table_format_string     = 'llllll' # currently, there are 6 columns in every list element
    # complete_table_string   = Latex.makeTable(table_format_string, component_list)
    table_format_string_longtable = '{0.9\linewidth}{llXXll}'
    complete_table_string        = Latex.makeLongTable(table_format_string_longtable, component_list)
    print('Leaving formatComponentsIntoTable')
    return complete_table_string



# Takes as many arguments as wanted. Every argument is turned into a string with an EOL usable in TeX. They are written in the order they are passed to the function 
def makeTeXFileFromFormatedBuffer(tex_file, *args):
    print('Entering makeTexFileFromFormatedBuffer')
    Latex.writeDocumentClass(tex_file, 'scrartcl' , '[landscape]' ) # scrartcl is mostly a good choice. do not modify if not sure what you are doing!
    packages = [['booktabs'],
         ['ltablex'], 
         ['background', 'pages=all'], 
         ['graphicx'], 
         ['geometry', 'scale=0.9', 'landscape'], 
         ['hyperref']]
    Latex.writePreambleOfTex(tex_file, packages)
    logo = testForPicture()
    if logo:
        Latex.setBackgroundPicture(tex_file, logo)
    latex_string = ''
    for arg in args:
        latex_string += str(arg)
        latex_string += '\n'
    Latex.writeBufferToTexFile(tex_file, latex_string)
    print('Leaving makeTexFileFromFormatedBuffer')


# Runs XeTeX on given texfile, pdf result will be in output_file
def generatePDFFromTEXFile(tex_file):
    print('Entering generatePDFFromTEXFile')
    print('Outputfile is %s' % sys.argv[2] + '/../')
    Latex.compileXeLatex(tex_file, sys.argv[2] + '/../')
    print('Leaving generatePDFFromTEXFile')




####################################################################
# The plugin itself
######################################################################
#  Making sure that I can write to a file
# Open a file to write to, if the file cannot be opened output to stdout
# instead
print(sys.version)


# Reading in netlist with kicad netlist reader to gain all information needed 
# Here the formatting etc. is done
netlist = kicad_netlist_reader.netlist(sys.argv[1])
components_of_netlist, number_of_components = getComponentsFromNetlist(netlist)
formatted_components_of_netlist = formatNetlist(components_of_netlist)
name_of_BOM_list, date_of_netlist, tool_of_netlist = getNetlistInformation(netlist)


name_of_document = testIfFileIsWriteable()
if name_of_document != False:
    tabellen_string = formatComponentsIntoTable(formatted_components_of_netlist)
    makeTeXFileFromFormatedBuffer(test_tex_file, tabellen_string)
    print(name_of_document)
    generatePDFFromTEXFile(name_of_document)
else:
    print('Could not write to file.')
