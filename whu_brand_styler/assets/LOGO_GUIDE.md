# WHU Logo Assets - Usage Guide

## 📁 Logo Files Included

This assets folder contains official WHU Otto Beisheim School of Management logos ready for use in any content format.

### Available Logo Files

```
assets/
├── whu-logo-full.png (15 KB)        Primary logo with full text
├── whu-logo-icon.png (11 KB)        Symbol/icon only
├── logo_full_base64.txt             Base64 encoded (for HTML embedding)
└── logo_icon_base64.txt             Base64 encoded (for HTML embedding)
```

## 🎨 Logo Specifications

### Primary Logo (whu-logo-full.png)
- **Dimensions**: ~585 x 184 pixels
- **Format**: PNG with transparency
- **Size**: 15 KB
- **Colors**: WHU Blue (#2C4592) text with symbol
- **Use for**: Headers, title pages, primary branding

### Icon/Symbol (whu-logo-icon.png)
- **Dimensions**: ~200 x 200 pixels (square)
- **Format**: PNG with transparency
- **Size**: 11 KB
- **Colors**: Multi-color geometric pattern
- **Use for**: Small spaces, icons, favicons, app icons

## 📐 Logo Usage Guidelines

### Minimum Sizes
- **Digital**: 120px width minimum (full logo), 40px width minimum (icon)
- **Print**: 1 inch width minimum (full logo), 0.5 inch minimum (icon)

### Clear Space
Maintain clear space around logo equal to the height of the "W" in WHU
- **Minimum**: Logo height × 0.5 on all sides
- **Recommended**: Logo height × 1 on all sides

### Placement

#### Presentations
- **Title Slides**: Bottom right corner or top right
- **Content Slides**: Top right corner in white box
- **Size**: 1-1.5 inches width

#### Documents
- **Headers**: Top right corner
- **Footers**: Center or right-aligned
- **Size**: 0.75-1 inch width

#### Web/HTML
- **Navigation**: Top left (120-200px width)
- **Footer**: Center or left (80-120px width)
- **Favicon**: Use icon version, 32x32 or 64x64px

### Backgrounds
- **Light backgrounds**: Use standard logo (as provided)
- **Dark backgrounds**: Request white version if needed
- **Photographs**: Place logo in white box or clear area
- **Colored backgrounds**: Ensure contrast ratio meets accessibility standards

## 💻 How to Use Logos

### Option 1: Direct File Reference

#### In HTML
```html
<img src="assets/whu-logo-full.png" alt="WHU Otto Beisheim School of Management" style="width: 200px;">
```

#### In React/JSX
```jsx
<img 
  src="/path/to/assets/whu-logo-full.png" 
  alt="WHU Otto Beisheim School of Management"
  style={{ width: '200px', height: 'auto' }}
/>
```

#### In Python (docx)
```python
from docx import Document
from docx.shared import Inches

doc = Document()
doc.add_picture('assets/whu-logo-full.png', width=Inches(1.5))
```

#### In Python (pptx)
```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[0])

# Add logo
left = Inches(8.5)
top = Inches(0.2)
width = Inches(1.3)
slide.shapes.add_picture('assets/whu-logo-full.png', left, top, width=width)
```

### Option 2: Base64 Embedding (No External Files)

#### Read Base64 Data
```python
# Read the base64 encoded logo
with open('assets/logo_full_base64.txt', 'r') as f:
    logo_base64 = f.read()
```

#### In HTML
```html
<img src="data:image/png;base64,PASTE_BASE64_HERE" alt="WHU Logo">
```

#### In React/JSX
```jsx
const logoBase64 = "PASTE_BASE64_HERE";

<img 
  src={`data:image/png;base64,${logoBase64}`}
  alt="WHU Otto Beisheim School of Management"
  style={{ width: '200px' }}
/>
```

#### In Markdown
```markdown
![WHU Logo](data:image/png;base64,PASTE_BASE64_HERE)
```

### Option 3: CSS Background

```css
.whu-logo {
  width: 200px;
  height: 63px;
  background: url('assets/whu-logo-full.png') no-repeat center;
  background-size: contain;
}
```

## 📋 Logo Usage Examples

### Example 1: HTML Navigation Bar

```html
<header style="background: #2C4592; padding: 20px; display: flex; align-items: center;">
  <img 
    src="assets/whu-logo-full.png" 
    alt="WHU Otto Beisheim School of Management"
    style="height: 40px; filter: brightness(0) invert(1);"
  />
  <nav style="margin-left: auto;">
    <a href="#" style="color: white; margin-left: 20px;">Programs</a>
    <a href="#" style="color: white; margin-left: 20px;">Research</a>
  </nav>
</header>
```

### Example 2: Document Header (Python)

```python
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Add header with logo
section = doc.sections[0]
header = section.header

# Add logo to header
paragraph = header.paragraphs[0]
run = paragraph.add_run()
run.add_picture('assets/whu-logo-full.png', width=Inches(1.2))
paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
```

### Example 3: Presentation Title Slide (Python)

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[0])

# Add logo to bottom right
left = Inches(8)
top = Inches(6.5)
width = Inches(1.5)
slide.shapes.add_picture('assets/whu-logo-full.png', left, top, width=width)

prs.save('presentation.pptx')
```

### Example 4: React Component with Logo

```jsx
import React from 'react';

const WHUHeader = () => {
  return (
    <header style={{
      background: '#2C4592',
      padding: '20px 40px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between'
    }}>
      <img 
        src="assets/whu-logo-full.png"
        alt="WHU Otto Beisheim School of Management"
        style={{ 
          height: '50px',
          filter: 'brightness(0) invert(1)' // Make white on blue
        }}
      />
      <nav>
        <a href="#programs" style={{ color: 'white', marginLeft: '30px' }}>Programs</a>
        <a href="#research" style={{ color: 'white', marginLeft: '30px' }}>Research</a>
        <a href="#about" style={{ color: 'white', marginLeft: '30px' }}>About</a>
      </nav>
    </header>
  );
};

export default WHUHeader;
```

### Example 5: Email Signature HTML

```html
<table style="font-family: Arial, sans-serif; font-size: 14px;">
  <tr>
    <td style="padding-right: 20px;">
      <img src="assets/whu-logo-full.png" alt="WHU" style="width: 150px;">
    </td>
    <td>
      <strong style="color: #2C4592;">Your Name</strong><br>
      Title / Department<br>
      WHU – Otto Beisheim School of Management<br>
      <a href="mailto:email@whu.edu" style="color: #E7331A;">email@whu.edu</a>
    </td>
  </tr>
</table>
```

## 🎨 Logo Color Variations

### For Light Backgrounds
Use the provided logo as-is (default blue)

### For Dark Backgrounds (CSS Filter)
```css
/* Convert logo to white */
.logo-white {
  filter: brightness(0) invert(1);
}
```

### For Blue Backgrounds (WHU Blue)
Place logo in white box:
```html
<div style="background: white; padding: 10px; display: inline-block; border-radius: 4px;">
  <img src="assets/whu-logo-full.png" alt="WHU" style="height: 40px;">
</div>
```

## ⚠️ Logo Don'ts

❌ **Don't** stretch or distort the logo (maintain aspect ratio)  
❌ **Don't** change logo colors (use as provided)  
❌ **Don't** add effects (shadows, gradients, outlines)  
❌ **Don't** rotate the logo  
❌ **Don't** place on busy backgrounds without clear space  
❌ **Don't** use low-resolution versions (pixelated)  
❌ **Don't** recreate or modify the logo elements  

## ✅ Logo Best Practices

✅ **Do** maintain aspect ratio (width/height proportional)  
✅ **Do** provide adequate clear space  
✅ **Do** use high-contrast backgrounds  
✅ **Do** include alt text for accessibility  
✅ **Do** use appropriate size for medium (print vs digital)  
✅ **Do** test logo visibility on various backgrounds  
✅ **Do** use vector format when available (SVG)  

## 🔧 Technical Implementation

### Responsive Logo (CSS)

```css
.whu-logo {
  max-width: 200px;
  height: auto;
  width: 100%;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .whu-logo {
    max-width: 150px;
  }
}

@media (max-width: 480px) {
  .whu-logo {
    max-width: 120px;
  }
}
```

### Lazy Loading (HTML)

```html
<img 
  src="assets/whu-logo-full.png"
  alt="WHU Otto Beisheim School of Management"
  loading="lazy"
  width="200"
  height="63"
/>
```

### Retina Display Support

```html
<img 
  src="assets/whu-logo-full.png"
  srcset="assets/whu-logo-full.png 1x,
          assets/whu-logo-full@2x.png 2x"
  alt="WHU Logo"
/>
```

## 📊 Logo File Information

### whu-logo-full.png
- **Type**: Raster image (PNG)
- **Transparency**: Yes (alpha channel)
- **Color mode**: RGB
- **Dimensions**: 585 × 184 pixels
- **Aspect ratio**: ~3.18:1
- **File size**: 15 KB
- **DPI**: 96 (standard screen resolution)

### whu-logo-icon.png
- **Type**: Raster image (PNG)
- **Transparency**: Yes (alpha channel)
- **Color mode**: RGB
- **Dimensions**: ~200 × 200 pixels (square)
- **Aspect ratio**: 1:1
- **File size**: 11 KB
- **DPI**: 96 (standard screen resolution)

## 🔗 Quick Reference

### File Paths
```bash
# Full logo
assets/whu-logo-full.png

# Icon only
assets/whu-logo-icon.png

# Base64 versions
assets/logo_full_base64.txt
assets/logo_icon_base64.txt
```

### Standard Sizes
```
Large:    200-300px width (hero sections, main headers)
Medium:   120-200px width (navigation, page headers)
Small:    80-120px width (footers, small spaces)
Icon:     40-64px width (favicons, app icons)
```

### Alt Text
Always use descriptive alt text:
```html
alt="WHU Otto Beisheim School of Management"
alt="WHU Logo"
alt="WHU"
```

## 📞 Need Help?

- Check the main SKILL.md for branding workflows
- Review whu-brand-library.md for complete guidelines
- See implementation-examples.md for code samples

---

**Remember**: The logo is a key brand element. Use it consistently and with proper clear space for maximum impact! 🎨
