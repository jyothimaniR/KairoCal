import { memo } from 'react';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import { NavLink } from 'react-router-dom';
import menuItems from 'config/menuItems';

function MenuList({ expanded }) {
  return (
    <List>
      {menuItems.map((item) => (
        <ListItemButton
          key={item.title}
          component={NavLink}
          to={item.path}
          sx={{
            '&.active': {
              bgcolor: 'action.selected',
              color: 'primary.main',
              fontWeight: 'bold',
            },
            justifyContent: expanded ? 'flex-start' : 'center',
            px: expanded ? 2 : 1,
          }}
        >
          <ListItemIcon sx={{ minWidth: expanded ? 40 : 0, justifyContent: 'center' }}>{item.icon && <item.icon />}</ListItemIcon>
          {expanded && <ListItemText primary={item.title} />}
        </ListItemButton>
      ))}
    </List>
  );
}

export default memo(MenuList);
