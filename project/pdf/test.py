
# -*- coding: utf-8 -*-

from LatexTemplate import *
Type = Template(Title = "UNIK 4690 Computer Vision Project\\\ Pose \& Seg \\\ \small{\href{https://github.com/mathhat/unik4690/tree/master/project}{Source}}", author="Joseph Knutson \& Jacob Alexander Hay") #<----- Header title
#^additional vars: author(str), date(str), landscape(boolean) 
#---create content as raw string below--# 
#----------using LaTeX-format-----------#  
content = r'' #creating initial content, 
#------------content below--------------# 
content += r''' 


%\section*{Mulige kilder til segmentering:} 
%\url{https://www.cs.cmu.edu/~hebert/boundaries.htm}
\clearpage
\section*{Introduction}
Object Detection is a field within Computer Vision with the purpose of detecting objects of different classes. These classes of objects range from
footballs to pedestrians. There are many methods for detecting the latter, but sadly, most of these methods care not to specify the position of 
a person in its entirety. 
Instead, some methods return rectangular patches where the person resides, while others return only a handful of key-points.
\\
\\
This project combines modern pose detection methods, like the one introduced by $Toshev \ et\ al\ (2014)$ \cite{swag}, with image processing and feature detection methods like Laplacian Blending and Edge Detection 
in order to not only detect people in images, but to better describe which pixels they inhabit. 
Once the human's pixels are extracted, we transfer them to other images via image blending. Like a green screen without a green screen.
\\
\\
The following chapters will discuss what tools we've used and roughly touch on the theory behind them. We'll clarify what we've borrowed from others. Which things we've implemented during our process, both that which works and that which doesn't.
And finally, we point out what we wish to improve and further implement.


%\section*{Background}
%Green Screens, are used in movies, series, news, video-games and home-made videos with the main reason of providing an artificial background. The technique requires an
%approximately monochrome and plain background (often green) to be placed behind whatever is wanted in the foreground (often a person). When the green screen is placed, 
%a technique called Chroma Keying is applied in order to map where the plain green surface is. When the location of the green pixels are knows, a CGI, Computer Generated 
%Image, is mapped onto these pixels, making it seem like the person is standing in front of whatever is put in the back.
%\\
%\\
%Our algorithm provides a Green Screen tool for people, without having to place a Green Screen behind them. Our algorithm requires only 1 camera and has no dependence on color segmentation.
%Even though Computer Vision has taught us powerful, color based segmentation methods, they rely on plain backgrounds. Colour based segmentation is therefore not in our interest, as we seek to create something more flexible.
%Instead of using gaussian classification on the local colorspace to extract people from the image, we propose a method relying on feature detection, contouring and laplacian blurring, as an alternative.

\section*{Theory}
This chapter presents the methods we've used and a little bit about the theory behind them.
\subsection*{Pose Detection}
Pose Detection is a computer vision technology which aims to detect key-points points, often on a person's body, in order to define
that object's pose. Pose is in this case the translational information of the person in the image, its position in other words. In image 
\ref{fig:pose1} you can observe the algorithm\footnotemark \footnotetext{This algorithm was written by OpenPose\\Link to source: https://github.com/ildoonet/tf-pose-estimation} at work.
The pose detection algorithm is the basis for our project, and as you can see, it finds key-points on both bodies and faces.
\\
\\
\begin{figure}\centering
\includegraphics[width=0.6\textwidth]{smile}
\caption{Pose detection algorithm which finds key body-points.}
\label{fig:pose1}
\end{figure}
There are many ways to go about pose-detecting. The method we have borrowed from OpenPose is a modern method based on deep-learning, first presented by \cite{swag} in 2014.
The algorithm is built upon a deep convolutional neural-network developed by Carnegie Mellon University with help of COCO and MPII datasets.
This deep convolutional neural network has a generic DNN architecture, consisting of several layers -- each being a linear transformation followed by a non-linear one. The first layer takes
as input an image of predefined size. The further convolution of this image can be observed in image \ref{fig:pose2}. The network's output is, as we saw, the key-points of the person's joints and face.
\begin{figure}\centering
\includegraphics[width=1\textwidth]{deep}
\caption{Diagram of the pose detection DNN, showing the convolutional behavior of this kind of network.}
\label{fig:pose2}
\end{figure}
\clearpage
\subsection*{Edge Detection}
Edges can be both basic yet informative features in images. A basic way of finding edges is to look for large changes in pixel values along the x and y axes.
This is equivalent to finding the gradient, or derivative of the image function. Mathematically, we can express the edge intensity in a pixel as the difference between its neighbouring pixels' values:
\begin{equation}
I_e(x,y) = |I(x-1,y) - I(x+1,y)| + |I(x,y-1) - I(x+1,y+1)|
\end{equation}
where $I_e$ is the pixel value in the new edge image, $I$ is the pixel value in the original image, and x and y are image coordinates.
There are many more methods to finding edges that add more complexities, like using the Laplacian or adding threshold techniques. A famous edge detector function 
found in Open CV, called Canny works its magic in image \ref{fig:canny}
\begin{figure}\centering
\includegraphics[width=.6\textwidth]{canny}
\caption{The Canny function detects edges in an image. It also includes threshold parameters which can reduce noisy details.}
\label{fig:canny}
\end{figure}

\subsection*{Image Pyramids and Laplace Blending}
Laplace blending is an important part of our algorithm. The idea of Laplace blending is to first create a Gaussian and Laplacian pyramid for
two different images, use a ramp-filter to define the overlapping behaviour they should have, and then collapse the overlapping image pyramids.
Image \ref{fig:lap1}, \ref{fig:lap2}, and \ref{fig:lap3} are intuitive lecture slides from our course that explain the smooth image merging that Laplace blending offers.
Not only do we use these pyramids for Laplace blending, we also use them for contouring.
\begin{figure}\centering
\includegraphics[width=.6\textwidth]{lap1}
\caption{The Gaussian image pyramid.}
\label{fig:lap1}
\end{figure}
\begin{figure}\centering
\includegraphics[width=.7\textwidth]{lap2}
\caption{The Laplacian pyramid.}
\label{fig:lap2}
\end{figure}
\begin{figure}\centering
\includegraphics[width=.7\textwidth]{lap3}
\caption{The conjoining of the images at multiple resolution levels with the help of a ramp/mask.}
\label{fig:lap3}
\end{figure}

\clearpage
\section*{Tools and Programming Language} 
\subsection*{Apparatus}
Our code can run live on webcam, so as long as you have a webcam, no matter how low-res it is, you can run our code.
If you want a decent fps, e.g. over 20 fps, you'll need a dedicated graphics card. 
\subsection*{Source that is not Our}
As previously stated, the DNN that finds key-points along the body is not written by us. It is however an important input for
the code we've written ourselves.
\subsection*{Python}
Our project is written in Python 2.7. The libraries we're using are Numpy, Open CV2, Numba and Sci-Kit Learn.
Numpy for matrix creation and matrix operations. Open CV is mainly used for edge detection, laplace blending, human modeling and morphological operations.
Numba is for compiling Python code into C++ before it's run. This is mainly for image normalization. Sci-Kit had some useful image resize functions.

\section*{Process} 
Along the long road towards a usable 2D segmentation we tried a few different 
approaches. 
\subsection*{Contours}
Our initial attempt at capturing the pixels of a human in the image consisted of using the Canny Edge detection algorithm.
This proved too difficult as a near perfect, closed curve around the individual was impossible to get. Our plan was to fill the contour once it became a closed curve, like MS paint's "fill" tool.
Image \ref{contour} shows the promising contours that we managed to produce.
\\
\\
\begin{figure}\centering
\includegraphics[width=.7\textwidth]{jesus}
\caption{The use of edges to create a closed curve proved difficult.}
\label{contour}
\end{figure}
\subsection*{Convex Contours}
Since the contours would'nt close themselves, we got the idea that we should try closing them by treating them as polygon vertices.
Using cv2.fillconvexPoly(), we made a last ditch effort to make contours work, resulting in image \ref{contour2}. Not too pretty. 
If our goal is to confine all the pixels of the person, this metod only covers half of them. Morphology didn't fix this.

\begin{figure}\centering
\includegraphics[width=.7\textwidth]{stuff2}
\caption{Open CV's FillConvexPoly algorithm was not fitting, but produced an interesting result on our open contour lines.}
\label{contour2}
\end{figure}


\begin{figure}\centering
\includegraphics[width=.7\textwidth]{dummy}
\caption{Geometric shapes based on the pose detection DNN. We started making a dummy to represent the human. This made it easy to find edges local to the person.}
\label{dummy}
\end{figure}

\subsection*{Body Estimation and Draw Functions}
We started making a model of the human body, a dummy, while working on the contouring (see image \ref{dummy}) and kept using it for Laplacian Blending too!
The dummy was a rough estimation of where the person's body was positioned, this helped us get rid of outside noise.
By simply using a Hamarand product (a sort of dot product between matrices, but with no reduction afterwards),
all edges outside of our dummy was annuled.
\\
\\
We implement several different draw-functions for head, jawline, torso, 
arms and legs. 
\begin{itemize}
\item[Head] This function finds keypoints; eyes, nose, ears, and neck. 
Generating a semicircle or ellipse that covers the base structure of the back of the cranium. 
\item[Jaw] This draws a set of vertices that form a square on bottom, and vertices at about 45 deg 
angle from the eyes to cover noses or chinbones. 
\item[Torso] The torso is drawn in as two opposing semi-ellipses, which can be thought of as a 
slightly chubbied hour-glass. 
\item[Arms \& legs] These are in our model assumed to be approximately cylindrical. So we draw 
thick lines or squares that cover these, keeping with the theory that the 2D projection of a 
cylinder, or cone-section (non parallel cylinder sides), will form a square-like shape.
\item[Hands] Since our Pose-library doesn't feature hands, we decided to simply cover these by semicircles 
that somewhat cover the range of motion that these are likely to be found in.
\\
\\  
\end{itemize}

We kept improving the dummy, because we knew we could use it along other image processing techniques. 
Creating more limbs from lines, ellipses and quadrilaterals, using simple pose transformations based on the key-points returned by the DNN.
By making it dynamically grow and shrink based on pixel distances of the DNN's keypoints, it now mimics the human form quite well. 
As of now, the dummy looks like it does in image \ref{dummy2}. 

\begin{figure}\centering
\includegraphics[width=.6\textwidth]{swg}
\caption{More geometric shapes mimicing the person's body based on the pose detection DNN. Silly as it looks, a lot of works went into creating this guy (or girl).}
\label{dummy2}
\end{figure}

\subsection*{Laplace Blending}
With a human dummy that roughly fits over the person in the image, Jacob proposed to simply laplace blend the person into another image, using the
dummy as a ramp/mask. This gave some rather good results, but with a bit blurred out edges along the person (see figure \ref{1} and \ref{2}).

\begin{figure}\centering
\includegraphics[width=.5\textwidth]{1}
\caption{Using the dummy as mask for Laplace Blending}
\label{1}
\end{figure}

\begin{figure}\centering
\includegraphics[width=.5\textwidth]{2}
\caption{Laplace Blending of webcam stream and artificial background}
\label{2}
\end{figure}





\section*{Evaluation and Future Ambitions}

Our Green Screen has the potential to become more precise by combining it with a successful method for finding a closed contour around the person.
We were unable to implement a proper contour and ended instead up with a bulky Laplace Blending method for extracting the person's pixels instead.
\\
\\
We want to improve this code further, so that it can extract people from an image and used their pose and pixel values to recreate a model of them in 3D.
As we were given feedback, we were guided towards doing more image segmentation, and less of 
our primary concept to "scan" a human being into a 3D model.  
However, in order to do so, we would need to generate a 3D imaging tool which would allow 
us to both segment, capture, create a mosaic, and use something like ORBSLAM to keep track 
of the features and keypoints on this expansive surface that covers a human being. 
\\
\\
Along the way we would then need to be able to extract the portions of the image that 
correlates to the people in the image. Which essentially turns the program 
into a green-screen (without the green). 
\\
\\
Ideally we would have a code that can take any coupled set of Canonical shapes, and 
a Pose-detection software, map the Shapes to the Pose, and from there be able to extract 
the information necessary to create 3D models of people. 


\begin{thebibliography}{9}
\bibitem{swag} 
Alexander Toshev (Google), Christian Szegedy (Google). \\
\textit{DeepPose: Human Pose Estimation via Deep Neural Networks}. 2014.\\
Conference on Computer Vision and Pattern Recognition, 2014.
\\\texttt{http://openaccess.thecvf.com/content\_cvpr\_2014/papers/Toshev\_DeepPose\_Human\_Pose\_2014\_CVPR\_paper.pdf}\\
Google, 1600 Amphitheatre Pkwy, Mountain View, CA 94043
\end{thebibliography}



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

2. Forsøk i metoder for å separere mennesket ved hjelp av; 
   Canny edge, differential-bilde (endring per frame), Laplace-Pyramide-nivåer. 
   
3. Laplace Blending (milestone): Green screen 

4. Profit
    
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



