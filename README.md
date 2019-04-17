# Movie Data Analysis from 2014 to 2018

## Team Members:

Zeyu Yan, George Bendele & Mrinalini Darswal

## Project Description:

We will analyze all the movie data from 2014 to 2018 (the past 5 years) to see what interesting trends we can reveal. (Finished)

**Extra:** Train a classifier to classify the sentiment of movie reviews. The accuracy of the classifier should be at least over 85%. (Finished)

**Optional:** Analyze on all of the Marvel movie data to reveal interesting trends. (Data already gathered, but not enough time to finish)

## Where to get the data?

We plan to retrieve detailed movie data using the [OMDB API](http://www.omdbapi.com/). However, we cannot retrieve movie data by year directly using [OMDB API](http://www.omdbapi.com/). To solve this problem, we need to have lists of moive names for each year from 2014 to 2018. A complete list of movie names by year can be found from [Wikipedia](https://www.wikipedia.org/). Following are links for the lists of movie names from 2014 to 2018:
* [2018 Movie List](https://en.wikipedia.org/wiki/2018_in_film)
* [2017 Movie List](https://en.wikipedia.org/wiki/2017_in_film)
* [2016 Movie List](https://en.wikipedia.org/wiki/2016_in_film)
* [2015 Movie List](https://en.wikipedia.org/wiki/2015_in_film)
* [2014 Movie List](https://en.wikipedia.org/wiki/2014_in_film)

To get the lists of movie names from the webpages, we wrote web crawlers to crawl the useful information. The web crawler Python files have been uploaded to the same Repo as this README file. After using web crawler to crawl the lists of movie names for each year from 2014 to 2018, we then looped through the list of movie names for each year to get the detailed movie information through [OMDB API](http://www.omdbapi.com/) and saved the data as seperate .CSV files for each year.

For the **Extra** sentiment analysis part, the training and testing data we used are from [Large Movie Review Dataset v1.0](https://www.kaggle.com/iarunava/imdb-movie-reviews-dataset).

For the **Optional** Marvel movie data analysis part, we also used a web crawler to crawl the list of Marvel movie names from https://www.boxofficemojo.com/franchises/chart/?id=avengers.htm (by the time we crawled the data, the data of "Captain Marvel" was not yet available). Then we also looped through the list of Marvel movie names to the detailed movie information through [OMDB API](http://www.omdbapi.com/) and saved the data into a .CSV file. The web crawler Python files for this part have also been uploaded to the same Repo as this README file.

## Related Files

* For the analysis on the movie data from 2014 to 2018, please refer to [movie_data_analysis_final.ipynb](https://github.com/DataNoob0723/Movie-Data_Analysis_Project/blob/master/movie_data_analysis_final.ipynb).
* For the IMDB movie reviews sentiment analysis, please refer to [imdb_sentiment_analysis.ipynb](https://github.com/DataNoob0723/Movie-Data_Analysis_Project/blob/master/imdb_sentiment_analysis.ipynb).
* The train and test datasets for IMDB movie reviews are in [imdb_sentiment_data.zip](https://github.com/DataNoob0723/Movie-Data_Analysis_Project/blob/master/imdb_sentiment_data.zip).
* [data_loader.py](https://github.com/DataNoob0723/Movie-Data_Analysis_Project/blob/master/data_loader.py) is used to load the IMDB movie reviews datasets and save them as Pickle files for later use.
* All of the movie data we used for analysis for this project are in the [data](https://github.com/DataNoob0723/Movie-Data_Analysis_Project/tree/master/data) folder.
* For all of the web crawlers, please refer to [web crawlers](https://github.com/DataNoob0723/Movie-Data_Analysis_Project/tree/master/web%20crawlers) folder.

## Results & Conlusions

### Analysis on All the Movie Data from 2014 to 2018

The top 20 highest box office moveis from 2014 to 2018 are shown in the following figure. "Avengers: Infinity War" is the box office champion for the past 5 years. "Rogue One: A Star War Story" and "Jurassic World" are the 2nd and 3rd.
    
![top 20 movies](https://github.com/DataNoob0723/Movie-Data_Analysis/raw/master/images/bo_top20_movies.png)

The top 20 actors with the highest accumulative box office from 2014 to 2018 are shown in the following figure. Chris Evans is the accumulative box office champion for the past 5 years. Robert Downey Jr. is right behind him and really close.

![top 20 actors](https://github.com/DataNoob0723/Movie_Data_Analysis/raw/master/images/total_bo_top20_actors.png)

The top 20 directors with the highest accumulative box office from 2014 to 2018 are shown in the following figure. Russo Brothers are the accumulative box office champion for the past 5 years.

![top 20 directors](https://github.com/DataNoob0723/Movie_Data_Analysis/raw/master/images/total_bo_top20_directors.png)

The we want to analyze the performance of movies from different genres for the past 5 years. The following figure shows the total number of movies from different genres between 2014 and 2018. Note that one specific movie may belong to several different genres. From the figure, it is seen that the most popular genre for the past 5 years is "Drama".

![num genres](https://github.com/DataNoob0723/Movie_Data_Analysis/raw/master/images/genre_total_plot_1.png)

From the following figure, it is seen that in terms of accumulative box office, the genre "Adventure" is the champion for the past 5 years, although the genre "Action" is really close.

![bo genres](https://github.com/DataNoob0723/Movie_Data_Analysis/raw/master/images/genre_total_plot_2.png)

However, it is seen from the following figure that in terms of average box office, the genre "Sci-Fi" is the champion for the past 5 years. "Adventure" is right behind it and really close.

![avg bo genres](https://github.com/DataNoob0723/Movie_Data_Analysis/raw/master/images/genre_total_plot_3.png)

Then we want to investigate the trend of box office for the past 5 years. **The data for 2018 is eliminated for this analysis due to the number of samples are not large enough.** The following figure shows the plot of total box office from 2014 to 2017. It can be seen that from 2016, the total box office of the year has increased significantly.

![total bo](https://github.com/DataNoob0723/Movie_Data_Analysis/raw/master/images/total_bo_plot.png)

The following figure shows the average box office for each year from 2014 to 2017. It can be seen that among these 4 years, 2015 has the lowest average box office and 2016 has the highest box office. It should be noticed that although 2017 has much higher total box office comparing to 2014, the average box office of these 2 years are quite close. The reason for this is that 2017 has more movies released compared to 2014.

![avg bo](https://github.com/DataNoob0723/Movie_Data_Analysis/raw/master/images/avg_bo_plot.png)

Finally, we investigate the average rating of the movies from 2014 to 2018. We gathered the rating data from 3 diffrerent sources: IMDB, Rotten Tomatoes and Metacritic. From the follwing figure, it is seen that the trend of rating from all 3 sources are basically the same. It is intereting to notice that year 2015 has the lowest total and average box office, but has the highest average rating among the past 5 years. This interesting result reveals that this is no direct relation between the rating of the movies and their box office.

![avg ratings](https://github.com/DataNoob0723/Movie_Data_Analysis/raw/master/images/avg_rating_plot.png)

### Extra: IMDB Movie Reviews Sentiment Analysis

For this part, our goal is to train a classifier which is able to distinguish between positive and negative movie reviews. The accuracy should be at leat over 85%. 

#### 1. Preprocessing the Data

For the IMDB movie review data, we performed some basic cleanings through string operations and Regular Expression. After cleaning, we vectorized the texts into TF-IDF models with dimensions of 5000.

#### 2. Testing Baseline Algorithms

The baseline algorithms we are tesing are:

* Logistic Regrssion
* Linear Discriminant Analysis
* Decision Tree
* Gaussian Naive Bayes
* Linear SVC

First of all, we compared the performance of the above 5 baseline algorithms on the same training dataset (size 25000) using 10-fold cross-validation. It turned out that Logistic Regression (with an average 10-fold accuracy of 88.42%) and Linear SVC (with an average 10-fold accuracy of 87.46%) are the top two algorithms with better performance.

|Method Name   |10-Fold Avg Accuracy   |10-Fold Accuracy STD  |
|:------------:|:---------------------:|:--------------------:|
|Logistic Regression|0.8842|0.0058|
|Linear Discriminant Analysis|0.8591|0.0067|
|Decision Tree|0.7130|0.0065|
|Gaussian Naive Bayes|0.8003|0.0094|
|Linear SVC|0.8746|0.0065|

The next step is to try to further tune the parameters of Logistic Regression and Linear SVC to see if we can achieve even better performance. It turned out that the best performance of Logistic Regression is 88.42% (with C = 1) and the best performance of Linear SVC is 88.37% (with C = 0.25). Their best performances are really close. Therefore, we decided to test these two algorithms with their optimal parameters on the test set to finally pick the one with better performance.

|C Value for LR|10-Fold Avg Accuracy|10-Fold Accuracy STD|
|:------------:|:---------------------:|:--------------------:|
|0.01|0.8429|0.0074|
|0.05|0.8590|0.0070|
|0.25|0.8764|0.0064|
|0.5|0.8814|0.0057|
|1|0.8842|0.0058|

|C Value for LSVC|10-Fold Avg Accuracy|10-Fold Accuracy STD|
|:------------:|:---------------------:|:--------------------:|
|0.01|0.8659|0.0068|
|0.05|0.8825|0.0053|
|0.25|0.8837|0.0040|
|0.5|0.8789|0.0041|
|1|0.8746|0.0065|

Running the above two algorithms with their optimal parameters on the same test dataset (size 25000) respectively, Logistic Regression eneded up with an accuracy of 88.08% and Linear SVC ended up with an accuracy of 87.78%. The performane of Logistic Regression is slightly better than Linear SVC, therefore, we chose Logistic Regression as our final choice and the best model ended up with a performance of 88.08%, which satisfied our minimum requirement (at least over 85%).

## Future Work

This is actually a large project and a lot more can be done. Due to the time limitation, we only finished the aforementioned analysis. The following are some further topics or improvements which could be investigated in the future.

For movie data analysis, the simpliest improvement is to gather more data. Currently we are conducting our research only on the data for the past 5 years. Past 10 years' or 20 years' data would be even better. Time-series analysis could also be conducted using Reccurent Nerual Network. Howver, the conclusion/trends drawn directly from time-series analysis may not be reliable enough. Further investigations on the reasons which cause the trends of the time-series are necessary.

For IMDB reviews sentiment analysis, the following are some techniques which can be investigated to further improve the classifier performance:

* Try ensemble methoed. Two kinds of ensemble methods can be investigated:
    * Boosting Methods: AdaBoost (AB) and Gradient Boosting (GBM)
    * Bagging Methods: Random Forests (RF) and Extra Trees (ET)
* Use N-Gram models to vectorize the texts.
* Use Word Embedding technique to vectorize the texts.
* Train a Recurrent Neural Network as the classifier.

## Special Thanks to George

Thanks to George since he also did a lot of work for this project. Since we have too much content and we ran out of time to integrate all of them, George's work is upload in the folder caller "George's work" in this Repo. Thanks to him for his great effort and excellent work!!!
