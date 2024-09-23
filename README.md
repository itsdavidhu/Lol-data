# League of Legends Data and Statistical Analysis

*tl;dr*

- Players perform best in their 8th to 10th game.
- Shorter sessions are better than longer ones for high elo.
- When winstreaking in a session, your chances of winning are higher.
- When losestreaking in a session, your chances of winning are lower.
- Breaks after losses do not affect the next games win rate, but breaks after wins do, especially in high elo.

**Contributors**:   
David Hu  
Jose Pestana

## Data Gathering
- This analysis has been done on 310,000 games from 3,100 players.
- 100 players were randomly selected from each division, each having played at least 200 games in the corresponding split. The dataset comprises the last 100 games for each of these players.
- The average win rate in high elo is 53.4% and in general is 50.4%
- High elo data are games from Master, Grandmaster, and Challenger.
- All the data gathered comes from the Riot Games API, specifically the LEAGUE-V4, SUMMONER-V4, and MATCH-V5 endpoints.
- For our purposes, a session is defined as consecutive games played without a significant break of more than 30 minutes between them.
- Breaks are defined as periods of 30 minutes or more between games, but no longer than 8 hours.

## Session Length
Our analysis begins with determining the optimal session length. We had two methods for determining this:
1. Calculating the next games win rate given session length.
2. Calculating the total win rate of a session length.

![alt text](https://github.com/itsdavidhu/Lol-data/blob/main/images/next_general.png?raw=true)
![alt text](https://github.com/itsdavidhu/Lol-data/blob/main/images/total_general.png?raw=true)

- The first graph shows the average win rate of a game after X games played for all elos - this reflects a players individual performance in that specific game of a session.
- The graph tells us that players start their sessions relatively poorly, and ramp up to their peak performance from their 8th-10th games and taper off afterwards.
- The increasing then decreasing win rates can be attributed to players spending a few games to 'warm up' or getting accustomed to playing ranked, thus perform the best from their 8th-10th games, but lose focus or get fatigued and perform accordingly after.
- Interestingly, looking at the winrates for total session length, these tendancies are not reflected.
- No pattern exists when comparing session length to associated win rates, meaning that any session length will generally result in the same lp gains.
- This is important as the first graph shows player individual performance increasing throughout the session, but their overall win rate stays stagnant, as their relatively poor performance at the beginning of the session off sets their peak performance later, resulting in the same outcome.
- This conclusion is futher supported by the high elo graph of session win rates.
- The highest session win rates in high elo tend to be shorter ones as skilled players are able to fully focus and hone in on their first game.

![alt text](https://github.com/itsdavidhu/Lol-data/blob/main/images/total_high.png?raw=true)

Key Takeaway - play a normal game / go into practice tool to get accustomed. Then, play with the most intention and focus on either a short session or the first 1-3 games of a session to fully maximize lp gains


## Streaks

In this section, we attempt to identify the impact of win and loss streaks. More specifically, when a player should stop playing after X streak length.

![alt text](https://github.com/itsdavidhu/Lol-data/blob/main/images/streaks.png?raw=true)


## Breaks
In this analysis, we attempt to identify the impact of breaks on the following game. We do this by determining the win rates after wins vs losses. For the general playerbase, we have:

**Win rate after win given break: 50.6%**

**Win rate after loss given break: 50.0%**

To our surprise, tilt after losses does not seem to have an impact on the next games win rate. Remember, the average win rate in general elo is 50.4%. Taking a break after a win can improve your chances of winning, while taking a break after a loss can lower your chances of winning. This idea is further evident in high elo, where we have:

**Win rate after win given break in high elo: 54.0%**

**Win rate after loss given break in high elo: 52.7%**

Remember, the average win rate in high elo is 53.4%. Therefore, in both general and high Elo, taking a break after a win can increase your chances of winning, while taking a break after a loss can actually decrease your chances of winning.

Further research topics:
- Average KDA's after wins and losses - check for correlation with tilt

## Statistical Analysis

- The statistical analysis is focused on high elo (master - challenger) as patterns are more consistent

    * The model is made ASSUMING linearity between session lengths and the outcome of a game

Logistic Regression

- Logistic regression is focused on modeling the relationship between games in a session (independent variable) and the binary outcome of the game, win / loss (dependent variable).
- The odds ratio from the data given by the model is 0.97193106, suggesting a negative relationship between win rate and session length
- i.e. per session game increase in session length, the win rate is approximately 97.2% of the previous (2.8% drop) 
- Its important to note, the average win rate itself is not dropping 2.8% per subsequent game, but the probability of winning drops 2.8% 
- ex. if one session WR was 0.55, two session would be 0.5346 (0.55 * 0.972), and onwards.
    
    * CAVIEATS - the models accuracy is fairly low, meaning the relationship is not necessarily linear, thus a second model is used

Polynomial Regression

- Polynomial regression is focused on modeling the relationship between games in a session (independent variable) and average win rate for the session length (dependent variable).
- The data is split into a training and test set (70/30)
- The model has degree 5, it was chosen as it optimizes the RMSE for the data
- The R value is negative implying a negative relationship between session length and win rates
- The R^2 value is 0.6860271713705075 - meaning that the proportion of the variance in session length win rate can be directly attributed to session length itself
- The number is fairly high and is interesting to explore why the variance occurs, important factors like champion, player variance between games, player fatigue over longer sessions, etc, all play a role
    
![alt text](https://github.com/itsdavidhu/Lol-data/blob/main/images/polynomial_regression.png?raw=true)

Data can be found at: https://huggingface.co/datasets/itsdavidhu/LolData 
