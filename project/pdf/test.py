
# -*- coding: utf-8 -*-

from LatexTemplate import *
Type = Template(Title = "UNIK 4690 Computer Vision Project\\\ The Magic Greenscreen", author="Joseph Knutson \& Jacob Alexander Hay") #<----- Header title
#^additional vars: author(str), date(str), landscape(boolean) 
#---create content as raw string below--# 
#----------using LaTeX-format-----------#  
content = r'' #creating initial content, 
#------------content below--------------# 
content += r''' 

%\section*{Mulige kilder til segmentering:} 
%\url{https://www.cs.cmu.edu/~hebert/boundaries.htm}
\abstract{}
\section*{Introduction}
Green Screens, are used in movies, series, news, video-games and home-made videos with the main reason of providing an artificial background. The technique requires an
approximately monochrome and plain background (often green) to be placed behind whatever is wanted in the foreground (often a person). When the green screen is placed, 
a technique called Chroma Keying is applied in order to map where the plain green surface is. When the location of the green pixels are knows, a CGI, Computer Generated 
Image, is mapped onto these pixels, making it seem like the person is standing in front of whatever is put in the back.

Our algorithm provides a Green Screen tool, without having to place a Green Screen inside the scene.
Our course has thought us complex, color based segmentation methods, but as people's backgrounds vary, colour based segmentation is not an option.


'''  

"""
Skissert fremgang: 
1. Idé; 
    Bruk OpenPose-biblioteker til å finne grunnpunkter i et 
    menneske slik at man kan generere et konvekst hull omkring 
    mennesket (omhyllings-flate.)
    
2. Ved å bruke Pose til å estimere hvor leddene på et menneske 
    er kan man danne en tilnærmet omhylling ved å bruke geometriske 
    former, slik som pyramider, kuler, kuber, osv. 
    (ikke ulikt en lego-figur, eller en skulptur.)
    
3. Til sist antar man at disse figurene og formene danner et sett, hvor 
    hele mennesket er inneholdt innenfor grensene til figurene. 
    (Matematisk sett er da mennesket en del av det konvekse settet med 
     punkter inneholdt i det samlede settet av 3D former. På samme 
     måte som alle luftpartiklene inne i en ball er en del av luften inne i 
     ballen.) 
     
4. Dette kan man videre bruke til segmentering av 3 dimensjoner, hvor 
    enhver vinkel kan dekkes gjennom en tenkt projeksjon av den fullførte 
    figuren inn i bildeflaten. (Dermed former dette også en potensiell 
    bestanddel for "minne" eller "forestillingsevne" til et kapselnettverk.)

Over til faktisk utførelse: 
1. Implementering av OpenPose. 

2. Forsøk i metoder for å separere mennesket ved hjelp av 

"""




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



