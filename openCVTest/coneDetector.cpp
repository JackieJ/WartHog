#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv\cv.h>
#include <opencv\highgui.h>

#include <iostream>
#include <stdio.h>
#include <queue>

using namespace std;
using namespace cv;

int Blue_min   =  0,
  Blue_max   =  150,
  Green_min  =  0,
  Green_max  =  150,
  Red_min    =  230,
  Red_max    =  270;

double Area_min = 500.0,
  Area_max = 2000000.0;

// parameters
int showImage = 1;

int BlueMin  = Blue_min,
  BlueMax  = Blue_max,
  GreenMin = Green_min,
  GreenMax = Green_max,
  RedMin   = Red_min,
  RedMax   = Red_max;

float areaMin = 500.0,
  areaMax = 20000000.0;

double screenCoverTarget = 0.5;

int main()
{
  Mat image;

  VideoCapture cap; // webcam class
  cap.open(0);	  // use webcam 0 <-- change this to work with the robot's webcam number

  //	cout << cap.set(CV_CAP_PROP_FRAME_WIDTH, 1152) << endl;
  //	cout << cap.set(CV_CAP_PROP_FRAME_HEIGHT, 720) << endl;

  cout << cap.set(CV_CAP_PROP_CONTRAST, .1) << endl;

  while(true){

    for(int n=0;n<2;n++){	// stores the pic from the webcam into image
      cap>>image;
      waitKey(33);
    } 

    if(showImage != 0){
      namedWindow("pre filter");
      imshow("pre filter", image);		// shows the image for debugging purposes
    }

    int b, g, r;			// used for the pixel values in the next for statements
    double whitePixels = 0;	// pixels in on state (white)			  
    // The following code filters the pixels so that only those 
    // that pass all three thesholds will show up in the final image

    for(int i=0; i<image.rows; i++){
      for(int j=0; j<image.cols; j++){
        b = image.at<Vec3b>(i,j)[0];
        g = image.at<Vec3b>(i,j)[1];
        r = image.at<Vec3b>(i,j)[2];

        if( b > BlueMin  && b < BlueMax  &&
				g > GreenMin && g < GreenMax &&
                                                    r > RedMin   && r < RedMax   )	{

          image.data[image.step[0]*i + image.step[1]* j + 0] = b;
          image.data[image.step[0]*i + image.step[1]* j + 1] = g;
          image.data[image.step[0]*i + image.step[1]* j + 2] = r;
          whitePixels++;
        }
        else {
          image.data[image.step[0]*i + image.step[1]* j + 0] = 0;
          image.data[image.step[0]*i + image.step[1]* j + 1] = 0;
          image.data[image.step[0]*i + image.step[1]* j + 2] = 0;
        }
      }
    } 
	
    if (showImage != 0){
      namedWindow("post filter");
      imshow("post filter", image);  // shows the image for debugging purposes
    }

    // blob dectection code
    cv::SimpleBlobDetector::Params params;
    params.minDistBetweenBlobs = 50.0f;
    params.filterByInertia = false;
    params.filterByConvexity = false;
    params.filterByColor = false;
    params.filterByCircularity = false;
    params.filterByArea = true;
    params.minArea = areaMin;			// Minimum blob size	<-- configure from tests
    params.maxArea = areaMax;			// Maximum blob size	<-- configure from tests

    Ptr<FeatureDetector> blob_detector = new SimpleBlobDetector(params);
    blob_detector->create("SimpleBlob");

    vector<cv::KeyPoint> keypoints;
    blob_detector->detect(image, keypoints);

    queue<float> xCoordinates;			// use a linked list to store the coordinates for the blobs
    // the code only uses the first one obtained 
    // I'm hoping there won't be more than one signal to follow

    // find the x coordinate for the center of the blobs

    for(int i = 0; i < keypoints.size(); i++){
      xCoordinates.push(keypoints[i].pt.x); 
    }

    double imageArea = image.rows * image.cols;
    double screenCover = (whitePixels / imageArea); // calculate the percentage of screen covered by the cone
	
    if(xCoordinates.empty())			// if there is no orange in the image
      {
        cout << 0 << endl;
      }
    else
      {
        if(screenCover > screenCoverTarget)		// if the image fills up at least a set percentage of the screen
          {
            cout << "screen filled" << endl;
          }
        else if(xCoordinates.front() < 270)	// if the image is on the left
          {
            cout << "left" << endl;
          }
        else if(xCoordinates.front() > 370)	// if the image is on the right
          {
            cout << "right" << endl;
          }
        else								// if the image is in the middle
          {
            cout << "middle" << endl;
          }
      }
  } return 0;
}
