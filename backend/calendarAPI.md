```mermaid
sequenceDiagram
    autonumber
    participant U as ユーザー（ブラウザ）
    participant F as フロントエンド
    participant B as Flaskバックエンド
    participant G as Google OAuthサーバー

    %% --- 認証開始 ---
    U->>F: ① GET /api/auth HTTP/1.1<br>Host: localhost:5173
    F->>B: ② GET /api/auth HTTP/1.1<br>Host: localhost:3000<br>（Proxy転送）
    B-->>F: ③ HTTP/1.1 302 Found<br>Location: https://accounts.google.com/o/oauth2/v2/auth?client_id=...&redirect_uri=http://127.0.0.1:3000/oauth2callback&scope=...&response_type=code
    F-->>U: ③' HTTP/1.1 302 Found<br>Location: https://accounts.google.com/o/oauth2/v2/auth?...

    %% --- Googleログイン画面へ遷移 ---
    U->>G: ④ GET /o/oauth2/v2/auth?... HTTP/1.1<br>Host: accounts.google.com
    G-->>U: ⑤ HTTP/1.1 200 OK<br>Content-Type: text/html<br>（Googleログイン・同意画面）

    %% --- 同意送信 ---
    U-->>G: ⑥ POST /signin/v2/challenge/... HTTP/1.1<br>Cookie: ...<br>Body: consent=allow
    G-->>U: ⑦ HTTP/1.1 302 Found<br>Location: http://127.0.0.1:3000/oauth2callback?code=abcd1234&state=xyz

    %% --- 認可コード受取 ---
    U->>B: ⑧ GET /oauth2callback?code=abcd1234&state=xyz HTTP/1.1<br>Host: localhost:3000
    B->>G: ⑨ POST /token HTTP/1.1<br>Host: oauth2.googleapis.com<br>Content-Type: application/x-www-form-urlencoded<br>Body: code=abcd1234&client_id=...&client_secret=...&redirect_uri=...&grant_type=authorization_code
    G-->>B: ⑩ HTTP/1.1 200 OK<br>Content-Type: application/json<br>{"access_token": "...", "refresh_token": "...", "expires_in": 3600}

    %% --- 認証後のリダイレクト ---
    B-->>U: ⑪ HTTP/1.1 302 Found<br>Location: http://localhost:5173/post-auth
    U->>F: ⑫ GET /post-auth HTTP/1.1<br>Host: localhost:5173
    F-->>U: ⑬ HTTP/1.1 200 OK<br>Content-Type: text/html<br>（完了画面を表示）
    
