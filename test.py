
# -*- coding: utf-8 -*-

from LatexTemplate import *
Type = Template(Title = "Documentatino ", author="J \& J") #<----- Header title
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













#--------------Typeset below:-------------------->#
if __name__ == '__main__':
    try:
        Type.content(content)       # may be irrelevant
        Type.Typeset('test',showpdf=False) # <-filename
    except: 
        pass



