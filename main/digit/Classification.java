//package com.company;

/**
 * <p>
 * The distance between the two images can be calculated in many different ways. But I used the Euclidean distance algorithm.
 * The way it will be calculated for images is by summing the squared Euclidean distance between the corresponding pixels of two images.
 * </p>
 * @author Adam Jarzebak
 * @since 2018-02-21
 * @apiNote
 */
public class Classification {
    private boolean debug;
    private int secondIteration = 0;

    /**
     * @param debugMode
     */
    public Classification(boolean debugMode) {
        debug = debugMode;
    }

    /**
     * This function run training for a single point.
     *
     * @param point
     * @param trainingSet
     * @return boolean: If correctly recognized return true otherwise false
     */
    public boolean findMatch(int[] point, int[][] trainingSet, boolean debug1) {

        double currentDistance;

//      Digit that we are comparing with all other in training set
        int currentDigit = point[64];

//      Keep track of all found digits
        int indexFound = 0;

//      Calculates distance using Euclidean distance algorithm. And keep it as the shortest
        double shortestDistance = MyUtils.calcDistance(point, trainingSet[0], 64);

//      Repeat this step for the length of all data.
        for (int i = 1; i < trainingSet.length; i++) {
            currentDistance = MyUtils.calcDistance(point, trainingSet[i], 64);

//          Check if new calculated distance is shorter than the previous, if yes then replace shortest distance with new one.
            if (currentDistance < shortestDistance) {
                shortestDistance = currentDistance;
                indexFound = i;
            }
        }

//      For found index with shortest distance take out the digit
        int foundDigit = trainingSet[indexFound][64];

//      Check if the index of the smallest smallest distance to the point is the correct digit
        boolean matched = (currentDigit == foundDigit);

//      To let know if we enter cosineSimilarity iteration
        boolean issecondIteration = false;

//      If Euclidean distance could not find the right matched digit then enter this loop and repeat the task but this time will use cosine similarity function.
        if (!(matched)) {
            issecondIteration = true;

//          Keep track of of iterations in second loop
            secondIteration++;

            indexFound = 0;
//
            shortestDistance = MyUtils.cosineSimilarity(point, trainingSet[0], 64);

            for (int ii = 1; ii < trainingSet.length; ii++) {
                currentDistance = MyUtils.cosineSimilarity(point, trainingSet[ii], 64);

//              For debugging purposes, enabled from constructor.
                if (debug1) {
                    System.out.println("Current distance is: " + currentDistance + " Digit is: " + currentDigit + " searched point: " + trainingSet[ii][64]);
                }

                if (currentDistance < shortestDistance) {
                    shortestDistance = currentDistance;
                    indexFound = ii;
                }
            }

//          For found index with shortest distance take out the digit
            foundDigit = trainingSet[indexFound][64];

//          Check if digits are matched.
            matched = (currentDigit == foundDigit);
        }

//      Printing for debugging purposes
        if (debug) {

            System.out.println("\nSearched digit: " + currentDigit + " found digit: " + foundDigit + ". The shortest distance is: " + shortestDistance + " Matched:" + matched + " Cosine Similarity: " + issecondIteration + "\n");

        }

        return matched;
    }

    /**
     * This function run training for a single digit which comes from web interface.
     *
     * @param point
     * @param trainingSet
     * @return predictions: returns two prediction from two algorithms
     */
    public void findMatchWebInterface(int[] point, int[][] trainingSet, boolean debug1) {

        double currentDistance;

//      Digit that we are comparing with all other in training set
//        int currentDigit = point[64];

//      Keep track of all found digits
        int indexFound = 0;

//      Calculates distance using Euclidean distance algorithm. And keep it as the shortest
        double shortestDistanceEuclidean = MyUtils.calcDistance(point, trainingSet[0], 64);

//      Repeat this step for the length of all data.
        for (int i = 1; i < trainingSet.length; i++) {
            currentDistance = MyUtils.calcDistance(point, trainingSet[i], 64);

//          Check if new calculated distance is shorter than the previous, if yes then replace shortest distance with new one.
            if (currentDistance < shortestDistanceEuclidean) {
                shortestDistanceEuclidean = currentDistance;
                indexFound = i;
            }
        }

//      For found index with shortest distance take out the digit
        int foundDigitEuclidean = trainingSet[indexFound][64];

//      Check if the index of the smallest smallest distance to the point is the correct digit
//        boolean matched = (currentDigit == foundDigit);

//      To let know if we enter cosineSimilarity iteration
//        boolean issecondIteration = false;

//      Repeat the task but this time will use cosine similarity function.
//        if (!(matched)) {
//            issecondIteration = true;

//       Keep track of of iterations in second loop
//        secondIteration++;

        indexFound = 0;
//
        double shortestDistanceCosine = MyUtils.cosineSimilarity(point, trainingSet[0], 64);

        for (int ii = 1; ii < trainingSet.length; ii++) {
            currentDistance = MyUtils.cosineSimilarity(point, trainingSet[ii], 64);

            if (currentDistance < shortestDistanceCosine) {
                shortestDistanceCosine = currentDistance;
                indexFound = ii;
            }
        }

//      For found index with shortest distance take out the digit
        int foundDigitCosine = trainingSet[indexFound][64];

//       System.out.println("\nFound digit Euclidean: " + foundDigitEuclidean + ". Euclidean distance is: " + shortestDistanceEuclidean + "\n");
       System.out.println(foundDigitEuclidean);
//       System.out.println("\nFound digit cosine: " + foundDigitCosine + " Cosine similarity distance: " + shortestDistanceCosine + "\n");

    }

    /**
     * This function run a training for all points from a training data.
     * Training is run on another set of data which is provided
     *
     * @param trainingSet
     * @param testingSet
     */
    public void findMathForAllData(int[][] trainingSet, int[][] testingSet) {

//      Initialize all objects and set up progress bar
        ProgressBar bar = new ProgressBar();
        System.out.println("Process Starts Now!");
        int totalPrograss = trainingSet.length;
        bar.update(0, totalPrograss);

//      These values are used to keep track of right and incorrect guesses
        int correctGuess = 0;
        int incorrectGuess = 0;

//      For all elements in training set, perform findMatch function which is trying to guess a digit
        for (int i = 0; i < trainingSet.length; i++) {

            boolean matched = findMatch(trainingSet[i], testingSet, false);

            if (matched) {
                correctGuess++;
            } else {
                incorrectGuess++;
            }

//          Progress bar
            bar.update(i, totalPrograss);
        }

//      Below values are representing a results of classification process.
        System.out.println("Process Completed!");

        double errorRate = (double) incorrectGuess / (double) correctGuess;

        System.out.println("\nFor this classification found: " + correctGuess + " correctly recognized digits and " + incorrectGuess + " incorrectly recognized digits.");

        System.out.println("\nCorrectly recognized: " + (float) (100 - (errorRate * 10)) + "%");

        System.out.println("\nSecond iteration counter: " + secondIteration);

    }
}
