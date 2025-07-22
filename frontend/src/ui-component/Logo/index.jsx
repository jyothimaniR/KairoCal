// material-ui
import { useTheme } from '@mui/material/styles';
import logoImg from 'assets/images/kairocal-logo.png';

export default function Logo({ expanded }) {
  return (
    <img
      src={logoImg}
      alt="KairoCal Logo"
      style={{
        width: expanded ? 72 : 48,
        height: expanded ? 72 : 48,
        objectFit: 'contain',
        display: 'block',
        margin: '0 auto',
        padding: expanded ? 12 : 4,
        transition: 'all 0.2s',
      }}
    />
  );
}
