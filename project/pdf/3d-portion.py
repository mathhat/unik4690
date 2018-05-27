
# -*- coding: utf-8 -*-

from LatexTemplate import *
Type = Template(Title = "Ignore. Import content3 from here. ") #<----- Header title
#^additional vars: author(str), date(str), landscape(boolean) 
#---create content as raw string below--# 
#----------using LaTeX-format-----------#  
content3 = r'' #creating initial content, 
#------------content below--------------# 
content3 += r''' 
\section*{The Geometric Motivation: }
This is a short section/chapter covering the motivation to use 
Geometric shapes for our segmentation, and some mathematically nice qualities 
of these shapes. 
\subsection'{Platonic Solids:}
From the ancient times there has been a special place for what was known then 
as Platonic solids. These were thought to be sacred shapes that described 
something True, and for our intents and purposes that might as well be true. 

These shapes are indeed special, including but not limited to the cube, 
the pyramid, and the dodocahedron.

Essential qualities of these are that they are polygons, and therefore 
also convex shapes. As a curiosity these were traditionally combined 
into a single shape, called the Metatron's Cube. 
\subsection*{Convexity: }
A set, C, is said to be convex if $\forany x,y \in C$ and $t \in [0,1]$ the 
following is always true:
\begin{equation}
(1 - t)x + yt \in C
\end{equation}
This is trivially true, perhaps, for polygons, but it is essential 
when considering our project. 

\subsection*{Projection of Convex Shapes:}
Basic Assumption: 
The projection of a 3D, Convex shape to a 2D image-surface will form a 
2D Convex Shape. (This assumption is true, but will not be proven here)

Knowing that this is the case, the following preposition is an important 
bit of logic for our project. 

\subsection*{Geometric assumptions, and our Project:}
If we assume that a body is a combination of polygons, and other convex 
shapes such as spheres, then from an image of a set of polygons we can infer a 3D shape. 

We do this every day when we assume that, e.g. an apple has a 3D shape, even 
though we can only see an image of it. 

When we look at a head, we will assume it has a spheroid upper portion, and a 
jaw-structure which is similar to a bumpy semi-cylinder. 

The image we see is undeniably 2D, and yet we have an underlying assumption of the 
shape based on knowing key-facts, and associating them with keypoints. 

Conceptually then; it makes sense to endow the machine's vision with these same 
suppositions. Essentially to couple keypoints with geometric shapes. 
Using pose to extract rotation and keypoints then, we can theoretically form 
a human being composed entirely of convex shapes, and as noted this can 
be extended into assumptions as to the 3 dimensional shape of things. 

This is not unlike how people have created human figures in video-games. 

\subsection*{Vision and Segmentation Geometrically:}
Vision in human beings is not an easy thing to emulate. Specifically 
our vision seems to be filtered through visual centers, creatively named V1, V2, etc.. 
What these visual centers seem to do is isolate qualities about the image you're perceiving. 
\url{https://en.wikipedia.org/wiki/Visual_cortex}

What we may call the secondary portion of vision relates to the projected expectations 
we have. That is, if a face turns to the side, we expect the head to expand backwards relative to the face, 
and we would be surprised if it did not. (See \url{https://en.wikipedia.org/wiki/Mental_rotation})

In terms of what is happening in our human vision, there are theories to support 
we are operating on what's known as the Dorsal Stream. 
(\url{https://en.wikipedia.org/wiki/Two-streams_hypothesis#Dorsal_stream})

In other words; in our human vision there are expected results from rotation of an object 
that stem from our experience in a three dimensional world. Borrowing some of this 
in an attempt to improve upon the machine vision, seems to us to make sense. 

This is part of what Hinton (et. al.) uses to create the theory of Capsule Networks. 
(For more on CapsNet, we suggest this series of articles: \url{https://medium.com/ai%C2%B3-theory-practice-business/understanding-hintons-capsule-networks-part-i-intuition-b4b559d1159b})

\subsection*{Our Concept:}
For these reasons our algorithm was created to use geometric relations to generate a 
collected set of 2D convex shapes that change and morph with respect to the pose.
The shape of our segmentation is a collection of ellipses and polygons, which 
with more time can be expanded to heuristically understand what possible 3D shapes 
form these on an image-surface. 

For the 3D underlying shapes one has to actually rotate the object, remembering the previous 
rotations, keeping track of the object to ensure one does not "learn" the wrong things, and 
from this infer the correct geometric shape(s). (This would require us to create a LSTM or something similar, 
and was for that reason not included in the current scope.)



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
        Type.Typeset('3d-portion',showpdf=False) # <-filename
    except: 
        pass



