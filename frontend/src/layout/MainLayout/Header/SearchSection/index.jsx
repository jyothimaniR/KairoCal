import { useState, useEffect, useRef } from 'react';
import Box from '@mui/material/Box';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import MicIcon from '@mui/icons-material/Mic';

const placeholders = [
  "What's on your mind?",
  'Add a new event with your voice or text…',
  'Try: Meeting at 4pm tomorrow at campus'
];

export default function SearchSection() {
  const [placeholderIndex, setPlaceholderIndex] = useState(0);
  const [inputValue, setInputValue] = useState('');
  const intervalRef = useRef();

  useEffect(() => {
    intervalRef.current = setInterval(() => {
      setPlaceholderIndex((prev) => (prev + 1) % placeholders.length);
    }, 3000);
    return () => clearInterval(intervalRef.current);
  }, []);

  return (
    <Box sx={{ width: { md: 350, lg: 434 }, ml: 2 }}>
      <OutlinedInput
        fullWidth
        value={inputValue}
        onChange={e => setInputValue(e.target.value)}
        placeholder={placeholders[placeholderIndex]}
        sx={{
          bgcolor: 'background.paper',
          borderRadius: 2,
          transition: 'box-shadow 0.2s',
          boxShadow: 1,
          fontSize: 16,
          '::placeholder': {
            opacity: 0.7,
            fontStyle: 'italic',
            transition: 'opacity 0.5s',
          },
        }}
        endAdornment={
          <InputAdornment position="end">
            <IconButton edge="end" aria-label="voice input">
              <MicIcon />
            </IconButton>
          </InputAdornment>
        }
      />
    </Box>
  );
}
