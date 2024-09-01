# League of Legends Data and Statistical Analysis

tl;dr
- Longer sessions are better than shorter ones for the general playerbase, up until the 11th game onwards.
- Shorter sessions are better than longer ones for high elo.
- When winstreaking in a session, your chances of winning are higher.
- When losestreaking in a session, your chances of winning are lower.
- Breaks after losses do not affect the next games winrate, but breaks after wins do.

## Data Gathering
- This analysis has been done on 310,000 games from 3,100 players.
- 100 players were randomly selected from each division, each having played at least 200 games in the corresponding split. The dataset comprises the last 100 games for each of these players.
- All the data gathered comes from the Riot Games API, specifically the LEAGUE-V4, SUMMONER-V4, and MATCH-V5 endpoints.
- For our purposes, a session is defined as consecutive games played without a significant break of more than 30 minutes between them.
- Breaks are defined as periods of 30 minutes or more between games, but no longer than 8 hours.

![alt text](https://github.com/itsdavidhu/Lol-data/blob/main/images/total_general.png?raw=true)
![alt text](https://github.com/itsdavidhu/Lol-data/blob/main/images/streaks.png?raw=true)
![alt text](https://github.com/itsdavidhu/Lol-data/blob/main/images/next_general.png?raw=true)
![alt text](https://github.com/itsdavidhu/Lol-data/blob/main/images/total_high.png?raw=true)


## Statistical Analysis

 -The statistical analysis is focused on high elo (master - challenger) as patters are more consistent

    * The model is made ASSUMING linearity between session lengths and the out come of a game

    Logistic Regression

    - Logistic regression is focused on modelling the relationship between games in a session (independent varialbe) and the binary outcome of the game, win / loss (dependent variable).
    - The odds ratio from the data given by the model is 0.97193106, suggesting a negative relationship between win rate and session length
    - i.e. per session game increase in session length, the win rate is approximately 97.2% of the previous (2.8% drop) 
    - Its important to note, the average win rate itself is not dropping 2.8% per subsequent game, but the probability of winning drops 2.8% 
    - ex. if one session WR was 0.55, two session would be 0.5346 (0.55 * 0.972), and onwards.
    
    * CAVIEATS - the models accuracy is fairly low, meaning the relationship is not necessarily linear, thus a second model is used

    Polynomial Regression

    - Polynomial regression is focused on modelling the relationship between games in a session (independent variable) and average win rate for the session length (dependent variable).
    - The data is split into a training and test set (70/30)
    - The model has degree 5, it was chosen as it optimizes the RMSE for the data
    - The R value is negative implying a negative relationship between session length and win rates
    - The R^2 value is 0.6860271713705075 - meaning that the proportion of the variance in session length win rate can be directly attributed to session length itself
    - The number is fairly high and is interesting to explore why the variance occurs, important factors like champion, player variance between games, player fatigue over longer sessios etc, all play a role
    
    
![alt text](https://github.com/itsdavidhu/Lol-data/blob/main/images/polynomial_regression.png?raw=true)


Data can be found at: https://huggingface.co/datasets/itsdavidhu/LolData 
