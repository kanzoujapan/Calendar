

## 現状

google calendar API との通信の実装中
実際にgoogle 認可画面が表示された
次は
google calendar にアクセスできるようにするまで
tokenとかの話を解決

## データベース

- google calendar events db


| Column             | Type              | Constraints                                     | Description |
|------------------|-----------------|--------------------------------------------------------|------|
| user_id          | VARCHAR(64)    | NOT NULL                                               | ユーザーID（主キーの一部） |
| google_event_id  | VARCHAR(64)    | NOT NULL                                               | GoogleイベントID（主キーの一部） |
| event_date       | DATE            | NOT NULL                                               | 検索用の基準日（JSTで丸めて格納） |
| title            | VARCHAR(255)    | NOT NULL                                               | イベントのタイトル（原則 summary） |
| description      | TEXT            | NULL                                                   | イベント説明（空でも可） |
| raw_json         | JSON            | NULL                                                   | 追加情報（JSON形式で格納） |
| updated_at       | DATETIME        | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  | 最終更新時刻 |
| **PRIMARY KEY**  | (user_id, google_event_id) |                                             | 複合主キー |
| **INDEX**        | idx_user_date (user_id, event_date) |                                    | user_id と event_date の複合インデックス |



| Column       | Type        | Constraints                                | Description                             |
|--------------|-------------|---------------------------------------------|-----------------------------------------|
| user_id      | VARCHAR(64) | PRIMARY KEY, NOT NULL                       | 内部ユーザーID (UUIDなど)               |
| google_sub   | VARCHAR(64) | UNIQUE, NOT NULL                            | Googleの不変ID (OpenID Connect sub)     |
| refresh_token| TEXT        | NULL許容                                    | リフレッシュトークン                    |
| expires_at   | DATETIME    | NOT NULL                                    | access_token失効日時 (UTC)              |
| updated_at   | DATETIME    | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード最終更新時刻            |
