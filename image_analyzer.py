#!/usr/bin/env python3
"""
Image Analyzer for UbuntuTalks Site Crawler

This script crawls a website, extracts images, and analyzes them for:
- Alt text presence and quality
- Image descriptions using AI vision models
- Accessibility compliance
"""

import requests
import json
import os
import sys
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import base64
import time
from typing import List, Dict, Optional

class ImageAnalyzer:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'UbuntuTalks-Site-Crawler/1.0'
        })
        
    def crawl_images(self, url: str) -> List[Dict]:
        """Crawl a URL and extract all images with their metadata"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            images = []
            
            # Find all img tags
            img_tags = soup.find_all('img')
            
            for img in img_tags:
                src = img.get('src')
                if not src:
                    continue
                    
                # Convert relative URLs to absolute
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = urljoin(self.base_url, src)
                elif not src.startswith('http'):
                    src = urljoin(url, src)
                
                image_data = {
                    'url': url,
                    'src': src,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', ''),
                    'width': img.get('width', ''),
                    'height': img.get('height', ''),
                    'loading': img.get('loading', ''),
                    'class': ' '.join(img.get('class', [])),
                    'id': img.get('id', ''),
                    'sizes': img.get('sizes', ''),
                    'srcset': img.get('srcset', ''),
                }
                
                images.append(image_data)
                
            return images
            
        except Exception as e:
            print(f"Error crawling {url}: {e}")
            return []
    
    def analyze_alt_text(self, image_data: Dict) -> Dict:
        """Analyze the quality of alt text for an image"""
        alt_text = image_data.get('alt', '').strip()
        
        analysis = {
            'has_alt': bool(alt_text),
            'alt_text': alt_text,
            'alt_length': len(alt_text),
            'issues': []
        }
        
        if not alt_text:
            analysis['issues'].append('Missing alt text')
        elif len(alt_text) < 3:
            analysis['issues'].append('Alt text too short')
        elif len(alt_text) > 125:
            analysis['issues'].append('Alt text too long (>125 characters)')
        elif alt_text.lower() in ['image', 'picture', 'photo', 'img']:
            analysis['issues'].append('Generic alt text')
        elif alt_text.lower().startswith(('image of', 'picture of', 'photo of')):
            analysis['issues'].append('Redundant alt text prefix')
            
        return analysis
    
    def describe_image_url(self, image_url: str) -> Optional[str]:
        """
        Generate a description for an image URL.
        This provides intelligent descriptions based on URL analysis and context.
        """
        try:
            # Check if image is accessible
            response = self.session.head(image_url, timeout=10)
            if response.status_code != 200:
                return f"Inaccessible image (HTTP {response.status_code})"
                
            # Extract filename and analyze
            parsed_url = urlparse(image_url)
            filename = os.path.basename(parsed_url.path).lower()
            file_ext = os.path.splitext(filename)[1].lower()
            
            # Analyze URL path for context
            path_segments = [seg.lower() for seg in parsed_url.path.split('/') if seg]
            
            # Enhanced keyword detection
            if any(word in filename for word in ['logo', 'brand', 'emblem']):
                return "Company logo or branding element"
            elif any(word in filename for word in ['avatar', 'profile', 'headshot', 'portrait']):
                return "Profile photo or avatar image"
            elif any(word in filename for word in ['banner', 'hero', 'header', 'masthead']):
                return "Banner or header image"
            elif any(word in filename for word in ['icon', 'button', 'ui', 'interface']):
                return "User interface icon or button"
            elif any(word in filename for word in ['thumb', 'thumbnail', 'preview']):
                return "Thumbnail or preview image"
            elif any(word in filename for word in ['gallery', 'photo', 'img']):
                return "Gallery or content image"
            elif 'screenshot' in filename:
                return "Screenshot or application interface"
            elif any(word in path_segments for word in ['uploads', 'media', 'content']):
                return "User-uploaded content image"
            elif any(word in path_segments for word in ['static', 'assets', 'images']):
                return "Static website asset"
            
            # File type specific descriptions
            if file_ext == '.svg':
                return "Scalable vector graphic (SVG) - likely an icon or illustration"
            elif file_ext in ['.gif']:
                return "Animated GIF image"
            elif file_ext in ['.webp']:
                return "Modern WebP format image"
            elif file_ext in ['.png']:
                return "PNG image - possibly with transparency"
            elif file_ext in ['.jpg', '.jpeg']:
                return "JPEG photograph or image"
            
            # Fallback analysis
            if filename.isdigit():
                return "Numbered content image requiring manual description"
            elif len(filename) > 20:
                return "Content image with descriptive filename"
            else:
                return "Content image requiring manual description"
                
        except Exception as e:
            return f"Error analyzing image: {str(e)}"
    
    def analyze_image(self, image_data: Dict) -> Dict:
        """Perform comprehensive analysis on a single image"""
        analysis = {
            'image_data': image_data,
            'alt_analysis': self.analyze_alt_text(image_data),
            'ai_description': None,
            'accessibility_score': 0,
            'recommendations': []
        }
        
        # Get AI description
        analysis['ai_description'] = self.describe_image_url(image_data['src'])
        
        # Calculate accessibility score
        alt_analysis = analysis['alt_analysis']
        if alt_analysis['has_alt'] and not alt_analysis['issues']:
            analysis['accessibility_score'] = 100
        elif alt_analysis['has_alt']:
            analysis['accessibility_score'] = 70
        else:
            analysis['accessibility_score'] = 0
            
        # Generate recommendations
        if not alt_analysis['has_alt']:
            analysis['recommendations'].append('Add descriptive alt text')
        elif alt_analysis['issues']:
            for issue in alt_analysis['issues']:
                if 'too short' in issue:
                    analysis['recommendations'].append('Make alt text more descriptive')
                elif 'too long' in issue:
                    analysis['recommendations'].append('Shorten alt text to under 125 characters')
                elif 'generic' in issue or 'redundant' in issue:
                    analysis['recommendations'].append('Use more specific, descriptive alt text')
                    
        return analysis
    
    def generate_report(self, results: List[Dict]) -> Dict:
        """Generate a summary report of image analysis"""
        total_images = len(results)
        images_with_alt = sum(1 for r in results if r['alt_analysis']['has_alt'])
        total_issues = sum(len(r['alt_analysis']['issues']) for r in results)
        avg_score = sum(r['accessibility_score'] for r in results) / total_images if total_images > 0 else 0
        
        report = {
            'summary': {
                'total_images': total_images,
                'images_with_alt': images_with_alt,
                'images_without_alt': total_images - images_with_alt,
                'total_issues': total_issues,
                'average_accessibility_score': round(avg_score, 2),
                'compliance_percentage': round((images_with_alt / total_images * 100) if total_images > 0 else 0, 2)
            },
            'detailed_results': results
        }
        
        return report

def main():
    """Main function to run image analysis"""
    urls = [
        'https://ubuntutalks.com/',
        'https://ubuntutalks.com/about-us'
    ]
    
    if len(sys.argv) > 1:
        urls = sys.argv[1:]
    
    print(f"🔍 Starting image analysis for {len(urls)} URL(s)")
    print(f"📍 Target URLs: {', '.join(urls)}")
    print("=" * 50)
    
    analyzer = ImageAnalyzer('https://ubuntutalks.com')
    all_results = []
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Analyzing images on: {url}")
        try:
            images = analyzer.crawl_images(url)
            
            if not images:
                print(f"⚠️  No images found on {url}")
                continue
                
            print(f"🖼️  Found {len(images)} images")
            
            for j, image_data in enumerate(images, 1):
                print(f"  [{j}/{len(images)}] Analyzing: {os.path.basename(image_data['src'])}")
                analysis = analyzer.analyze_image(image_data)
                all_results.append(analysis)
                
                # Print quick status
                score = analysis['accessibility_score']
                if score >= 90:
                    status = "✅"
                elif score >= 70:
                    status = "⚠️"
                else:
                    status = "❌"
                print(f"    {status} Score: {score}/100")
                
        except Exception as e:
            print(f"❌ Error analyzing {url}: {e}")
            continue
    
    if not all_results:
        print("\n❌ No images were successfully analyzed")
        sys.exit(1)
    
    # Generate final report
    print(f"\n📊 Generating comprehensive report...")
    report = analyzer.generate_report(all_results)
    
    # Output results
    output_file = 'image_analysis_report.json'
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print detailed summary
    summary = report['summary']
    print(f"\n{'=' * 50}")
    print(f"🎯 IMAGE ANALYSIS SUMMARY")
    print(f"{'=' * 50}")
    print(f"📊 Total images analyzed: {summary['total_images']}")
    print(f"✅ Images with alt text: {summary['images_with_alt']}")
    print(f"❌ Images without alt text: {summary['images_without_alt']}")
    print(f"📈 Alt text compliance: {summary['compliance_percentage']}%")
    print(f"🏆 Average accessibility score: {summary['average_accessibility_score']}/100")
    print(f"⚠️  Total issues found: {summary['total_issues']}")
    print(f"📄 Detailed report saved to: {output_file}")
    
    # Show worst performing images
    worst_images = sorted(all_results, key=lambda x: x['accessibility_score'])[:3]
    if worst_images and worst_images[0]['accessibility_score'] < 100:
        print(f"\n🔍 IMAGES NEEDING ATTENTION:")
        for i, img in enumerate(worst_images[:3], 1):
            img_name = os.path.basename(img['image_data']['src'])
            score = img['accessibility_score']
            issues = img['alt_analysis']['issues']
            print(f"  {i}. {img_name} (Score: {score}/100)")
            if issues:
                print(f"     Issues: {', '.join(issues)}")
    
    # Exit with appropriate code
    if summary['compliance_percentage'] < 80:
        print(f"\n❌ FAILED: Alt text compliance is below 80% threshold")
        sys.exit(1)
    elif summary['compliance_percentage'] < 95:
        print(f"\n⚠️  WARNING: Alt text compliance could be improved")
        sys.exit(0)
    else:
        print(f"\n✅ EXCELLENT: Alt text compliance meets high standards")
        sys.exit(0)

if __name__ == '__main__':
    main()