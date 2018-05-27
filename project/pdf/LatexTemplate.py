# -*- coding: utf-8 -*-
"""
CHANGELOG:
Update 06.05.17:
Added to scripts and export via bashrc
note: 1. Added #! first line path (find with "which python")
      2. chmod 744 Latextemplate-file makes run anywhere
      3. added:
      "export PATH=$PATH:/home/jacobalexander/Dropbox/Py_Resources/scripts"
      to ~/.bashrc (path to script)
      4. run > source ~/.bashrc

Update 11.04.17:
cleanup and precision in generated py-file 
comment included on variables for the generation 
(author, date, landscape) 

Also some general cleanup.

Update 04.04.17:
TODO:
-Make hidden the aux,log,out,txt files. 



Update 18.02.17: 
- Make "yes" default prompt.


Update: 31.01.17: 

Location of resource established based on os. 
Hashed out "new" function, consider for later readdition.

Update 29.01.17: 
Moved to dropbox, added location.
updated 18.11.16: 
FIXES: 
changed the postscript for py files generated to not run 
"new" function yet. (added elif statement to skip if 
no identified sysargv1)

also aesthetic brush up, no major changes otherwise.

updated: 05.09.16
Note: Landscape, filled, pay attention to multicol
geometry change fixed, ish. 
added Table-adder

Moved Table-function in here. 05.09.16, so import Table, and use as 
prescribed. 

FIXES:  
Make Landscape not default, but easy to control from 
init function 

TODO: 
- Write compiler (as content or as bringing in from different .txt files.
need to check and import every type, try-except loops. 
- More templates, and options for easy change between landscape etc. 
"""

#Default template for use. cut/paste commented field 
# and use raw_strings in content element ( content += r"")
import sys
import os
import datetime
class Template:
    """
    Usage 
    Create new Template file: 
    > python LatexTemplate.py <Title> 
    
    Editing: 
    open <Title>.py in word-processer. 
    write text and LaTeX-format in "content"-raw string object
    example: 
        content = r""
    or 
        content += r"" 
    Typesetting:
    > python <Title>.py 
    """
    def __init__(self, Title='', 
                author=None, 
                date=None, 
                landscape=False):
        """
        Define author in the bottom of write-file, <Title>.py 
        if no author is given, default is set in program 
        if no date is given, will use today's date.
        """
        if author == None: 
            self.author = "use author=string"  #default Author set
        else:    
            self.author = author
        if date == None:                    #default date = today 
            s = str(datetime.datetime.now())
            S = s.split()[0]
            self.date = S
        else:
            self.date = date
        self.title = Title
        self.landscape = landscape

    def OldIntro(self):
        if self.landscape: 
            Intro = r" \documentclass[landscape]{article} %landscape mode included"
        else: 
            Intro = r"\documentclass{article} %landscape mode included"
        Intro += r"""
%Additions by joseph
\usepackage{subcaption}
\usepackage{parskip}
\usepackage{color}
\usepackage{listings}


\definecolor{red}{rgb}{1,0,0}
\definecolor{green}{rgb}{0,1,0}
\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}

\lstdefinestyle{mystyle}{
    backgroundcolor=\color{backcolour},   
    commentstyle=\color{blue},
    numberstyle=\tiny\color{codepurple},
    stringstyle=\color{codegreen},
    basicstyle=\footnotesize,
    breakatwhitespace=false,         
    breaklines=true,                 
    captionpos=b,                    
    keepspaces=true,                 
    numbers=left,                    
    numbersep=5pt,                  
    showspaces=false,                
    showstringspaces=false,
    showtabs=false,                  
    tabsize=2
}
 
\lstset{style=mystyle,language = Python}


\usepackage{geometry}
\geometry{left=20mm,right=20mm,top=20mm,bottom=30mm}
\usepackage{fancyvrb}   % for verbatim monospace computer code
\usepackage{graphicx}   % for \includegraphics command
\usepackage{pdfpages}
\usepackage{amssymb,amsmath}    % math stuff
\usepackage{mathtools}
\usepackage{verbatim}   % for importing verbatim. fancy is better google it
\usepackage[utf8]{inputenc} % utf-8 encoding.
\usepackage{physics} %for bra-ket notattino etc. 
\usepackage{multicol,caption}
\usepackage{lipsum}
\usepackage{epigraph}
\usepackage{enumitem}
\usepackage{tensor}
\usepackage{hyperref}
\setlength{\columnsep}{1cm}
\newenvironment{Figure}
  {\par\medskip\noindent\minipage{\linewidth}}
  {\endminipage\par\medskip}
\begin{document}"""
        

        Intro+=r"""
\title{%s}
\author{%s}
\date{%s}
\maketitle

""" % (str(self.title),str(self.author),str(self.date))
        self.intro = Intro

    def content(self, content):
        """
        Method extracts everything defined as content (raw-string element)
        """
        self.content = content

    #Clippings part 1 from here 


    def Typeset(self, filename, showpdf=True):
        """
        called when running; 
            >python <Title>.py
        Generates pdf-file using pdflatex 
        if: [showpdf=True] will try opening pdf in evince 
	TODO: Fix universal search for used reader, and apply under showpdf-function
        """
        self.TXTGen(filename)   
        try: 
            os.system('pdflatex %s.txt' % self.filename)
        except: 
            print "pdf generation failed, please use converter of choice to generate LaTeX-pdf with the content in  %s.txt" %self.filename
        if showpdf:
            if sys.platform == 'darwin':
                try:
                    os.system('open -a "Preview.app" %s.pdf' %self.filename) 
                except:
                    pass
            else:
                try:
                    os.system('open %s.pdf &' % self.filename)
                except:
                    print "failed to open pdf"

    def Cleanup(self):
        """
        Moves files to subdirectory before Typeset, pdflatex etc. 
        """
        
        #Check for subdir
        def checkdir():
            try:
                e_code = os.system('ls Temp_%s/'%self.filename)
                if e_code != 0: 
                    os.system('mkdir Temp_%s'%self.filename)
                else: 
                    pass
            except: 
                pass
        #Run above, then implement move of py-files. 
        #Subsequent, run pdf-latex, copy pdf back.
        pass



    def TXTGen(self, filename):
        """
        Writes to .txt file with LaTeX template which can be converted directly to LaTeX document, (will automatically generate pdf if pdflatex is installed)
        """
        self.OldIntro()
        content = self.intro
        content += self.content
        content += '\n\\end{document}\n'
        infile = open('%s'%filename +'.txt', 'w')
        infile.write(content)
        infile.close
        self.filename = filename

#Consider adding useful functions with %-out in bottom, 
# either as demo or for usefulness or rare use.
try: 
    Title = sys.argv[1]
except: 
    Title = 'Unknown'

Template1 = r"""
# -*- coding: utf-8 -*-

from LatexTemplate import *
Type = Template(Title = "Title") #<----- Header title
#^additional vars: author(str), date(str), landscape(boolean) 
#---create content as raw string below--# 
#----------using LaTeX-format-----------#  
content = r'' #creating initial content, 
#------------content below--------------# 
content += r''' 


'''  


#------useful functions & such----------#
# Allowing for Python Code
# %s format for standard string inclusion. 
# May also call on other programs for generating data 
# that goes into string. 

# See for table generation: 
# Use Table(Input, Input titles) function for Table 
#                          or Table.T for transpose
#Latex: 
'''

#%\end{Verbatim}
#%\VerbatimInput{program}

\mathcal{} #%Calligraphic
\mathbb{}  #Hollow Spaces
\mathbf{}  #Boldface

\begin{equiation}\tag*{S} #change showing tag *no parenthesis
\labe
\begin{Figure}
 \centering
 \includegraphics[width=\linewidth]{count_deg_fig.png}
 \captionof{figure}{målingsdata}
\end{Figure}

\begin{multicols*}{2} %remember to \end.
\begin{description} %or item, enumerate
\epigraph{quote}{author} %for cool quotes

\includepdf{file.pdf} %or png works too. 

% For "skipping" the rest of column, or page 
\vfill\null
\columnbreak

\begin{align} 
%usage: & for line \\ for breaks


'''












"""
Template1 += """
#--------------Typeset below:-------------------->#
if __name__ == '__main__':
    try:
        Type.content(content)       # may be irrelevant
        Type.Typeset('%s',showpdf=False) # <-filename
    except: 
        pass



""" % (Title) #, Title)

import numpy as np
def Table(Input, variable_titles):
    """
    Usage; input array with values, and 
    list with titles/headers for values. 
    If needed twist, just add with .T at end (transpose.)
    Remember to check values
    """
    width, height = np.shape(Input)
    table = r'''\begin{center}
  \begin{tabular}{%s}''' % ('| c ' * width + '|')
    table += r'''
    \hline
    %s '''% variable_titles[0]
    for i in range(width-1):
        table += r' & %s ' % (variable_titles[i+1]) 
    table += r'''\\ \hline 
    '''    
    for i in range(height):
        table += r'%s ' % Input[0][i]
        for j in range(width-1):
            table += r' & %s ' % (Input[j+1][i]) 
        table += r'''\\ \hline 
        '''   
    table += r'''
  \end{tabular}
 \end{center}'''
    return table 


#IFNAME run-portion.
if __name__ == '__main__':
    title=Title      #Defined earlier, sysargv1
    try:
        yesno = raw_input('Create/Overwrite %s.py ? [y]/n' %title)
        if yesno == 'y' or yesno == 'Y':
            infile = open('%s'%title + '.py', 'w')
            infile.write(Template1)
            infile.close()
        elif yesno == '': 
            infile = open('%s'%title + '.py', 'w')
            infile.write(Template1)
            infile.close()
        else: 
            pass
    except:
        print "no title, (sys.argv[1]), detected. Enter Title:"
        prompt = raw_input()
        if prompt == '': 
            print 'no title selected, please try again'
            sys.exit(1)
        else:
            infile = open('%s'%prompt + '.py', 'w')
            infile.write(Template1)
            infile.close()



'''
#Clips, Removals, temp-storage of additional mods:
    #Clippings part 1 start: 
    def Abstract(self, abstract):
        """
        self explanatory, same as other categories:
        - Abstract.
        - Introduction.
        - Theory. 
        - Experiment. 
        - Result. 
        - Discuss + Conclusions. 
        - Summary. 
        - Citations 
        """
        self.abstract = abstract

    def Introduction(self, intro):
        self.intro = intro
    def Theory(self, string):
        self.theory = string
    def Experiment(self, string):
        self.experiment = string
    def Result(self, string):
        self.result = string
    def Discussion(self, string):
        self.discussion = string
    def Summary(self, string):
        self.summary = string
    def Citations(self, string):
        self.citations = string

    def NewType(self, filename=None, template = None):
        """
        TODO: make different templates. 
        save as tmp.txt and pdflatex the kerfuffle out of it. 
        """
        for filename in ['abstract', 'intro', 'theory','experiment','result','discussion','summary','citations']:
            try:
                stuff = r''
                infile = open('%s'%filename +'.txt', 'r')
                for line in infile:
                    stuff += r'%s'%line
                infile.close
            except:
                pass


    def Store(self):
        """
        Stores in order to .txt files: 
        - Abstract.
        - Introduction.
        - Theory. 
        - Experiment. 
        - Result. 
        - Discuss + Conclusions. 
        - Summary. 
        - Citations 
        """
        for filename in ['abstract', 'intro', 'theory','experiment','result','discussion','summary','citations']:
            try:
                infile = open('%s'%filename +'.txt', 'w')
                infile.write(eval('self.'+'%s'%filename))
                infile.close
            except:
                pass
        #self.filename = filename
    #Clippings part 1 stop


#Clipped from pre- ifname
###---For modification inculding "new" function----###
"""
    if sys.argv[1] == 'new':
        try:
            Type.Abstract(abstract)
            Type.Intro(intro)
            Type.Theory(theory)
            Type.Experiment(experiment)
            Type.Result(result)
            Type.Discussion(discussion)
            Type.Summary(summary)
            Type.Citations(citations)
            Type.Store()    
            Type.NewType('%s',showpdf=True) # ---- ,, ----
    #creates .txt-file with given filename (sub-function)
    #runs following command using os.system-call
    #> pdflatex filename.txt  
        except: 
            print "error in 'new'-function"
    elif sys.argv[1] == None:
        pass
    else: 
        pass
""" 
'''
