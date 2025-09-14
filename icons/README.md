# Icon Files Required

This directory should contain the following icon files for full PWA support:

## Standard Icons
- `icon-16x16.png` - Browser favicon
- `icon-32x32.png` - Browser favicon  
- `icon-72x72.png` - Small Android icon
- `icon-96x96.png` - Android icon
- `icon-128x128.png` - Chrome Web Store icon
- `icon-144x144.png` - Microsoft tile icon
- `icon-152x152.png` - iOS icon
- `icon-192x192.png` - Android home screen icon
- `icon-384x384.png` - Android splash screen
- `icon-512x512.png` - PWA standard large icon

## Icon Requirements
- All icons should be square (1:1 aspect ratio)
- Use PNG format for best compatibility
- Should feature the Ubuntu Talks logo/branding
- Background should be transparent or match the app's background color
- Icons should be "maskable" - safe area in center 80% of the icon

## Generation Tools
You can generate these icons from a single high-resolution source using:
- [PWA Asset Generator](https://github.com/onderceylan/pwa-asset-generator)
- [RealFaviconGenerator](https://realfavicongenerator.net/)
- [PWABuilder](https://www.pwabuilder.com/)

## Command Example
```bash
npx pwa-asset-generator source-icon.png ./icons --manifest ./manifest.json
```