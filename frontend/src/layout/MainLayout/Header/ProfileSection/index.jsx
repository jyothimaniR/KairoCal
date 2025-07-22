import { useState, useRef } from 'react';
import { useTheme } from '@mui/material/styles';
import Avatar from '@mui/material/Avatar';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import IconButton from '@mui/material/IconButton';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import User1 from 'assets/images/users/user-round.svg';
import { userMenuItems } from 'config/userMenu';

export default function ProfileSection() {
  const theme = useTheme();
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  const handleClick = (event) => setAnchorEl(event.currentTarget);
  const handleClose = () => setAnchorEl(null);

  // Demo user info
  const user = { name: 'Jyothi', email: 'jyothi@email.com' };

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', ml: 2 }}>
      <Avatar src={User1} alt={user.name} sx={{ width: 40, height: 40, mr: 1 }} />
      <Box sx={{ textAlign: 'right', mr: 1 }}>
        <Typography variant="subtitle1" sx={{ fontWeight: 600, lineHeight: 1 }}>
          Hi, {user.name}
        </Typography>
        <Typography variant="caption" color="text.secondary" sx={{ lineHeight: 1 }}>
          {user.email}
        </Typography>
      </Box>
      <IconButton onClick={handleClick} size="small" sx={{ ml: 0.5 }}>
        <ArrowDropDownIcon />
      </IconButton>
      <Menu anchorEl={anchorEl} open={open} onClose={handleClose} onClick={handleClose} transformOrigin={{ horizontal: 'right', vertical: 'top' }} anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}>
        {userMenuItems.map((item) => (
          <MenuItem key={item.label} onClick={() => {/* handle action here */}}>{item.label}</MenuItem>
        ))}
      </Menu>
    </Box>
  );
}
