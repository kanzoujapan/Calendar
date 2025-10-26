# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(["dist"]),
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: [
          "./tsconfig.node.json",
          "./tsconfig.app.json",
        ],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
]);
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from "eslint-plugin-react-x";
import reactDom from "eslint-plugin-react-dom";

export default defineConfig([
  globalIgnores(["dist"]),
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs["recommended-typescript"],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: [
          "./tsconfig.node.json",
          "./tsconfig.app.json",
        ],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
]);
```

## 現状

google calendar API との通信の実装中
実際にgoogle 認可画面が表示された
次は
google calendar にアクセスできるようにするまで
tokenとかの話を解決

## データベース

- google calendar events db

   | 列名             | 型              | 制約・デフォルト値                                     | 説明 |
|------------------|-----------------|--------------------------------------------------------|------|
| user_id          | VARCHAR(255)    | NOT NULL                                               | ユーザーID（主キーの一部） |
| google_event_id  | VARCHAR(255)    | NOT NULL                                               | GoogleイベントID（主キーの一部） |
| event_date       | DATE            | NOT NULL                                               | 検索用の基準日（JSTで丸めて格納） |
| title            | VARCHAR(255)    | NOT NULL                                               | イベントのタイトル（原則 summary） |
| description      | TEXT            | NULL                                                   | イベント説明（空でも可） |
| raw_json         | JSON            | NULL                                                   | 追加情報（JSON形式で格納） |
| updated_at       | DATETIME        | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  | 最終更新時刻 |
| **PRIMARY KEY**  | (user_id, google_event_id) |                                                    | 複合主キー |
| **INDEX**        | idx_user_date (user_id, event_date) |                                        | user_id と event_date の複合インデックス |
