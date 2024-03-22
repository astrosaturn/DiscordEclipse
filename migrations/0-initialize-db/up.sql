USE eclipsedatabase;

CREATE TABLE actions
(
    casenum         INT             NOT NULL PRIMARY KEY,
    user_id         BIGINT          NOT NULL,
    guild_id        BIGINT          NOT NULL,
    action_type     VARCHAR(255)    NOT NULL,
    reason          VARCHAR(255)            ,
    moderator       BIGINT          NOT NULL,
    username        VARCHAR(255)    NOT NULL
);

CREATE TABLE guilds
(
    guild_id        BIGINT          NOT NULL PRIMARY KEY,
    log_chan_id     BIGINT,
    scrape_chan_id  BIGINT,
    scraper_wh_id   BIGINT
);

CREATE TABLE users
(
    user_id         BIGINT         NOT NULL PRIMARY KEY,
    current_xp      INT,
    user_level      INT,
    credits         BIGINT,
    daily_cooldown  BIGINT,
    theft_cooldown  BIGINT,
    bank            BIGINT,
    cases           INT
);