// アプリ全体のルートコンポーネント
import CheckTheDay from "./pages/CheckTheDay";



export default function App() {
  return <CheckTheDay />;
}

// import { BrowserRouter, Routes, Route } from "react-router-dom";
// import CheckTheDay from "./pages/CheckTheDay";
// import Settings from "./pages/Settings";

// export default function App() {
//   return (
//     <BrowserRouter>
//       <Routes>
//         <Route path="/" element={<CheckTheDay />} />
//         <Route path="/settings" element={<Settings />} />
//       </Routes>
//     </BrowserRouter>
//   );
// }