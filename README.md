# Driving Distance

Algorithm for calculating driving distance and time between multiple points using Distance Matrix API from Google Maps. The input for this algorithm is an Excel spreadsheet with origins in one column and destinations in another. Works best when either origins or destinations are not all unique. In this case, destinations repeat so the data aren't considered row-by-row but a subset of the dataset is created for each distinct destination. Thus, given 10.000 rows and only 250 destinations, the number of API calls necessary is 520.

Case study and more information: https://mateuszwiza.medium.com/get-driving-distance-between-multiple-points-using-google-maps-distance-matrix-api-32b6feaa0d18

