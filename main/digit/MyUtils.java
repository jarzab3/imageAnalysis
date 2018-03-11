//package com.company;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;
import java.net.URL;
import java.util.*;


import java.io.*;

/**
 * <h1>Utilities functions for Euclidean algorithm!</h1>
 * The MyUtils methods implements an application that
 * simply allows user to read files, calculate distances and train data.
 * <b>TODO:</b>
 * 1) Improve comments
 * 2) Add analytics
 * 3) Add to page
 *
 * @author Adam Jarzebak
 * @version 1.1
 * @since 2018-02-15
 */
public class MyUtils {

    /**
     * Read the data from the file
     *
     * @param filename
     * @param webURL
     * @param webPath
     * @return data
     * @throws IOException On input error.
     * @see IOException
     *
     */
    public static int[][] readFile(String filename, boolean webURL, String webPath) throws IOException {

//      Initialize an empty array list where a data from file will be stored.
        ArrayList<String> strs = new ArrayList<String>();

//      By default is set up to download data from web, but if this fails then switch to local data.

        if (webURL) {
            URL connection = new URL(webPath);

            System.out.println("Successfully opened stream to: " + webPath);

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(connection.openStream()));

            String strline = null;
            while ((strline = in.readLine()) != null) {
                strs.add(strline);
            }

            System.out.println("Received data from url");


        } else {

            try {
                FileInputStream instream = new FileInputStream(filename);
                DataInputStream datain = new DataInputStream(instream);
                BufferedReader br = new BufferedReader(new InputStreamReader(datain));

                String strline = null;
                while ((strline = br.readLine()) != null) {
                    strs.add(strline);
                }

                datain.close();

//          Catch any IO error and throw exception if any occurs.
            } catch (Exception e) {
                e.printStackTrace(System.out);
            }
        }

        int[][] data = new int[strs.size()][65];
        for (int i = 0; i < strs.size(); i++) {
            String str = strs.get(i);
//          Separate data by comma a separator.

            String[] el = str.split(",");
            for (int j = 0; j < el.length; j++) {
                data[i][j] = Integer.valueOf(el[j]);
            }
        }

//      Return data retried from a file
        return data;
    }

    /**
     * This function prints one dimensional array
     *
     * @param arrIn
     * @throws IllegalArgumentException
     */
    public void printArray(int[] arrIn) {
        try {
            for (int anArrIn : arrIn) {
                System.out.print(anArrIn + " ");
            }
            System.out.println("\n");
        } catch (IllegalArgumentException e) {
            e.printStackTrace();
        }
    }

    /**
     * This function prints a two dimensional array
     *
     * @param arrIn
     * @param printLength
     * @throws IllegalArgumentException
     * @since 2018-01-12
     */
    public static void printArray2(double[][] arrIn, boolean printLength) {
        try {
//          For all elements in the array print values
            for (double[] anArrIn : arrIn) {

//              If printLength value is true then it will print length of arrays in an array
                if (printLength) {
                    System.out.println("\n" + "Length is: " + anArrIn.length);
                } else {
                    System.out.println("\n");
                }

                for (int j = 0; j < arrIn[0].length; j++) {
                    System.out.print(anArrIn[j] + " ");
                }
            }

        } catch (IllegalArgumentException e) {
            e.printStackTrace();
        }
    }

    /**
     * This function calculates Euclidean distance for n number of dimensions.
     *
     * @param point1
     * @param point2
     * @param dimensions
     * @return double: Total Euclidean distance for n dimensional array
     * @implNote dist(( x, y), (a, b)) = √(x - a)² + (y - b)² ...
     * @since 2018-01-18
     */
    public static double calcDistance(int[] point1, int[] point2, int dimensions) {
//      Variable total distance
        double distance;
        double tempResult = 0;

        for (int index = 0; index < dimensions; index++) {
            double q = (double) point1[index];
            double p = (double) point2[index];

//         Stores temporary value. Adding cumulatively.
            tempResult = tempResult + Math.pow((q - p), 2);
        }

//      Take a square root of total n dimensional points
        distance = Math.sqrt(tempResult);

        return distance;
    }


    /**
     * The activation function for svm. Function that takes an input and returns a sign of this number
     *
     * @param input
     * @return -1 or 1
     * @since 2018-02-10
     */
    public static int sign(double input) {

        if (input >= 0) {
            return 1;
        } else {
            return -1;
        }
    }

    /**
     * The Dot Product gives a number as an answer (a "scalar", not a vector).
     * The Dot Product is written using a central dot: a · b
     * This means the Dot Product of a and b
     * @param a
     * @param b
     * @return
     */
    public static double dotProduct(double[] a, double[] b) {
        double sum = 0;
        for (int i = 0; i < a.length; i++) {
            sum += a[i] * b[i];
        }
        return sum;
    }

    /**
     * Method to calculate cosine similarity between two digits.
     *
     * @param docVector1 : vector 1
     * @param docVector2 : vector 2
     * @return double cosine similarity value
     * @implNote Cosine similarity is a measure of similarity between two non-zero vectors of an inner product space that measures the cosine of the angle between them.
     * @since 2018-03-08
     */
    public static double cosineSimilarity(int[] docVector1, int[] docVector2, int dimensions) {
        double dotProduct = 0.0;
        double magnitude1 = 0.0;
        double magnitude2 = 0.0;
        double cosineSimilarity = 0.0;

//      docVector1 and docVector2 must be of same length
        for (int i = 0; i < dimensions; i++) {
            dotProduct += docVector1[i] * docVector2[i]; //a.b
            magnitude1 += Math.pow(docVector1[i], 2);  //(a^2)
            magnitude2 += Math.pow(docVector2[i], 2); //(b^2)
        }

        magnitude1 = Math.sqrt(magnitude1);//sqrt(a^2)
        magnitude2 = Math.sqrt(magnitude2);//sqrt(b^2)

//      When magnitudes of two vectors are not equal to 0 then calculate the dot product of these vectors.
        if (magnitude1 != 0.0 | magnitude2 != 0.0) {
//          a · b = ax × bx + ay × by
            cosineSimilarity = dotProduct / (magnitude1 * magnitude2);

        } else {
//          Otherwise returns 0
            return 0.0;
        }

//      Returns cosine similarity value for n dimensional data.
        return cosineSimilarity;
    }

    /**
     * Function that takes two arrays and multiply each of these values by themself.
     * @implNote Example: {1,2} x {2, 3} --> {2, 6}
     * @param array1
     * @param array2
     * @return an array of new values
     * @since 2018-03-03
     */
    public static double[] multiplyArray(double[] array1, double[] array2) {

        double[] newArray = new double[array1.length];

        for (int i = 0; i < array1.length; i++) {
            newArray[i] = array1[i] * array2[i];
        }

        return newArray;
    }

    /**
     * Functuion calculates the magnitude of a vector from its components, we take the square
     * root of the sum of the components' squares (this is a direct result of the Pythagorean theorem):
     *
     * @param vector
     * @param round
     * @return double magnitude
     * @since 2018-03-02
     */
    public static double vectorMagnitude(double[] vector, boolean round) {

        double magnitude;

        magnitude = Math.sqrt(Math.pow(vector[0], 2) + Math.pow(vector[1], 2));

        if (round){
            magnitude = Math.round(magnitude);
        }

        return magnitude;
    }

    /**
     * Function which takes an arrayList and duplicates its elements by variable 'times'
     * @param times
     * @param list
     * @since 2018-02-26
     */
    public static void duplicateList(int times, ArrayList<Double> list) {

        int listSize = list.size();

        for (int i = 0; i < listSize; i++) {

            for (int j = 0; j < times; j++) {
                Double temp = list.get(i);
                list.add(temp);

            }
        }
    }


    /**
     * Function converts 2d array into dictionary. Therefore it can be easier searched
     *
     * @param dataDict
     * @return Dictionary
     * @since 2018-03-19
     */
    public static List<Double> dictToList(Dictionary<Integer, double[][]> dataDict) {

        List<Double> all_data = new ArrayList<Double>();

        Enumeration<double[][]> element = dataDict.elements();

        while (element.hasMoreElements()) {
            double[][] a = element.nextElement();

            for (double[] i : a) {
                for (double j : i) {
                    all_data.add(j);
                }
            }
        }

        return all_data;
    }


    /**
     * @param pixel
     * @return grayArray an array of gray values from RGB colors
     * @since 2018-03-09
     */
    public static int printPixelARGB(int pixel) {
        int alpha = (pixel >> 24) & 0xff;
        int red = (pixel >> 16) & 0xff;
        int green = (pixel >> 8) & 0xff;
        int blue = (pixel) & 0xff;
//        For debug purpose, uncomment below line
//        System.out.println("argb: " + alpha + ", " + red + ", " + green + ", " + blue + " Grayscale: " + (red + green + blue + alpha) / 4);

        return (red + green + blue + alpha) / 4;
    }

    private static int[] marchThroughImage(BufferedImage image) {
//      Dimensions of the image
        int w = image.getWidth();
        int h = image.getHeight();

//      Temp index for an array write
        int arrayindex = 0;

//      New array for gray values
        int[] grayArray = new int[h * w];

        for (int i = 0; i < h; i++) {
            for (int j = 0; j < w; j++) {
                int pixel = image.getRGB(j, i);
                int gray = printPixelARGB(pixel);
                grayArray[arrayindex] = gray;
                arrayindex++;
            }
        }
        return grayArray;
    }

    /**
     * This function executes the conversion from image format to an array of gray values
     * @since 2018-03-09
     */
    public static int[] convertImageToGrayArray() {

        String imagePath = "digit.png";

        int[] grayArray = {};

        try {

            BufferedImage image = ImageIO.read(new File(imagePath));

            grayArray = marchThroughImage(image);

//            System.out.println(Arrays.toString(grayArray));

        } catch (IOException e) {
            System.err.println(e.getMessage());
        }

        return grayArray;
    }

}

