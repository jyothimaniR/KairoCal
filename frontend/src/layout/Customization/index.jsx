import { useState } from 'react';
import { useTheme } from '@mui/material/styles';
import Divider from '@mui/material/Divider';
import Drawer from '@mui/material/Drawer';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';

// REMOVE: import PerfectScrollbar from 'react-perfect-scrollbar';
// REPLACE WITH: Simple Box with overflow

import FontFamily from './FontFamily';
import BorderRadius from './BorderRadius';
import AnimateButton from 'ui-component/extended/AnimateButton';
import { IconSettings } from '@tabler/icons-react';

export default function Customization() {
  const theme = useTheme();
  const [open, setOpen] = useState(false);
  
  const handleToggle = () => {
    setOpen(!open);
  };

  return (
    <Drawer 
      anchor="right" 
      onClose={handleToggle} 
      open={open} 
      slotProps={{ paper: { sx: { width: 280 } } }}
    >
      {/* Replace PerfectScrollbar with Box */}
      <Box sx={{ 
        height: '100%', 
        overflowY: 'auto',
        padding: 2
      }}>
        <Grid container spacing={2}>
          <Grid size={12}>
            <FontFamily />
            <Divider />
          </Grid>
          <Grid size={12}>
            <BorderRadius />
            <Divider />
          </Grid>
        </Grid>
      </Box>
    </Drawer>
  );
}