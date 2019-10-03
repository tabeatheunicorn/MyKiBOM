import LatexModule as Latex
import kicad_netlist_reader

import sys
import os
import glob

# The path to the picture is the optional third commandline parameter. If there is a file for the given path, it can be used as path which is returned form that function
def testForPicture():
    if os.path.isfile('C:/Bilder/AI_Stencil.png'):  # custom picture  
        path_to_AI_logo = 'C:/Bilder/AI_Stencil.png'
    if len(sys.argv) > 3:
        if sys.argv[3] != '': # empty string entered if picture should not be modified
            if os.path.isfile(sys.argv[3]):
                path_to_AI_logo = str(sys.argv[3]).replace('\\', '/')
            else:
                print("this isn't a picture")
    return path_to_AI_logo


# If a certain name is given as command line parameter, this one is set as filename. other than that, the default filename ist choosen
def testForCustomFilename():
    if len(sys.argv) > 4:
        filename = sys.argv[4]
        filename_wo_ext, extension = os.path.splitext(filename)
        if extension != '.tex':
            filename = filename_wo_ext + '.tex'
    else:
        filename = 'Version' + str(date_of_netlist).replace('.', '_').replace(' ', '_').replace(':','_')  + '.tex' # Custom Filename. Change here
    return filename


# Creates Doku Directory in the current folder where all bom related files will be placed. Returns True or False based on whether the dir exists after executing this function
def createDokuFolderIfNotExistent(directory):
    doku_directory = directory + '/doku'
    if not os.path.exists(doku_directory):
        os.mkdir(doku_directory)
    
    # test if successful
    if os.path.exists(doku_directory):
        return True
    else:
        return False

# This function tests if the file that should contain the tex file that is compiled later is writeable. It returns the absolute path to the file to compile later if that was possible
def testIfFileIsWriteable():
    try:
        name_of_document = testForCustomFilename()
        doku_directory, tail = os.path.split(sys.argv[2])  # second commandlineparamter selects the output directory plus name of board file without ending
        created_doku_directory = createDokuFolderIfNotExistent(doku_directory)
        if created_doku_directory == True:
            doku_directory += '/doku'
        test_tex_file = doku_directory + '/' + name_of_document # absolute path to tex_dokument to be created

        open_test_tex_file = open(test_tex_file, 'w+') # w+ creates the file if it is not existent
        open_test_tex_file.close()
        print('TeX File can be found at ', test_tex_file)
        return test_tex_file

    except IOError:
        e = "Can't open output file for writing: " + test_tex_file
        print( __file__, ":", e, sys.stderr )
        test_tex_file = sys.stdout
        return False

# Creates a list with all important information of the netlist given to it, also returns number of components
# Structure of the list elements is: getRef(), getValue(), getFootprint(), getDatasheet(), getField("Manufacturer"), getField("Vendor")
# @return list of components where each listentry consits of the defined component infos. First entrys are head of table
def getComponentsFromNetlist(netlist):
    print('Entering getComponentsFromNetlist')
    components = netlist.getInterestingComponents() # result is dependent on the configuration of the kicad_netlist_reader.py config part
    customFields = netlist.gatherComponentFieldUnion() # returns all fields that are used within the components
    fieldHeadings = ['Referenz', 'Wert', 'Footprint', 'Datenblatt']
    # for field in customFields: # this adds custom fields to the headings. Do not forget to change tableformatstring if uncommenting
    #     fieldHeadings.append(field)
    return_components =[fieldHeadings, ['\\midrule \\\\'], ['\\endhead'] ] # if this is initialised with a first list element, this can be used as a header later on
    print(return_components)
    total_amount_of_components = 0
    for comp in components:
        #print('All info about component', comp.getFieldNames())
        total_amount_of_components += 1
        # compCustomFields =[] # currently not in use
        # for field in customFields:
        #     appending = comp.getField(field)
        #     if appending == '' or appending == None:
        #         appending == " "
        #     compCustomFields.append(appending)
        fieldinfoslist = [comp.getRef(), comp.getValue(), comp.getFootprint(), comp.getDatasheet()] #+ compCustomFields 
        # if (len(fieldinfoslist) < len(return_components_headings)):
        #     print('zu kurz ', fieldinfoslist[0])
        return_components.append(fieldinfoslist)
    print(return_components)
    print('\n Leaving getComponentsFromNetlist')
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
        formatted_component = []
        #print('editing')
        #print(component)
        for info in component:
            info = str(info).replace('_', '\\_').replace('%', '\\%').replace('#','\\#')
            info = Latex.createHREFlinkIfLink(info, 'Link zum Datenblatt')
            formatted_component.append(info)
            #print(info)
        formatted_components_of_netlist.append(formatted_component)
    # print('Komponenten: ', formatted_components_of_netlist)
    # print('#############################')
    return formatted_components_of_netlist


# this function formats the components from the netlist to go into a LaTeX usable string. The components should be in the format they are in after using the function getComponentsFromNetlist()
def formatComponentsIntoTable(component_list):
    print('Entering formatComponentsIntoTable')
    table_format_string_longtable = '{0.9\linewidth}{llXX}' # llXX ist tableformatstring
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
# sys.argv[1] contains the xml file that is processed. 
project_folder, xml_name = os.path.split(sys.argv[1]) 

components_of_netlist, number_of_components = getComponentsFromNetlist(netlist)
formatted_components_of_netlist = formatNetlist(components_of_netlist)
name_of_BOM_list, date_of_netlist, tool_of_netlist = getNetlistInformation(netlist)

print(name_of_BOM_list, date_of_netlist)
name_of_document = testIfFileIsWriteable()
if name_of_document != False:
    tabellen_string = formatComponentsIntoTable(formatted_components_of_netlist)
    makeTeXFileFromFormatedBuffer(name_of_document, tabellen_string)
    print('Pdf is generated from ' + name_of_document)
    folder, file_name = os.path.split(name_of_document)
    #Latex.compileXeLatex(file_name, folder) 
    filename_without_extension, extension = os.path.splitext(file_name)
    print("searching for " + folder + '/' + filename_without_extension + '.pdf')
    if os.path.exists(folder + '/' + filename_without_extension + '.pdf'):
        print('Generated pdf successfully!')
    else:
        print('Please retry, pdf couldnot be found')
else:
    print('Could not write to file. No tex or pdf Output.')
