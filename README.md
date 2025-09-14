# PWA Manifest Head for Ubuntu Talks

This repository now contains the necessary PWA (Progressive Web App) manifest and head elements for the Ubuntu Talks website.

## Files Added

### Core PWA Files
- `manifest.json` - Web app manifest with PWA configuration
- `index.html` - HTML template with complete PWA head section
- `sw.js` - Service worker for offline functionality
- `browserconfig.xml` - Microsoft tile configuration

### Required Assets (to be added)
- `icons/` - Directory for app icons (16x16 to 512x512)
- `screenshots/` - Directory for app store screenshots

## PWA Head Elements Included

### Essential PWA Meta Tags
```html
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#E95420">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### iOS Safari Support
```html
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Ubuntu Talks">
<link rel="apple-touch-icon" href="/icons/icon-152x152.png">
```

### Microsoft Tiles
```html
<meta name="msapplication-TileColor" content="#E95420">
<meta name="msapplication-TileImage" content="/icons/icon-144x144.png">
<meta name="msapplication-config" content="/browserconfig.xml">
```

### Social Media Integration
- Open Graph tags for Facebook/LinkedIn
- Twitter Card tags
- Proper meta descriptions and keywords

## Implementation

1. **Copy the manifest head section** from `index.html` to your website's HTML head
2. **Upload the manifest.json** to your website root
3. **Add the service worker** (sw.js) to your website root
4. **Generate and upload icons** in the required sizes (see manifest.json)
5. **Add browserconfig.xml** for Microsoft tile support

## Required Icon Sizes

The manifest references these icon sizes:
- 16x16, 32x32 (favicons)
- 72x72, 96x96, 128x128, 144x144, 152x152 (various device sizes)
- 192x192, 384x384, 512x512 (Android and PWA standards)

## Testing PWA Compliance

After implementation, test your PWA at:
- [PWABuilder](https://pwabuilder.com/reportcard?site=https://app.ubuntutalks.com)
- Chrome DevTools > Lighthouse > Progressive Web App audit
- Chrome DevTools > Application > Manifest

## Color Scheme

The PWA uses Ubuntu's official orange color (#E95420) as the theme color to maintain brand consistency.