# Fix corrupted emojis in LandingPage.tsx
$filePath = "LandingPage.tsx"

# Read file with proper encoding
$content = Get-Content $filePath -Raw -Encoding UTF8

# Define replacements
$replacements = @{
    'ðŸ§ ' = '🧠'
    '¤' = '🎤' 
    '¡' = '⚡'
    'ï¿½ðŸ"„' = '🔄'
    'ðŸ"' = '📊'
    '📅' = '🗓️'
    '€¢' = '•'
}

# Apply all replacements
foreach ($old in $replacements.Keys) {
    $new = $replacements[$old]
    $content = $content -replace [regex]::Escape($old), $new
    Write-Host "Replacing '$old' with '$new'"
}

# Write back with UTF8 encoding
$content | Out-File $filePath -Encoding UTF8 -NoNewline
Write-Host "Emoji fixes completed!"
