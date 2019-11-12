# terrarium

A simple liner transformation tool created by me to learn python.

Looking forward to suggestions about functions I can implement. 

Snaglist:

-add live transform for scaling, rotation, translation with a bounding box
-add button for drawing mode, change add point to single click while in drawing mode
-add drawing primitive shapes menu

-bezier curves
  best solution, I think would be to add another list linked to the points list which will contain the tangents
  then when drawing lines connecting points check if tangent(xy)!=point(xy) for either point connected
  if True draw bezier curve, if false draw simple line
  variable for steps (precision of drawing)
  editing of tangents - can be added to the movePoint function - first we check if a point was selected then we check if a tangent was selected
  drawing of tangents
  locking tangents
  maths
  P = (1−t)3P1 + 3(1−t)2tP2 +3(1−t)t2P3 + t3P4

-change dimensions of the window
-calculate the final matrix from all the transforms and list the steps in a panel
-add shear transform

  
