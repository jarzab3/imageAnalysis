//package com.company;

import java.util.*;

/**
 * <h>Support Vector Machine</h>
 * <p>
 * SVM is a supervised machine learning algorithm which can be used for both classification or regression challenges. However,  it is mostly used in classification problems.
 * In this algorithm, we plot each data item as a point in n-dimensional space (where n is number of features you have) with the value of each feature being the value of a particular coordinate.
 * Then, we perform classification by finding the hyper-plane that differentiate the two classes very well
 * </p>
 */
public class SupportVectorMachine {

    private double[] w;

    private double b;

    //  Class  variables
    double maxFeatureValue;
    double minFeatureValue;

    /**
     * {||w|| : [w, b]}
     *
     * This function is responsible for entire training, where the hyperplane obtained is optimal.
     * For a linearly separable set of 2D-points which belong to one of two classes, finding a separating straight line.
     *
     * @param dataDict opt_dict = {}
     * @since 2018-03-01
     * @implSpec
     *  – w is a weight vector
     *  – x is input vector
     *  – b is bias
     */

//  SupportVectorMachine and
    public void fit(Dictionary<Integer, double[][]> dataDict) {

        Hashtable<Double, double[][]> optDict = new Hashtable<>();

        double[][] transforms = {{1, 1}, {-1, 1}, {-1, -1}, {1, -1}};

        List<Double> all_data;

        all_data = MyUtils.dictToList(dataDict);

        this.maxFeatureValue = Collections.max(all_data);

        this.minFeatureValue = Collections.min(all_data);

        double[] stepSizes = {this.maxFeatureValue * 0.1,
                this.maxFeatureValue * 0.01,
                this.maxFeatureValue * 0.001};

        int bRangeMultiple = 2;

        int bMultiple = 5;

        double latestOptimum = this.maxFeatureValue * 10;

        for (int s = 0; s < stepSizes.length; s++) {
            double step = stepSizes[s];

            double[] wTemp = {latestOptimum, latestOptimum};

//          System.out.println("---===> " + wTemp[0] + "  " + wTemp[1]);

            boolean optimized = false;

//          1) Identify the right hyper-plane. Identify the right hyper-plane to classify 1 and -1 classes
            while (!optimized) {

                double from = -1 * this.maxFeatureValue * bRangeMultiple;
                double limit = this.maxFeatureValue * bRangeMultiple;
                double rangeStep = step * bMultiple;

                while (from <= limit) {
                    this.b = from;
                    from = from + rangeStep;

//                  2) Identify the right hyper-plane
                    for (int ii = 0; ii < transforms.length; ii++) {
                        double[] transformation = transforms[ii];

                        double[] wt = MyUtils.multiplyArray(wTemp, transformation);

                        boolean foundOption = true;

//                      Iterate through all data and find all keys and put them into an array then it will be easier to sort in required order.
                        Enumeration<Integer> key = dataDict.keys();
                        while (key.hasMoreElements()) {
                            int i = key.nextElement();

                            double[][] value = dataDict.get(i);

                            for (double[] xi : value) {

//                               Perform dot.product of two vectors
                                if (!(((double) i * MyUtils.dotProduct(wt, xi)) + this.b >= 1)) {
                                    foundOption = false;
                                }

                            }

                        }

//                      Here, maximizing the distances between nearest data point (either class) and hyper-plane will help us to decide the right hyper-plane. This distance is called as Margin.
                        if (foundOption) {

                            double[][] tempArray = {wt, {this.b}};

                            double optKey = MyUtils.vectorMagnitude(wt, false);

                            optDict.put(optKey, tempArray);

                        }
                    }
                }


                if (wTemp[0] < 0) {
                    optimized = true;
                    System.out.println("Optimized one step");
                } else {

                    for (int i = 0; i < wTemp.length; i++)
                        wTemp[i] = wTemp[i] - step;
                }

            }

            ArrayList<Double> norms = new ArrayList<Double>();

            Enumeration<Double> key = optDict.keys();

            while (key.hasMoreElements()) {

                double keyToAdd = key.nextElement();

                norms.add(keyToAdd);

            }

            Collections.sort(norms);

//          ||w|| : [w,b]

            double[][] optChoice = optDict.get(norms.get(0));

            this.w = optChoice[0];
            this.b = optChoice[1][0];

            latestOptimum = optChoice[0][1] + step * 2;

//          ||w|| : [w,b]

        }
    }

    /**
     * Identify the right hyper-plane
     *
     * @param x
     * @param wl
     * @param b
     * @param v
     * @return double Result for a hyperplane
     */
    public double hyperPlane(double x, double[] wl, double b, double v) {
        double result;

        result = (-wl[0] * x - b + v) / wl[1];
        System.out.println("Hyperplane debug: " + result + " x " + x + " wl 1 " + wl[0] + " 2 " + wl[1] + " b " + b + " v " + v);
        return result;
    }


    /**
     * This function is performing last calculations for hyperplanes and prints results
     *
     * @since 2018-03-04
     * @return void
     */
    public void getResults() {

        double[] dataRange = {this.minFeatureValue * 0.9, this.maxFeatureValue * 1.1};

        double hypXmin = dataRange[0];
        double hypXmax = dataRange[1];

//      (w.x+b) = 1
//      Positive support vector hyperplane
        double psv1 = hyperPlane(hypXmin, this.w, this.b, 1);
        double psv2 = hyperPlane(hypXmax, this.w, this.b, 1);

        System.out.println("Positive hyperplane: " + hypXmin + " " + hypXmax + " " + psv1 + " " + psv2);


//      (w.x + b) = -1
//      Negative support vector hyperplane
        double nsv1 = hyperPlane(hypXmin, this.w, this.b, -1);
        double nsv2 = hyperPlane(hypXmax, this.w, this.b, -1);

        System.out.println("Negative hyperplane: " + hypXmin + " " + hypXmax + " " + nsv1 + " " + nsv2);

//      (w.x+b) = 0
//      Boundary support vector hyperplane
        double db1 = hyperPlane(hypXmin, this.w, this.b, 0);
        double db2 = hyperPlane(hypXmax, this.w, this.b, 0);

        System.out.println("Boundary hyperplane: " + hypXmin + " " + hypXmax + " " + db1 + " " + db2);
    }


    /**
     * This function will be able to classify additional data based on what the machine has learned so far.
     *
     * Sign (x * w + b)
     *
     * @param features
     * @return double result for prediction
     */
    public double predict(double[] features) {

        double classfication = MyUtils.sign(MyUtils.dotProduct(features, this.w) + this.b);

        return classfication;
    }

}
