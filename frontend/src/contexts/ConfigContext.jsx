import { createContext, useState } from 'react';

export const ConfigContext = createContext({
  borderRadius: 12,
  fontFamily: `'Roboto', sans-serif`,
  outlinedFilled: true,
  navType: 'light',
  mode: 'light',
  presetColor: 'default',
  onChangeMode: () => {},
  onChangePresetColor: () => {},
  onChangeFontFamily: () => {},
  onChangeBorderRadius: () => {},
  onChangeOutlinedFilled: () => {}
});

// ==============================|| CONFIG CONTEXT PROVIDER ||============================== //

export const ConfigProvider = ({ children }) => {
  const [mode, setMode] = useState('light');
  const [presetColor, setPresetColor] = useState('default');
  const [fontFamily, setFontFamily] = useState(`'Roboto', sans-serif`);
  const [borderRadius, setBorderRadius] = useState(12);
  const [outlinedFilled, setOutlinedFilled] = useState(true);
  const [navType, setNavType] = useState('light');

  const onChangeMode = (mode) => {
    setMode(mode);
  };

  const onChangePresetColor = (presetColor) => {
    setPresetColor(presetColor);
  };

  const onChangeFontFamily = (fontFamily) => {
    setFontFamily(fontFamily);
  };

  const onChangeBorderRadius = (borderRadius) => {
    setBorderRadius(borderRadius);
  };

  const onChangeOutlinedFilled = (outlinedFilled) => {
    setOutlinedFilled(outlinedFilled);
  };

  const value = {
    mode,
    presetColor,
    fontFamily,
    borderRadius,
    outlinedFilled,
    navType,
    onChangeMode,
    onChangePresetColor,
    onChangeFontFamily,
    onChangeBorderRadius,
    onChangeOutlinedFilled
  };

  return <ConfigContext.Provider value={value}>{children}</ConfigContext.Provider>;
};
