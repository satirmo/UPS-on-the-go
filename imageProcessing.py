import cv2;
import numpy as np;
from operator import truediv;
from math import sqrt;

def getDimensions( points ) :
    hull = cv2.convexHull( points );
    rect = [ x[ 0 ] for x in hull ];
    print( "0------" );
    print( rect );
    dim = [];

    for i in range( 4 ) :
        j = ( i + 1 ) % 4;

        dx = rect[ i ][ 0 ] - rect[ j ][ 0 ];
        dy = rect[ i ][ 1 ] - rect[ j ][ 1 ];
        dist = dx * dx + dy * dy;

        dim.append( sqrt( dist ) );

    dim.sort();

    ret = [];
    
    for i in range( 2 ) :
        val = truediv( dim[ 2*i ] + dim[ 2*i+1 ], 2 );
        ret.append( val );

    ret.sort();

    print( "*----" );
    print( dim );
    print( ret );

    return ret;

def detectContours( img, knownDimensionsId ) :
    # Reduce noise in the image
    '''cv2.imshow('init',img);
    cv2.waitKey(0);
    cv2.destroyAllWindows();'''

    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY );

    '''cv2.imshow('image',gray);
    cv2.waitKey(0);
    cv2.destroyAllWindows();'''

    blur = cv2.blur( gray, ( 5, 5 ) );
    blurInvert = ( 255 - blur );

    '''cv2.imshow('blur',blur);
    cv2.waitKey(0);
    cv2.destroyAllWindows();

    cv2.imshow('blurInvert',blurInvert);
    cv2.waitKey(0);
    cv2.destroyAllWindows();'''

    lower = np.array( [ 160 ] );
    upper = np.array( [ 255 ] );    

    shapeMask = cv2.inRange( blurInvert, lower, upper );
    masked = cv2.bitwise_and( blurInvert, blurInvert, mask = shapeMask );
    maskedInvert = cv2.bitwise_not( masked );
            
    '''cv2.imshow('maskedInvert', maskedInvert);
    cv2.waitKey(0);
    cv2.destroyAllWindows();'''

    ret, thresh = cv2.threshold( maskedInvert, 155, 255, 1 );
            
    '''cv2.imshow('threshhhhhh',thresh);
    cv2.waitKey(0);
    cv2.destroyAllWindows();'''
                
    contourImg, contours, hierarchy = cv2.findContours( thresh, 1, 2 );
    # cv2.drawContours(img, contours, -1, (0,255,0), 3);

    cv2.imshow('threshhhhhh',img);
    cv2.waitKey(0);
    cv2.destroyAllWindows();

    rects = [ ( -1, -1 ), ( -1, -1 ) ];

    for contour in contours :
        # print( contour[ 0 ] );
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        
        area = cv2.contourArea(box)

        if area > rects[ 1 ][ 0 ] :
            rects[ 0 ] = rects[ 1 ];
            rects[ 1 ] = ( area, box );

        elif area > rects[ 0 ][ 0 ] :
            rects[ 0 ] = ( area, box );

    print( rects[ 0 ] );
    print( rects[ 1 ] );

    dims = [ getDimensions( rect[ 1 ] ) for rect in rects ];
    ratios = [ truediv( x[ 0 ], x[ 1 ] ) for x in dims ];

    for dim in dims :
        print( truediv( dim[ 0 ], dim[ 1 ] ) );

    if abs( ratios[ 0 ] - cardRatio ) < abs( ratios[ 1 ] - cardRatio ) :
        knownId = 0;
        otherId = 1;

    else :
        knownId = 1;
        otherId = 0;

    cv2.drawContours(img,[ rects[ otherId ][ 1 ] ],0,(255,255,0),2);
    cv2.drawContours(img,[ rects[ knownId ][ 1 ] ],0,(0,0,255),2);

    print( knownDimensions[ knownDimensionsId ][ 0 ] );
    print( dims[ otherId ][ 0 ] );
    print( dims[ knownId ][ 0 ] );

    width = truediv( knownDimensions[ knownDimensionsId ][ 0 ] * dims[ otherId ][ 0 ], dims[ knownId ][ 0 ] );
    height = truediv( knownDimensions[ knownDimensionsId ][ 1 ] * dims[ otherId ][ 1 ], dims[ knownId ][ 1 ] );
    print( "width: ", width );
    print( "height: ", height );
    
    cv2.imshow('rect', img);
    cv2.waitKey(0);
    cv2.destroyAllWindows();

    return ( width, height );

knownDimensions = [ (2.125, 3.370) ];

if __name__ == "__main__" :
    cardRatio = 53.98 / 85.60;
    print( cardRatio );
    for i in range( 1, 4 ) :
        numStr = "0" + str( i ) if i < 10 else str( i );
        name = "img" + numStr + ".jpg";
        img = cv2.imread( name );
        res = cv2.resize(img,None,fx=0.15, fy=0.15, interpolation = cv2.INTER_CUBIC)

        dimensions = detectContours( res, 0 );
