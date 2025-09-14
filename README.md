# UbuntuTalks Site Crawler

Automated crawler audits for UbuntuTalks.com including performance monitoring, broken link detection, and image accessibility analysis.

## Features

### 🔍 Lighthouse Audits
- Performance monitoring
- SEO analysis  
- Accessibility compliance
- Best practices evaluation

### 🔗 Broken Link Detection
- Comprehensive link validation
- Multiple URL support
- Detailed reporting

### 🖼️ Image Analysis & Descriptions
- **Alt text analysis** - Detects missing or poor quality alt text
- **Accessibility compliance** - Scores images on accessibility standards
- **AI-powered descriptions** - Generates basic image descriptions
- **Detailed reporting** - Comprehensive analysis reports

## Image Analysis Features

The image analyzer crawls specified URLs and analyzes all images for:

- **Alt text presence** - Identifies images without alt attributes
- **Alt text quality** - Flags issues like:
  - Missing alt text
  - Too short/long descriptions
  - Generic text ("image", "picture")
  - Redundant prefixes ("image of", "picture of")
- **Basic AI descriptions** - Provides context-aware descriptions based on:
  - Filename analysis
  - Image type detection (logo, avatar, banner, icon)
  - File format identification
- **Accessibility scoring** - Rates each image 0-100 for accessibility
- **Recommendations** - Actionable suggestions for improvement

## Usage

### Manual Script Execution
```bash
# Install dependencies
pip install -r requirements.txt

# Analyze images on specific URLs
python image_analyzer.py https://ubuntutalks.com/ https://ubuntutalks.com/about-us

# View generated report
cat image_analysis_report.json
```

### GitHub Actions
The workflow automatically runs on manual trigger (`workflow_dispatch`) and includes:

1. **Lighthouse audits** for performance and accessibility
2. **Link checking** for broken links
3. **Image analysis** for alt text compliance

Results are saved as downloadable artifacts:
- `lighthouse-reports` - Performance metrics
- `lychee-report` - Broken link analysis  
- `image-analysis-report` - Image accessibility analysis

## Image Analysis Report Format

```json
{
  "summary": {
    "total_images": 25,
    "images_with_alt": 20,
    "images_without_alt": 5,
    "total_issues": 8,
    "average_accessibility_score": 82.5,
    "compliance_percentage": 80.0
  },
  "detailed_results": [
    {
      "image_data": {
        "url": "https://ubuntutalks.com/",
        "src": "https://ubuntutalks.com/logo.png",
        "alt": "UbuntuTalks logo",
        "title": "",
        "width": "200",
        "height": "50"
      },
      "alt_analysis": {
        "has_alt": true,
        "alt_text": "UbuntuTalks logo",
        "alt_length": 16,
        "issues": []
      },
      "ai_description": "Logo or branding image",
      "accessibility_score": 100,
      "recommendations": []
    }
  ]
}
```

## Compliance Standards

The image analyzer follows WCAG 2.1 guidelines:

- **Alt text requirements**: All images must have descriptive alt attributes
- **Length guidelines**: Alt text should be 3-125 characters
- **Quality standards**: Avoid generic terms and redundant prefixes
- **Compliance threshold**: 80% of images should have proper alt text

## Development

### Adding New Analysis Features

The `ImageAnalyzer` class can be extended with additional methods:

```python
def analyze_color_contrast(self, image_data):
    """Analyze color contrast for accessibility"""
    pass

def detect_text_in_images(self, image_url):
    """Detect text content in images"""
    pass
```

### Integrating AI Vision APIs

The `describe_image_url` method can be enhanced with services like:
- OpenAI Vision API
- Google Cloud Vision
- Azure Computer Vision
- AWS Rekognition

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all audits pass
5. Submit a pull request

## License

This project is part of the UbuntuTalks ecosystem and follows the same licensing terms.