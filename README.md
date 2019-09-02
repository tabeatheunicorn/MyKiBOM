# MyKiBOM
Customizable KiCad Bill of Materials (BOM) with LaTeX and Python

# About the project
This project provides python scripts to create a pdf that is a Bill of Materials (BOM) in KiCad. It also comes with a install script ( **execute as admin only**)
that installs miktex and required packages if needed as well as copying the scriptfiles to the KiCad scripting folder (*this needs admin rights*).

## How to Use
When Opening EEScheme from KiCad, klick on the BOM-Button. This should generate an up-to-date netlist. Then choose the KiBOMWithTeX**.py-Plugin you want and create a KiBOM.
From Version 1.1 on the commandline arguments allow to customize the generated .pdf file.
