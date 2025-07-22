import { useState } from 'react';

// material-ui
import { useTheme } from '@mui/material/styles';
import Divider from '@mui/material/Divider';
import Drawer from '@mui/material/Drawer';
import Grid from '@mui/material/Grid';

// third party
import PerfectScrollbar from 'react-perfect-scrollbar';

// project imports
import FontFamily from './FontFamily';
import BorderRadius from './BorderRadius';

import AnimateButton from 'ui-component/extended/AnimateButton';

// assets
import { IconSettings } from '@tabler/icons-react';
// ==============================|| LIVE CUSTOMIZATION ||============================== //

export default function Customization() {
  const theme = useTheme();

  // drawer on/off
  const [open, setOpen] = useState(false);
  const handleToggle = () => {
    setOpen(!open);
  };

  return (
    <Drawer anchor="right" onClose={handleToggle} open={open} slotProps={{ paper: { sx: { width: 280 } } }}>
      <PerfectScrollbar>
        <Grid container spacing={2}>
          <Grid size={12}>
            {/* font family */}
            <FontFamily />
            <Divider />
          </Grid>
          <Grid size={12}>
            {/* border radius */}
            <BorderRadius />
            <Divider />
          </Grid>
        </Grid>
      </PerfectScrollbar>
    </Drawer>
  );
}
