-- Players Table
CREATE TABLE Players (
    PlayerID INT AUTO_INCREMENT PRIMARY KEY,
    PlayerName VARCHAR(255) NOT NULL
);

-- Teams Table
CREATE TABLE Teams (
    TeamID INT AUTO_INCREMENT PRIMARY KEY,
    TeamName VARCHAR(255) NOT NULL
);

INSERT INTO Teams (TeamName) VALUES 
('BC Allschwil'),
('BC Bären Kleinbasel'),
('BC Winterthur'),
('Bernex Basket'),
('Centre National du Basket Suisse'),
('GC Zürich Wildcats'),
('Goldcoast Wallabies'),
('Groupe E Académie Fribourg U23'),
('Lions de Genève U23 pwd by Grand-Saconnex'),
('Morges-Saint-Prex Red Devils'),
('Swiss Central Basketball'),
('Union Lavaux Riviera Basket'),
('Vevey Riviera Basket U23'),
('Villars Basket');


-- PlayerTeamAffiliation Table
CREATE TABLE PlayerTeamAffiliation (
    AffiliationID INT AUTO_INCREMENT PRIMARY KEY,
    PlayerID INT,
    TeamID INT,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID),
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID)
);

-- Matches Table
CREATE TABLE Matches (
    MatchID INT AUTO_INCREMENT PRIMARY KEY,
    MatchDate DATE,
    Team1ID INT,
    Team2ID INT,
    FOREIGN KEY (Team1ID) REFERENCES Teams(TeamID),
    FOREIGN KEY (Team2ID) REFERENCES Teams(TeamID)
);

-- PlayerMatchStatistics Table
CREATE TABLE PlayerMatchStatistics (
    StatID INT AUTO_INCREMENT PRIMARY KEY,
    MatchID INT,
    PlayerID INT,
    MinutesPlayed INT,
    TwoPointsMade INT,
    TwoPointsAttempt INT,
    TwoPointsPercentage FLOAT,
    ThreePointsMade INT,
    ThreePointsAttempt INT,
    ThreePointsPercentage FLOAT,
    FreeThrowMade INT,
    FreeThrowAttempt INT,
    FreeThrowPercentage FLOAT,
    OffensiveRebound INT,
    DefensiveRebound INT,
    TotalRebound INT,
    Assists INT,
    Turnovers INT,
    Steals INT,
    Blocks INT,
    Fouls INT,
    FoulsOn INT,
    Efficency INT,
    TotalPoints INT,
    -- Other player-specific match stats can be added here
    FOREIGN KEY (MatchID) REFERENCES Matches(MatchID),
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID)
);

-- TeamMatchStatistics Table
CREATE TABLE TeamMatchStatistics (
    StatID INT AUTO_INCREMENT PRIMARY KEY,
    MatchID INT,
    TeamID INT,
    MinutesPlayed INT,
    TwoPointsMade INT,
    TwoPointsAttempt INT,
    TwoPointsPercentage FLOAT,
    ThreePointsMade INT,
    ThreePointsAttempt INT,
    ThreePointsPercentage FLOAT,
    FreeThrowMade INT,
    FreeThrowAttempt INT,
    FreeThrowPercentage FLOAT,
    OffensiveRebound INT,
    DefensiveRebound INT,
    TotalRebound INT,
    Assists INT,
    Turnovers INT,
    Steals INT,
    Blocks INT,
    Fouls INT,
    FoulsOn INT,
    Efficency INT,
    TotalPoints INT,
    -- Other team-specific match stats can be added here
    FOREIGN KEY (MatchID) REFERENCES Matches(MatchID),
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID)
);

CREATE TABLE ProcessedGameDays (
    GameDay DATE PRIMARY KEY
);
