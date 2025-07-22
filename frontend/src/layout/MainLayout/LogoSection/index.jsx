import { Link as RouterLink } from 'react-router-dom';

// material-ui
import Link from '@mui/material/Link';

// project imports
import { DASHBOARD_PATH } from 'config';
import Logo from 'ui-component/Logo';

// ==============================|| MAIN LOGO ||============================== //

export default function LogoSection({ expanded }) {
  return (
    <Link component={RouterLink} to={DASHBOARD_PATH} aria-label="theme-logo" sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', width: '100%' }}>
      <Logo expanded={expanded} />
    </Link>
  );
}
