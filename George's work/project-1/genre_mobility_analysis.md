

```python
#Import dependencies
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
from scipy.stats import ttest_ind
```


```python
#Read in data
data2014_df = pd.read_csv('data/movie_data_for_past_years/2014_movies_data.csv')
data2015_df = pd.read_csv('data/movie_data_for_past_years/2015_movies_data.csv')
data2016_df = pd.read_csv('data/movie_data_for_past_years/2016_movies_data.csv')
data2017_df = pd.read_csv('data/movie_data_for_past_years/2017_movies_data.csv')
data2018_df = pd.read_csv('data/movie_data_for_past_years/2018_movies_data.csv')
```


```python
#Create function to select relevant data columns
def yearData(df):
    return pd.DataFrame({"Title" : df['Title'],
                         "Year" : df['Year'],
                         "Genre" : df['Genre'],
                         "BoxOffice" : df['BoxOffice'],
                         "Actors" : df['Actors']})
```


```python
#Select data to analyze
data2014_df = yearData(data2014_df)
data2015_df = yearData(data2015_df)
data2016_df = yearData(data2016_df)
data2017_df = yearData(data2017_df)
data2018_df = yearData(data2018_df)
```


```python
#Merge data frames
mergeData = data2014_df.append(data2015_df).append(data2016_df).append(data2017_df).append(data2018_df)
```


```python
#Split actors list
acts = mergeData["Actors"].str.split(", ", n = 6, expand = True)

acts = acts.rename(columns = {0 : 'Actor 1',
                              1 : 'Actor 2',
                              2 : 'Actor 3',
                              3 : 'Actor 4'},)
acts = acts.fillna("")
```


```python
#Split genres list
subs = mergeData["Genre"].str.split(", ", n = 5, expand = True)

subs = subs.rename(columns = {0 : 'subgenre 1',
                              1 : 'subgenre 2',
                              2 : 'subgenre 3',
                              3 : 'subgenre 4',
                              4 : 'subgenre 5',
                              5 : 'subgenre 6'},)
subs = subs.fillna("None")

```


```python
#Add split actor columns for main data frame
mergeData['Actor 1'] = acts['Actor 1']
mergeData['Actor 2'] = acts['Actor 2']
mergeData['Actor 3'] = acts['Actor 3']
mergeData['Actor 4'] = acts['Actor 4']

```


```python
#Add split subgenre columns for main data frame (limiting to 3 subgenres only)
mergeData['subgenre 1'] = subs['subgenre 1']
mergeData['subgenre 2'] = subs['subgenre 2']
mergeData['subgenre 3'] = subs['subgenre 3']

```


```python
#Drop genre and actor parent columns
mergeData = mergeData.drop(axis=1, columns=['Genre', 'Actors'])

```


```python
#Limit range to six years
mergeData = mergeData.loc[(mergeData['Year'] == '2013') |
                          (mergeData['Year'] == '2014') |
                          (mergeData['Year'] == '2015') |
                          (mergeData['Year'] == '2016') |
                          (mergeData['Year'] == '2017') |
                          (mergeData['Year'] == '2018')]
```


```python
#Reformat boxOffice data to float
```


```python
mergeData['BoxOffice'] = mergeData['BoxOffice'].replace({'\$': '', ',': ''}, regex=True).astype(float)
```


```python
#Put all actors into a list
full_act_list = mergeData['Actor 1']
full_act_list = full_act_list.append(mergeData['Actor 2']).append(mergeData['Actor 3']).append(mergeData['Actor 4'])
```


```python
#Get list of 50 actors with most film roles during the date range
full_act_list = pd.DataFrame(full_act_list)
all_act_films = pd.DataFrame(full_act_list[0].value_counts())
all_act_films = all_act_films.drop(index='')
all_act_films = all_act_films.nlargest(50, 0)
all_act_films = all_act_films.rename(columns={0 : 'Film Count'})
all_act_films.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Film Count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Liam Neeson</th>
      <td>10</td>
    </tr>
    <tr>
      <th>Steve Carell</th>
      <td>9</td>
    </tr>
    <tr>
      <th>Mark Wahlberg</th>
      <td>9</td>
    </tr>
    <tr>
      <th>Cate Blanchett</th>
      <td>8</td>
    </tr>
    <tr>
      <th>Jason Clarke</th>
      <td>8</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Create function to search merge data for actors and return genre and box office data
def rad(actor):
    actor_data = pd.DataFrame(mergeData.loc[(mergeData['Actor 1'] == actor) |
                                            (mergeData['Actor 2'] == actor) | 
                                            (mergeData['Actor 3'] == actor) | 
                                            (mergeData['Actor 4'] == actor)])
    film_count = actor_data['Title'].count()
    sum_boxoffice = actor_data['BoxOffice'].sum()
    mean_boxoffice = actor_data['BoxOffice'].mean()
    #Create function to check for genre = None
    def is_none(df):
        for value in df:
            if value != 'None':
                next
            else:
                return True
                break
    #Count unique genres for actor
    genres = pd.DataFrame(list(actor_data['subgenre 1']) + list(actor_data['subgenre 2']) + list(actor_data['subgenre 3']), columns=['Genre'])
    uni_gens = pd.DataFrame(genres['Genre'].unique())[0]
    if is_none(genres['Genre']) == True:
        genre_count = uni_gens.count() - 1
    else:
        genre_count = uni_gens.count()

        
    gen_max = pd.DataFrame(genres['Genre'].value_counts())
    gen_max = gen_max.reset_index()
    if gen_max['index'][0] != "None":
        get_max = gen_max['index'][0]
    elif gen_max['index'][0] == "None":
            get_max = gen_max['index'][1]
    
    return pd.DataFrame({'Actor' : actor,
            'Film Count' : film_count, 
            'Genre Count' : genre_count,
            'Top Genre' : get_max,
            'Summed BoxOffice' : sum_boxoffice, 
            'Mean BoxOffice' : mean_boxoffice}, index = [1])
    
```


```python
#Create empty data frame to store actor data
actor_df = pd.DataFrame(columns=['Actor',
                                 'Film Count',
                                 'Genre Count',
                                 'Top Genre',
                                 'Summed BoxOffice',
                                 'Mean BoxOffice'])
```


```python
#Build actor data frame
act_list = all_act_films.reset_index()
act_list = list(act_list['index'])
for actor in act_list:
    results = rad(actor)
    actor_df = actor_df.append(results, ignore_index=True)
```


```python
#Change count data to float type
actor_df['Film Count'] = actor_df['Film Count'].astype(float)
actor_df['Genre Count'] = actor_df['Genre Count'].astype(float)
```


```python
#Create function to pull full list of genres only from actors being investigated
def rush(actor):
    actor_data = pd.DataFrame(mergeData.loc[(mergeData['Actor 1'] == actor) |
                                            (mergeData['Actor 2'] == actor) | 
                                            (mergeData['Actor 3'] == actor) | 
                                            (mergeData['Actor 4'] == actor)])

    #Count unique genres for actor
    genres = pd.DataFrame(list(actor_data['subgenre 1']) + list(actor_data['subgenre 2']) + list(actor_data['subgenre 3']), columns=['Genre'])
    uni_gens = pd.DataFrame(genres['Genre'].unique())[0]

    
    return list(uni_gens)

```


```python
#Create clean genre list for 50 actors being evaluated
sublist = []
for actor in act_list:
    results = rush(actor)
    sublist = sublist + results
    
sublist2 = pd.DataFrame(sublist)
sublist2 = pd.DataFrame(sublist2[0].unique())
sublist2 = sublist2.drop(index=10)
sublist2 = sublist2.rename(columns={0 : 'Genres'})
sublist2 = sublist2.sort_values('Genres')
genre_list = list(sublist2['Genres'])
genre_list = pd.DataFrame(genre_list)
genre_list = genre_list.rename(columns={0 : 'Genres'})
genre_list = genre_list.reindex()
```

# Film Genre Diversity by Actor

Here we look at 50 actors who performed in 5 or more films from 2013 to 2018 to evaluate diversity of roles based on film genre, which may be a measure of "type casting." The purpose of this analysis is to determine if the data reveals any differences in genre mobility among actors and to see if the data suggests that genre mobility is beneficial or neutral to boxoffice returns, or if the practice of type casting, or an actor chosing to "stay in their lane," results in better returns.   

Movie data from the years 2013 through 2018 were pulled from the Open Movie Database (OMDB) for use in this analysis. For each film in the data set, the first 3 genre keywords listed for each film were used in the assessment. Not all films had 3 genre keywords listed; however, if more than one keyword was present, they were weighted equally (e.g., the first genre keyword was not given priority over the second or third). There were 21 categories of genre keywords included in the 50-actor data set. The genre keywords were as follows:



```python
genre_list
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Genres</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Action</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Adventure</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Animation</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Biography</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Comedy</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Crime</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Documentary</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Drama</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Family</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Fantasy</td>
    </tr>
    <tr>
      <th>10</th>
      <td>History</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Horror</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Music</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Musical</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Mystery</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Romance</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Sci-Fi</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Sport</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Thriller</td>
    </tr>
    <tr>
      <th>19</th>
      <td>War</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Western</td>
    </tr>
  </tbody>
</table>
</div>



# Genre Frequency

For the 50 actors analyzed, the genres of drama, comedy, action, and adventure topped the list as most frequently sited (Figure 1), which was not surprising. Biography held the fifth place spot, which was an interesting finding.


```python
# Create a word cloud of the most commonly sited genres for the 50 actor data set
wordcloud_list = []
for actor in act_list:
    results = rush(actor)
    wordcloud_list = wordcloud_list + results
    
wordcloud_list2 = pd.DataFrame(wordcloud_list)
wordcloud_list2 = pd.DataFrame(wordcloud_list2.loc[wordcloud_list2[0] != 'None'])
word_list = wordcloud_list2[0]
word_list = list(word_list)
str1 = ' '.join(str(e) for e in word_list)
str1

text = str1

# Create the wordcloud object
wordcloud = WordCloud(width=5*72, 
                      height=5*72, 
                      margin=0, 
                      max_font_size=60, 
                      min_font_size=20, 
                      background_color="black", 
                      colormap="Blues").generate(text)
 
# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.title("Fig 1. Wordcloud of Genre Frequency")
plt.savefig("wordcloud.pdf")
plt.show()
```


![png](genre_mobility_analysis_files/genre_mobility_analysis_24_0.png)



```python
wordcloud_list2[0].value_counts()
```




    Drama          47
    Action         42
    Comedy         42
    Adventure      40
    Biography      33
    Crime          30
    Thriller       27
    Romance        24
    Sci-Fi         24
    Mystery        20
    Fantasy        17
    History        15
    Horror         14
    Animation      12
    Music           8
    Family          7
    War             6
    Sport           6
    Western         3
    Documentary     3
    Musical         2
    Name: 0, dtype: int64



# Genre Score

Genre mobility was assessed by determining the number of films each actor performed in during the analysis period and quantifying the unique genre keywords associated with those films. A higher genre count was associated with participation in more diverse film types, while a lower count was associated with a narrower range. A genre score was derived by subtracting the film count from the genre count and then normalizing the resulting value to the difference in genre/film count means. The resulting score was intended to quantify an individual actor's genre mobility compared to the group as a whole.


```python
#Create a genres score and add to data frame
mean_film_count = actor_df['Film Count'].mean()
mean_genre_count = actor_df['Genre Count'].mean()
actor_df['Genre Score'] = ((actor_df['Genre Count'] - actor_df['Film Count'])/(mean_genre_count - mean_film_count)).astype(float)
# Recast box office totals in thousands of dollars for ease of processing
actor_df['Summed BoxOffice'] = actor_df['Summed BoxOffice']/1000
actor_df['Mean BoxOffice'] = actor_df['Mean BoxOffice']/1000
actor_df = actor_df.rename(columns={'Summed BoxOffice' : 'BoxOffice Sum (K)', 
                                    'Mean BoxOffice' : 'Mean BoxOffice/Film (K)'})
actor_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Actor</th>
      <th>Film Count</th>
      <th>Genre Count</th>
      <th>Top Genre</th>
      <th>BoxOffice Sum (K)</th>
      <th>Mean BoxOffice/Film (K)</th>
      <th>Genre Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Liam Neeson</td>
      <td>10.0</td>
      <td>11.0</td>
      <td>Drama</td>
      <td>154221.811</td>
      <td>38555.452750</td>
      <td>0.485437</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Steve Carell</td>
      <td>9.0</td>
      <td>10.0</td>
      <td>Drama</td>
      <td>343656.270</td>
      <td>68731.254000</td>
      <td>0.485437</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mark Wahlberg</td>
      <td>9.0</td>
      <td>8.0</td>
      <td>Comedy</td>
      <td>542716.709</td>
      <td>90452.784833</td>
      <td>-0.485437</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Cate Blanchett</td>
      <td>8.0</td>
      <td>10.0</td>
      <td>Drama</td>
      <td>722701.565</td>
      <td>120450.260833</td>
      <td>0.970874</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Jason Clarke</td>
      <td>8.0</td>
      <td>10.0</td>
      <td>Drama</td>
      <td>329976.759</td>
      <td>82494.189750</td>
      <td>0.970874</td>
    </tr>
  </tbody>
</table>
</div>



# Distribution

First, we wanted to develop an understanding of the distribution. Our initial assumption was that more performances would correspond to higher genre counts, so we looked at the distribution of actors to performances and the distribution of genre keywords versus performance counts. In our sample, the majority of actors (44 out of 50) performed in 5 to 7 films during the study period with only 6 actors performing in 8 or more films (Figure 2). As expected, film genre diversity generally increased with the number of performances (Figure 3). A histagram of genre scores shows that genre mobility across the data set was generally normally distributed (Figure 4).


```python
#Calculate actor counts and mean genre keywords by film count
actor_count = pd.DataFrame(actor_df.groupby('Film Count')['Actor'].count())
actor_count['Avg Genre Tags'] = pd.DataFrame(actor_df.groupby('Film Count')['Genre Count'].mean())
actor_count
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Actor</th>
      <th>Avg Genre Tags</th>
    </tr>
    <tr>
      <th>Film Count</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>5.0</th>
      <td>9</td>
      <td>7.555556</td>
    </tr>
    <tr>
      <th>6.0</th>
      <td>23</td>
      <td>8.000000</td>
    </tr>
    <tr>
      <th>7.0</th>
      <td>12</td>
      <td>9.166667</td>
    </tr>
    <tr>
      <th>8.0</th>
      <td>3</td>
      <td>10.333333</td>
    </tr>
    <tr>
      <th>9.0</th>
      <td>2</td>
      <td>9.000000</td>
    </tr>
    <tr>
      <th>10.0</th>
      <td>1</td>
      <td>11.000000</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Plot Film Performance Frequency
plt.bar(actor_count.index.values, actor_count['Actor'])
plt.xlabel("Number of Performances (2013-2018)")
plt.ylabel("No. Actors")
plt.title("Fig 2. Film Performance Frequency")
plt.savefig("performance_frequency_bar.png")
plt.show()
```


![png](genre_mobility_analysis_files/genre_mobility_analysis_30_0.png)



```python
#Plot Genre Diversity vs. Performance Count
plt.bar(actor_count.index.values, actor_count['Avg Genre Tags'])
plt.xlabel("Number of Performances (2013-2018)")
plt.ylabel("Avg No. Genre Keywords")
plt.title("Fig 3. Genre Diversity vs. Performance Count")
plt.savefig("genre_div_vs_count-bar.png")
plt.show()
```


![png](genre_mobility_analysis_files/genre_mobility_analysis_31_0.png)



```python
# Plot Histogram of Genre Score Distribution
plt.hist(actor_df['Genre Score'], bins=7)
plt.ylabel("Number of Actors")
plt.xlabel("Genre Score")
plt.title("Fig 4. Histogram of Genre Score Distribution")
plt.savefig("histo_genre_score.png")
plt.show()
```


![png](genre_mobility_analysis_files/genre_mobility_analysis_32_0.png)


# Ranking by Genre Count and Score

Next, we looked at rankings of genre mobility for the top 10 and bottom 10 actors based on genre counts and genre scores. The top 10 actors by genre count had drama as their primary listed genre (Figure 5). The bottom 10 actors by genre count had adventure as their primary listed genre followed by action and comedy (Figure 6). When assessed by genre score, the top 10 actors had the same primary genre (drama) (Figure 7); whereas, the bottom 10 actors had comedy as the primary genre (Figure 8). These results suggest that actors known for dramatic roles have generally higher genre mobility and are more likely to be cast in diverse film types than actors known for comedies or action/adventure films.



```python
# Get top and bottom 10 actors by Genre Count
largeGen = pd.DataFrame(actor_df.nlargest(10, "Genre Count"))
smallGen = pd.DataFrame(actor_df.nsmallest(10, "Genre Count"))
```


```python
gen_count_df = largeGen.append(smallGen).sort_values('Genre Count', ascending=False)
```


```python
gen_count_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Actor</th>
      <th>Film Count</th>
      <th>Genre Count</th>
      <th>Top Genre</th>
      <th>BoxOffice Sum (K)</th>
      <th>Mean BoxOffice/Film (K)</th>
      <th>Genre Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>13</th>
      <td>Michael Fassbender</td>
      <td>7.0</td>
      <td>13.0</td>
      <td>Drama</td>
      <td>294840.756</td>
      <td>49140.126000</td>
      <td>2.912621</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Domhnall Gleeson</td>
      <td>8.0</td>
      <td>11.0</td>
      <td>Drama</td>
      <td>226305.089</td>
      <td>45261.017800</td>
      <td>1.456311</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Emily Blunt</td>
      <td>7.0</td>
      <td>11.0</td>
      <td>Adventure</td>
      <td>188643.327</td>
      <td>62881.109000</td>
      <td>1.941748</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Liam Neeson</td>
      <td>10.0</td>
      <td>11.0</td>
      <td>Drama</td>
      <td>154221.811</td>
      <td>38555.452750</td>
      <td>0.485437</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Steve Carell</td>
      <td>9.0</td>
      <td>10.0</td>
      <td>Drama</td>
      <td>343656.270</td>
      <td>68731.254000</td>
      <td>0.485437</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Cate Blanchett</td>
      <td>8.0</td>
      <td>10.0</td>
      <td>Drama</td>
      <td>722701.565</td>
      <td>120450.260833</td>
      <td>0.970874</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Jason Clarke</td>
      <td>8.0</td>
      <td>10.0</td>
      <td>Drama</td>
      <td>329976.759</td>
      <td>82494.189750</td>
      <td>0.970874</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Joel Edgerton</td>
      <td>7.0</td>
      <td>10.0</td>
      <td>Drama</td>
      <td>112832.566</td>
      <td>28208.141500</td>
      <td>1.456311</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Elle Fanning</td>
      <td>7.0</td>
      <td>10.0</td>
      <td>Drama</td>
      <td>223277.782</td>
      <td>55819.445500</td>
      <td>1.456311</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Ryan Reynolds</td>
      <td>7.0</td>
      <td>10.0</td>
      <td>Sci-Fi</td>
      <td>135510.718</td>
      <td>33877.679500</td>
      <td>1.456311</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Toni Collette</td>
      <td>7.0</td>
      <td>7.0</td>
      <td>Drama</td>
      <td>2895.704</td>
      <td>2895.704000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Anna Kendrick</td>
      <td>7.0</td>
      <td>7.0</td>
      <td>Comedy</td>
      <td>365340.509</td>
      <td>73068.101800</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Daniel Brühl</td>
      <td>6.0</td>
      <td>7.0</td>
      <td>Drama</td>
      <td>17426.964</td>
      <td>8713.482000</td>
      <td>0.485437</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Vin Diesel</td>
      <td>6.0</td>
      <td>6.0</td>
      <td>Action</td>
      <td>1247930.919</td>
      <td>249586.183800</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>38</th>
      <td>Melissa McCarthy</td>
      <td>6.0</td>
      <td>6.0</td>
      <td>Comedy</td>
      <td>174402.724</td>
      <td>58134.241333</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>41</th>
      <td>Kate Winslet</td>
      <td>5.0</td>
      <td>6.0</td>
      <td>Drama</td>
      <td>57456.602</td>
      <td>14364.150500</td>
      <td>0.485437</td>
    </tr>
    <tr>
      <th>46</th>
      <td>Mila Kunis</td>
      <td>5.0</td>
      <td>6.0</td>
      <td>Adventure</td>
      <td>115969.750</td>
      <td>38656.583333</td>
      <td>0.485437</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Kevin Hart</td>
      <td>7.0</td>
      <td>6.0</td>
      <td>Comedy</td>
      <td>616949.259</td>
      <td>154237.314750</td>
      <td>-0.485437</td>
    </tr>
    <tr>
      <th>43</th>
      <td>Seth Rogen</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>Comedy</td>
      <td>182683.878</td>
      <td>45670.969500</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Will Arnett</td>
      <td>6.0</td>
      <td>5.0</td>
      <td>Adventure</td>
      <td>612810.391</td>
      <td>153202.597750</td>
      <td>-0.485437</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Plot Relative Frequency of Primary Genre: Top 10 Actors by Genre Count
labels = largeGen['Top Genre'].unique()
plt.pie(largeGen['Top Genre'].value_counts(), labels=labels)
plt.title("Fig 5. Relative Frequency of Primary Genre: Top 10 Actors by Genre Count")
plt.savefig("top10_by_genre_count_pie.png")
plt.show()
```


![png](genre_mobility_analysis_files/genre_mobility_analysis_37_0.png)



```python
#Plot Relative Frequency of Primary Genre: Bottom 10 Actors by Genre Count
labelsS = smallGen['Top Genre'].unique()
plt.pie(smallGen['Top Genre'].value_counts(), labels=labelsS)
plt.title("Fig 6. Relative Frequency of Primary Genre: Bottom 10 Actors by Genre Count")
plt.savefig("low10_by_genre_count_pie.png")
plt.show()
```


![png](genre_mobility_analysis_files/genre_mobility_analysis_38_0.png)



```python
# Get top and bottom 10 actors by Genre Score
large = pd.DataFrame(actor_df.nlargest(10, 'Genre Score'))
small = pd.DataFrame(actor_df.nsmallest(10, 'Genre Score'))
gen_score_df = large.append(small).sort_values('Genre Score', ascending=False)
```


```python
gen_score_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Actor</th>
      <th>Film Count</th>
      <th>Genre Count</th>
      <th>Top Genre</th>
      <th>BoxOffice Sum (K)</th>
      <th>Mean BoxOffice/Film (K)</th>
      <th>Genre Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>13</th>
      <td>Michael Fassbender</td>
      <td>7.0</td>
      <td>13.0</td>
      <td>Drama</td>
      <td>294840.756</td>
      <td>49140.126000</td>
      <td>2.912621</td>
    </tr>
    <tr>
      <th>49</th>
      <td>Johnny Depp</td>
      <td>5.0</td>
      <td>10.0</td>
      <td>Adventure</td>
      <td>251185.622</td>
      <td>62796.405500</td>
      <td>2.427184</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Emily Blunt</td>
      <td>7.0</td>
      <td>11.0</td>
      <td>Adventure</td>
      <td>188643.327</td>
      <td>62881.109000</td>
      <td>1.941748</td>
    </tr>
    <tr>
      <th>29</th>
      <td>Alicia Vikander</td>
      <td>6.0</td>
      <td>10.0</td>
      <td>Drama</td>
      <td>74497.944</td>
      <td>18624.486000</td>
      <td>1.941748</td>
    </tr>
    <tr>
      <th>33</th>
      <td>Jon Hamm</td>
      <td>6.0</td>
      <td>10.0</td>
      <td>Drama</td>
      <td>385740.336</td>
      <td>192870.168000</td>
      <td>1.941748</td>
    </tr>
    <tr>
      <th>36</th>
      <td>Nicole Kidman</td>
      <td>6.0</td>
      <td>10.0</td>
      <td>Drama</td>
      <td>10542.504</td>
      <td>10542.504000</td>
      <td>1.941748</td>
    </tr>
    <tr>
      <th>37</th>
      <td>Chris Hemsworth</td>
      <td>6.0</td>
      <td>10.0</td>
      <td>Action</td>
      <td>1433803.148</td>
      <td>286760.629600</td>
      <td>1.941748</td>
    </tr>
    <tr>
      <th>45</th>
      <td>Olivia Cooke</td>
      <td>5.0</td>
      <td>9.0</td>
      <td>Sci-Fi</td>
      <td>43916.212</td>
      <td>21958.106000</td>
      <td>1.941748</td>
    </tr>
    <tr>
      <th>48</th>
      <td>Michelle Williams</td>
      <td>5.0</td>
      <td>9.0</td>
      <td>Drama</td>
      <td>186074.200</td>
      <td>62024.733333</td>
      <td>1.941748</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Domhnall Gleeson</td>
      <td>8.0</td>
      <td>11.0</td>
      <td>Drama</td>
      <td>226305.089</td>
      <td>45261.017800</td>
      <td>1.456311</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Liam Neeson</td>
      <td>10.0</td>
      <td>11.0</td>
      <td>Drama</td>
      <td>154221.811</td>
      <td>38555.452750</td>
      <td>0.485437</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Steve Carell</td>
      <td>9.0</td>
      <td>10.0</td>
      <td>Drama</td>
      <td>343656.270</td>
      <td>68731.254000</td>
      <td>0.485437</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Toni Collette</td>
      <td>7.0</td>
      <td>7.0</td>
      <td>Drama</td>
      <td>2895.704</td>
      <td>2895.704000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Anna Kendrick</td>
      <td>7.0</td>
      <td>7.0</td>
      <td>Comedy</td>
      <td>365340.509</td>
      <td>73068.101800</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Vin Diesel</td>
      <td>6.0</td>
      <td>6.0</td>
      <td>Action</td>
      <td>1247930.919</td>
      <td>249586.183800</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>38</th>
      <td>Melissa McCarthy</td>
      <td>6.0</td>
      <td>6.0</td>
      <td>Comedy</td>
      <td>174402.724</td>
      <td>58134.241333</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>43</th>
      <td>Seth Rogen</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>Comedy</td>
      <td>182683.878</td>
      <td>45670.969500</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Will Arnett</td>
      <td>6.0</td>
      <td>5.0</td>
      <td>Adventure</td>
      <td>612810.391</td>
      <td>153202.597750</td>
      <td>-0.485437</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Kevin Hart</td>
      <td>7.0</td>
      <td>6.0</td>
      <td>Comedy</td>
      <td>616949.259</td>
      <td>154237.314750</td>
      <td>-0.485437</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mark Wahlberg</td>
      <td>9.0</td>
      <td>8.0</td>
      <td>Comedy</td>
      <td>542716.709</td>
      <td>90452.784833</td>
      <td>-0.485437</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Plot Relative Frequency of Primary Genre: Top 10 Actors by Genre Score
labelsLg = large['Top Genre'].unique()
plt.pie(large['Top Genre'].value_counts(), labels=labelsLg)
plt.title("Fig 7. Relative Frequency of Primary Genre: Top 10 Actors by Genre Score")
plt.savefig("top10_by_genre_score_pie.png")
plt.show()
```


![png](genre_mobility_analysis_files/genre_mobility_analysis_41_0.png)



```python
#Plot Relative Frequency of Primary Genre: Bottom 10 Actors by Genre Score
labelsSm = small['Top Genre'].unique()
plt.pie(small['Top Genre'].value_counts(), labels=labelsSm)
plt.title("Fig 8. Relative Frequency of Primary Genre: Bottom 10 Actors by Genre Score")
plt.savefig("low10_by_genre_score_pie.png")
plt.show()
```


![png](genre_mobility_analysis_files/genre_mobility_analysis_42_0.png)


# Genre Mobility and Box Office

Next we looked at how genre mobility affected box office returns. To assess this, we compared the mean box office returns (per film) for the top and bottom 10 actors based on genre score. Average box office per film was statistically significantly greater (pvalue=0.000) for actors that were highly genre mobile as compared to those with low genre mobility.


```python
#Get mean and SE box office for top 10 actors by genre score
top10 = pd.DataFrame(gen_score_df['Mean BoxOffice/Film (K)'].nlargest(10))
top10_mean = top10['Mean BoxOffice/Film (K)'].mean()
top10_ste = top10['Mean BoxOffice/Film (K)'].std()/(top10['Mean BoxOffice/Film (K)'].count() -1)

```


```python
#Get mean and SE box office for bottom 10 actors by genre score
low10 = pd.DataFrame(gen_score_df['Mean BoxOffice/Film (K)'].nsmallest(10))
low10_mean = low10['Mean BoxOffice/Film (K)'].mean()
low10_ste = low10['Mean BoxOffice/Film (K)'].std()/(low10['Mean BoxOffice/Film (K)'].count() -1)

```


```python
#Put results in data frame
mean_gen_scr_df = pd.DataFrame([[top10_mean, top10_ste], [low10_mean, low10_ste]], 
                               index=['Top 10', 'Bottom 10'],columns=['Mean BoxOffice', "SE"])
mean_gen_scr_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Mean BoxOffice</th>
      <th>SE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Top 10</th>
      <td>139458.654903</td>
      <td>9120.358598</td>
    </tr>
    <tr>
      <th>Bottom 10</th>
      <td>35280.734072</td>
      <td>2272.151163</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Run statistical comparison between groups
t10 = list(top10['Mean BoxOffice/Film (K)'])
l10 = list(low10['Mean BoxOffice/Film (K)'])
```


```python
ttest_ind(t10, l10)
```




    Ttest_indResult(statistic=3.894445231332718, pvalue=0.0010624875121458491)




```python
#Plot mean Box Office for Most/Least Genre Mobile Actors
plt.bar(mean_gen_scr_df.index.values, mean_gen_scr_df['Mean BoxOffice'], yerr=mean_gen_scr_df['SE'], capsize=10)
plt.ylabel("Avg Box Office ($US in Thousands)")
plt.xlabel("Top and Bottom 10 Actors Based on Genre Score")
plt.title("Fig 9. Avg Box Office per Film: Most/Least Genre Mobile Actors")
plt.savefig("top_bot_boxoffice_bar.png")
plt.show()
```


![png](genre_mobility_analysis_files/genre_mobility_analysis_49_0.png)


# What's Up With Comedy?

From earlier assessments, it was clear that actors with predominantly comedic credit tended to be less genre mobile than those with primarily dramatic credits. Singling out these primarily comedic actors, we can see that higher average box office receipts for primarily comedic actors generally correspond to lower genre mobility scores and vice versa (Figure 10). This could be an indication that for comedic actors, it is more profitable to be genre static, or it could show that type casting is more of a problem with comedic actors than with dramatic actors.


```python
comedians = actor_df.loc[actor_df['Top Genre'] == 'Comedy']
comedians
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Actor</th>
      <th>Film Count</th>
      <th>Genre Count</th>
      <th>Top Genre</th>
      <th>BoxOffice Sum (K)</th>
      <th>Mean BoxOffice/Film (K)</th>
      <th>Genre Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2</th>
      <td>Mark Wahlberg</td>
      <td>9.0</td>
      <td>8.0</td>
      <td>Comedy</td>
      <td>542716.709</td>
      <td>90452.784833</td>
      <td>-0.485437</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Kevin Hart</td>
      <td>7.0</td>
      <td>6.0</td>
      <td>Comedy</td>
      <td>616949.259</td>
      <td>154237.314750</td>
      <td>-0.485437</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Anna Kendrick</td>
      <td>7.0</td>
      <td>7.0</td>
      <td>Comedy</td>
      <td>365340.509</td>
      <td>73068.101800</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Channing Tatum</td>
      <td>7.0</td>
      <td>10.0</td>
      <td>Comedy</td>
      <td>235469.948</td>
      <td>58867.487000</td>
      <td>1.456311</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Jason Bateman</td>
      <td>6.0</td>
      <td>7.0</td>
      <td>Comedy</td>
      <td>133268.161</td>
      <td>33317.040250</td>
      <td>0.485437</td>
    </tr>
    <tr>
      <th>31</th>
      <td>Tessa Thompson</td>
      <td>6.0</td>
      <td>7.0</td>
      <td>Comedy</td>
      <td>81345.235</td>
      <td>40672.617500</td>
      <td>0.485437</td>
    </tr>
    <tr>
      <th>34</th>
      <td>Ed Helms</td>
      <td>6.0</td>
      <td>9.0</td>
      <td>Comedy</td>
      <td>130961.638</td>
      <td>43653.879333</td>
      <td>1.456311</td>
    </tr>
    <tr>
      <th>38</th>
      <td>Melissa McCarthy</td>
      <td>6.0</td>
      <td>6.0</td>
      <td>Comedy</td>
      <td>174402.724</td>
      <td>58134.241333</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>43</th>
      <td>Seth Rogen</td>
      <td>5.0</td>
      <td>5.0</td>
      <td>Comedy</td>
      <td>182683.878</td>
      <td>45670.969500</td>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>
</div>




```python
comedy_score_abs = pd.DataFrame(comedians['Genre Score'].abs())
```


```python
ax1 = plt.subplot()
ax2 = ax1.twinx()
x = comedians['Actor']
y = comedians['Mean BoxOffice/Film (K)']
z = comedy_score_abs['Genre Score']

ax1.bar(x, y,width=0.4, color='b',align='edge')
ax2.bar(x, z,width=-0.4,color='g',align='edge')
ax1.set_xticklabels(labels=x, rotation=45, ha='right')
ax1.set_ylabel("Avg Box Office ($US in Thousands)")
ax2.set_ylabel("Genre Score")
ax1.set_xlabel("Comedic Actors")
ax1.set_title("Comedic Actors: Avg Box Office vs. Genre Score")
plt.savefig("comedic_actors.png")
plt.show()
```


![png](genre_mobility_analysis_files/genre_mobility_analysis_53_0.png)


# Conclusions

In conclusion, this analysis suggests that genre mobility is more prevalent among actors with primarily dramatic film roles as compared to those with primarily comedic roles. This could be the result of type casting or studio pressure to keep comedians in their lane, where they generate more profits, or it could be a result of comedians chosing to focus on these roles. Actors with the most genre diverse roles had statistically significantly increased mean box office returns compared to the least genre mobile actors, which also suggests that an actors box office draw (i.e., star power) plays a role in their ability to successfully move between genre types. Further investigation should include better means of quantifying genre mobility, longer timeframes, regression analysis to determine correlations, and incorporation of film ratings to determine if awards and acknowledgements affect genre mobility. Additionally, weighting the genre classifications and analyzing whether the actor had a leading or supporting role in the film could enhance the analysis.


```python

```
