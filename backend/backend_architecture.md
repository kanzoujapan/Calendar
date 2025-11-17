```mermaid
flowchart LR

%% ========================
%% Presentation Layer
%% ========================
subgraph L1["Presentation Layer"]
direction TB
FE[Frontend (React / Vite)]
end

%% ========================
%% Application Layer
%% ========================
subgraph L2["Application Layer"]
direction TB
FLASK[Flask App (__init__.py)]
CONFIG[Config (config.py)]
AUTHBP[Auth Blueprint (/api/auth)]
PLANBP[Plan Blueprint (/api/plan)]
FLASK --> CONFIG
FLASK --> AUTHBP
FLASK --> PLANBP
end

%% ========================
%% Domain / Service Layer
%% ========================
subgraph L3["Domain / Service Layer"]
direction TB
OAUTH[GoogleOAuth Service (services/google_oauth.py)]
TIMEUTIL[TimeUtil (utils/timeutil.py)]
end

%% ========================
%% Data Layer
%% ========================
subgraph L4["Data Layer"]
direction TB
SQLA[SQLAlchemy (db/__init__.py)]
TOKEN[GoogleToken Model (db/models.py)]
SQLA --> TOKEN
end

%% ========================
%% External Systems
%% ========================
subgraph L5["External Systems"]
direction TB
GOAUTH[Google OAuth2 API]
GCAL[Google Calendar API（将来拡張）]
DB[(Database: MySQL / PostgreSQL)]
end

%% ========================
%% Cross-Layer Flows
%% ========================
FE -->|HTTP Request| FLASK
AUTHBP --> OAUTH
PLANBP --> TIMEUTIL

OAUTH --> SQLA
SQLA --> DB

OAUTH --> GOAUTH
PLANBP -.-> GCAL
```