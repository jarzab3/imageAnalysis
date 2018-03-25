//package com.company;

import java.io.IOException;
import java.util.Arrays;

public class Main {

    /**
     * Main function where all execution happening.
     *
     * @since 2018-01-10
     * @author Adam Jarzebak
     * @param args
     * @throws IOException
     * @deprecated url and local connection.
     * @apiNote Please vision 'jarzebak.eu/ai/documentation' for more details
     * @implNote entire code as well as changes can be found on github account:
     */
    public static void main(String[] args) throws IOException {

        String basePath = System.getProperty("user.dir");

        String path1 = basePath + "/cw2DataSet1.csv";
        String path2 = basePath + "/cw2DataSet2.csv";

        int[][] trainingSet = MyUtils.readFile(path1, false, "http://jarzebak.eu/getDataSet1");
        int[][] testingSet = MyUtils.readFile(path2, false, "http://jarzebak.eu/getDataSet2");

//      The constructor for Classification class taken an boolean input, this enables more comments which can be useful for debugging.
        Classification classification = new Classification(true);

//      First fold test
//        System.out.println("\n----------->>>Start first fold test<<<-----------\n");
//        classification.findMathForAllData(trainingSet, testingSet);

//      Second fold test
//        System.out.println("\n\n----------->>>Start second fold test<<<-----------\n\n");
//        classification.findMathForAllData(testingSet, trainingSet);


//      Two single digits outside of planned data for the coursework
//        int[] d2 = {0, 0, 0, 0, 0, 0, 0, 0, 0, 63, 63, 63, 63, 63, 0, 0, 0, 0, 0, 0, 0, 63, 0, 0, 0, 0, 0, 0, 63, 63, 0, 0, 0, 0, 0, 0, 63, 0, 0, 0, 0, 0, 0, 63, 63, 0, 0, 0, 0, 0, 0, 63, 0, 0, 0, 0, 0, 0, 63, 0, 0, 0, 0, 0, 7};
//        int[] d3 = {0, 0, 0, 0, 0, 0, 0, 0, 0, 63, 63, 63, 63, 63, 0, 0, 0, 0, 0, 0, 0, 63, 0, 0, 0, 0, 0, 0, 63, 63, 0, 0, 0, 0, 0, 63, 63, 0, 0, 0, 0, 0, 0, 63, 63, 0, 0, 0, 0, 0, 63, 63, 0, 0, 0, 0, 0, 0, 63, 63, 63, 63, 63, 0, 2};

//      Convert image to array
        int[] grayImage = MyUtils.convertImageToGrayArray();

//        Web interface execution
//        System.out.println(Arrays.toString(testingSet[0]));
        classification.findMatchWebInterface(grayImage, trainingSet, false);

    }
}


