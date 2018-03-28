#include "iostream"
#include "opencv/cv.hpp"
using namespace cv;
using namespace std;
int main(int argc, char** argv){

    if (argc < 3){
        cout << "put the images' names you want to blend into the cmd call";
        return 0;
    }

    Mat image1; //image 1 and to will be fused linearly
    Mat image2;
    Mat image3; //this is their product
    
    image1 = imread(argv[1],1);
    image2 = imread(argv[2],1);
    image3;
    
    addWeighted(image1,0.5,image2,0.5,0,image3);

    image3 = Scalar::all(150)-image3;

    imshow("red n green?", image3);
    waitKey(0);
}