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

Data can be found at: https://huggingface.co/datasets/itsdavidhu/LolData 
