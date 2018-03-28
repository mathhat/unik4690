

#include <opencv2/videoio.hpp>
#include <opencv/cv.hpp>
#include <iostream>
int main()
{
    cv::VideoCapture input_stream(0);

    if(!input_stream.isOpened()){
        std::cerr << "could not open camera\n";
        return EXIT_FAILURE;
    }
    const std::string window_title = "Lab 0: Introduction to OpenCV";
    cv::namedWindow(window_title,cv::WINDOW_NORMAL);



    cv::Mat frame;

    cv::Mat frame2;

    cv::Mat kernel = (cv::Mat_<char>(3,3) <<  0, -1.,  0,
                                            -1,  2. , 0,
                                            0, 0,  0);
    cv::filter2D(frame,frame2,frame.depth(),kernel);


    while(true)
    {
        input_stream >> frame;

        if (frame.empty())
        {break;}

        //cv::Canny(frame,frame2,40,80);
        //cv::blur(frame,frame,cv::Size(10,10));
        cv::filter2D(frame,frame2,frame.depth(),kernel);
        cv::imshow("cam",frame2);

        if(cv::waitKey(15) >= 0)
        {break;}
    }
    return EXIT_SUCCESS;
}
/*
void (cv::Mat& matrix){
    for (int i = 0; i<matrix.cols*matrix.channels())

}
*/