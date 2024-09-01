# League of Legends Data and Statistical Analysis

*tl;dr*
- Longer sessions are better than shorter ones for the general playerbase, up until the 11th game onwards.
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

![alt text](https://github.com/itsdavidhu/Lol-data/blob/main/images/total_high.png?raw=true)

## Streaks

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

Data can be found at: https://huggingface.co/datasets/itsdavidhu/LolData 
