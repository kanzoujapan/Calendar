# Backend Project Structure


```mermaid
flowchart TD
  A[backend/] --> B[app/]
  B --> B1[__init__.py]
  B --> B2[config.py]
  B --> B3[blueprints/]
  B3 --> B3a[auth.py]
  B3 --> B3b[plan.py]
  B --> B4[services/]
  B4 --> B4a[google_oauth.py]
  B --> B5[utils/]
  B5 --> B5a[timeutil.py]
  A --> C[db/]
  C --> C1[models.py]
  A --> D[wsgi.py]
  A --> E[requirements.txt]
  ```