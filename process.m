clc;clear all;close all;
%% Read Image
img = textread('human_corridor_0.txt');
mask = img;
mask(mask < 1.8 | mask > 4) = 0;
mask(mask>0) = 255;
mask = logical(mask);
imshow(mask,[]);
BW2 = bwareafilt(mask,3);
imshow(BW2)
%% After applying filter
imgnew = img .*BW2;
imshow(imgnew,[])

%% Calculation of 3D Points
[dist, side] = 


dist = 2.381; x= 149 ; y= 81 ;
px = dist *(x/175 - 0.5)*tand(35);
py = dist *(y/131 - 0.5)*tand(25);
pz = dist;
Px =[];
Py= [];
for x= 1:163
    px = imgnew(y,x) *(y/175 - 0.5)*tand(35);
    py = imgnew(y,x) *(x/131 - 0.5)*tand(25);
    Px= [Px;px]; 
    Py= [Py;py];   
end

peopleDetector = vision.PeopleDetector;
[bboxes,scores] = peopleDetector(BW2);