// Berry layout test for KairoCal
import React from "react";
import { ConfigProvider } from "./contexts/ConfigContext";
import ThemeCustomization from "./themes";
import MainLayout from "./layout/MainLayout";

function App() {
  return (
    <ConfigProvider>
      <ThemeCustomization>
        <MainLayout />
      </ThemeCustomization>
    </ConfigProvider>
  );
}

export default App;
