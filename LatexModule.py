import subprocess
import os
import time

#packages is a list of packages, that might include options that they will be used with
def writeDocumentClass(tex_file, document_class, document_class_options=''):
    print('Entering writeDocumentClass')
    print('Will write to %s' % str(tex_file))
    with open(tex_file, 'w+') as tex:
        tex.write('\documentclass%s{%s} \n'% (document_class_options, document_class))
    print('Leaving writeDoumentClass')
    return


# writes all packages given as list in parameter pacakges to the tex_file. Structure of packages is a list of list. 
# Every list contains the name of the package as element 0, optional package parameters are given as element 1 to n
def writePreambleOfTex(tex_file, packages):
    with open(tex_file, 'a') as tex:
        for package in packages:
            package_name=package[0]
            #print(packageName) # use for debugging purposes
            tex.write(r'\usepackage')
            if package[1:]:
                tex.write('[')
                for option in package[1:]:
                    tex.write('%s, \n' % option)
                tex.write(']')
            tex.write('{%s} \n' % package_name)
    return

# this can be used to write any list of tex lines in the given tex file
def writeSetupOfPackages(tex_file, setup_lines):
    with open(tex_file, 'a') as tex:
        for setup in setup_lines:
            tex.write('%s \n' % setup)
    return

# this function writes the given buffer between \begin and \end{document}. Everything valid in LaTeX can be entered here
def writeBufferToTexFile(tex_file, buffer = ''):
    with open(tex_file, 'a') as tex:
        tex.write(r'\begin{document}')
        #tex.write('\n Damit dort auch was steht \n') # use for debugging purposes
        tex.write(buffer)
        tex.write(r'\end{document}')


#if the package array is given, the needed packages are append here
def makeTable(columnstring, lines_to_insert):
    string = ('\n \\begin{table}[hb] \n \\centering \n \\begin{tabular}{%s}'% columnstring)
    string += '\n'
    for line in lines_to_insert:
        for column in line:
            string += column
            string += '\t &'
        string = string[:-1] # removes last &
        string += '\\\\ \n'
    string += '\end{tabular} \n \\end{table} \n'
    return string


# this creates a proper tabularx table. requires to load package longtable and booktabs
def makeLongTable(columnstring, lines_to_insert):
    string = ('\n \\begin{tabularx}%s'% columnstring)
    print(columnstring, "columnstring")
    string += '\n'
    string += '\\toprule \n'
    for line in lines_to_insert:
        for column in line:
            string += column
            string += '\t &'
        string = string[:-1] # removes last &
        string += '\\\\ \n'
    string += '\\bottomrule \n'
    string += '\end{tabularx} \n'
    print(string)
    return string


# this function requires the background package. it writes the setup needed for the background picture package.
def setBackgroundPicture(tex_file, path_to_picture):
    config_string =[ '''\\backgroundsetup{ scale=1,color=black,opacity=0.1,angle=0,placement=bottom,
        contents={\\includegraphics[height=\\paperheight]{%s}}}''' % path_to_picture]
    writeSetupOfPackages(tex_file, config_string)


# this makes a link a hyperref link. Obviously needs hyperref package. returns new string
def createHREFlinkIfLink(link, alias_text):
    if str(link).startswith( 'http' ):
        return '\\href{' + str(link) + '}{' + alias_text + '}'
    else:
        return link


def compileXeLatex(tex_file_name, this_dir):
    ''' Compiling the given texfile in the given directory with xelatex (twice for labeling reasons etc.)

        Args:
            tex_file_name(string): Name of the tex file, should have ending .tex
            this_dir(path): String that describes the absolute path of the folder the tex-file is in

        Returns:
            None
    '''
    print('Entering xetex compile')
    working_dir = this_dir
    print('WorkingDir is ' + working_dir)
    logfile = open(this_dir + '/tex.log', "w+")
    print('Logs will be written to ', logfile.name)
    process = subprocess.Popen(['xelatex', tex_file_name, '-synctex=1 -interaction=nonstopmode'], cwd=working_dir, stdout=logfile)
    process.wait() # execute the same command again once the first tex run is finished
    subprocess.Popen(['xelatex', tex_file_name, '-synctex=1 -interaction=nonstopmode'], cwd=working_dir, stdout=logfile)
    logfile.close()


# currently not in use 

def cleaningUpAfterLatexCompilation(folderpath, filename):
    ''' Deletes all Files that were created in the process of creating the .pdf from tex file. Exentsions are
        .aux, .log, .out and .synctex.gz
        
        Args:
            folderpath (string): A String interpreted as path to the folder where the genereated files are.
            filename (string): The name of the file without extension. Should be the same as the one of the .pdf document.
        
        Returns:
            None.'''
    extension_list = ['.aux', '.log', '.out', '.synctex.gz']
    for extension in extension_list:
        temp_filename = os.path.join(folderpath, (filename+extension))
        if os.path.isfile(temp_filename):
            os.remove(temp_filename)


if __name__ == "__main__":
    writeDocumentClass('test.tex', 'scrartcl')
    writePreambleOfTex('test.tex', [['geometry']])
    table=[['hi', '3', '5']]

    writeBufferToTexFile('test.tex', makeTable('lrr', table))
    compileXeLatex('test.tex')
