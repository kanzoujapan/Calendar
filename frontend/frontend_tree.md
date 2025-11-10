# Frontend Project Structure

```mermaid
flowchart TD
  A[frontend/] --> B[src/]
  B --> B1[main.tsx]
  B --> B2[App.tsx]
  B --> B3[components/]
  B3 --> B3a[Header.tsx]
  B3 --> B3b[MessageList.tsx]
  B3 --> B3c[DatePickerForm.tsx]
  B3 --> B3d[StatusBar.tsx]
  B3 --> B3e[AuthSection.tsx]
  B3 --> B3f[ErrorBanner.tsx]
  B --> B4[hooks/]
  B4 --> B4a[useAuth.ts]
  B4 --> B4b[useCalendar.ts]
  B --> B6[styles/]
  B6 --> B6a[index.css]
  B --> B7[types/]
  B7 --> B7a[message.ts]
  ```