Player data comes from http://stats.nba.com/js/data/ptsd/stats_ptsd.js

From the nba_api github, the format of the shot data is as follows:

            "GRID_TYPE", (Shot_Chart_Detail)
            "GAME_ID", 
            "GAME_EVENT_ID",
            "PLAYER_ID",
            "PLAYER_NAME",
            "TEAM_ID",
            "TEAM_NAME",
            "PERIOD",
            "MINUTES_REMAINING",
            "SECONDS_REMAINING",
            "EVENT_TYPE", ("Missed Shot" or "Made Shot")
            "ACTION_TYPE", (variety of shot, e.g. "Jump Shot")
            "SHOT_TYPE", ("3PT Field Goal" or "2PT Field Goal")
            "SHOT_ZONE_BASIC",
            "SHOT_ZONE_AREA",
            "SHOT_ZONE_RANGE",
            "SHOT_DISTANCE",
            "LOC_X", (hoop is at LOC_X = 0...units are in decifeet)
            "LOC_Y", (hoop is at LOC_Y = 0, which is 40 decifeet above baseline )
            "SHOT_ATTEMPTED_FLAG",
            "SHOT_MADE_FLAG",
            "GAME_DATE",
            "HTM", (Home team)
            "VTM" (Visiting team)