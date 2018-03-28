#include <iostream>
#include <opencv2/videoio.hpp>
#include <opencv/cv.hpp>
using namespace cv;
using namespace std;

int main(int argc, char** argv){
        if ( argc != 2 )
    {
        cerr<<"usage: DisplayImage.out <Image_Path>\n";
        return -1;
    }

    Mat image;
    Mat image2;
    //Rect r2(750,65,365,340); 


    image = imread(argv[1],1); //1 = color, I think 0 or negative is grey?
    Rect r(image.cols/2,0,image.cols/2,image.rows);
    
    if ( image.empty() )
    {
        printf("No image data \n");
        return -1;
    }
    /*
    for (int i = 0; i<image.cols*image.channels();i++){ //channels are color channels, like rgb 
        for (int j = 0; j<image.rows;j++){              //or brg = pixel[0] pixel[1] pixel[2]
            if (((i)%3)) //everything else than every third channel
            {               //value is zeroes out (leaves a red, green or blue pic)
                image.at<uchar>(j,i) = 0;//image.at<uchar>(j,i);
            }
        }
    }
    */
    blur(image,image2,Size(5,5));
    //Canny(image,image2,50,100);

    //namedWindow("title?",WINDOW_AUTOSIZE);
    //image(r) += Scalar::all(-100);
    //imwrite("blue.jpg",image);
    imshow("title?",image-image2);

    waitKey(0);
    return 0;

}