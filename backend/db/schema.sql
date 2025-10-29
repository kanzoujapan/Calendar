CREATE TABLE IF NOT EXISTS google_tokens (
  user_id       VARCHAR(64) PRIMARY KEY,      -- 自前の内部ユーザーID (例: UUID or app生成)
  google_sub    VARCHAR(64) UNIQUE NOT NULL,  -- Googleの不変ID (sub)
  refresh_token TEXT,
  expires_at    DATETIME NOT NULL,
  updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP
                           ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS google_calendar_events (
  user_id         VARCHAR(64) NOT NULL,
  google_event_id VARCHAR(128) NOT NULL,
  event_date      DATE NOT NULL,
  title           VARCHAR(255) NOT NULL,
  description     TEXT NULL,
  raw_json        JSON NULL,
  updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
                             ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, google_event_id),
  INDEX idx_user_date (user_id, event_date),
  CONSTRAINT fk_events_user
    FOREIGN KEY (user_id) REFERENCES google_tokens(user_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;