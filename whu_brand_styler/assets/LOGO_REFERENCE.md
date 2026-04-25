# WHU Logo Assets - Visual Reference

## 🎨 Logo Preview

This document provides a visual reference for the WHU logos included in this skill package.

---

## Primary Logo (Full)

**File**: `whu-logo-full.png`

### Description
- Full WHU logo with "Otto Beisheim School of Management" text
- Official blue color (#2C4592)
- Geometric symbol on the right
- Dimensions: 585 × 184 pixels
- File size: 15 KB

### Visual Preview
![WHU Full Logo](whu-logo-full.png)

### Usage
- **Primary branding**: Use for main headers, title pages
- **Minimum width**: 120px (digital), 1 inch (print)
- **Backgrounds**: Best on light backgrounds (white, light gray)
- **Dark backgrounds**: Apply white filter (CSS: `filter: brightness(0) invert(1)`)

### Code Examples

**HTML:**
```html
<img src="assets/whu-logo-full.png" 
     alt="WHU Otto Beisheim School of Management" 
     style="height: 50px;">
```

**React:**
```jsx
<img 
  src="assets/whu-logo-full.png"
  alt="WHU Otto Beisheim School of Management"
  style={{ height: '50px', width: 'auto' }}
/>
```

**Python (docx):**
```python
from docx.shared import Inches
doc.add_picture('assets/whu-logo-full.png', width=Inches(1.5))
```

---

## Symbol/Icon Only

**File**: `whu-logo-icon.png`

### Description
- WHU geometric symbol without text
- Multi-color design (blue, green, white)
- Square format for icons
- Dimensions: 200 × 200 pixels
- File size: 11 KB

### Visual Preview
![WHU Icon](whu-logo-icon.png)

### Usage
- **Small spaces**: Favicons, app icons, social media avatars
- **Square format**: Perfect for profile pictures, badges
- **Minimum size**: 40px width
- **Versatile**: Works on various backgrounds

### Code Examples

**HTML Favicon:**
```html
<link rel="icon" type="image/png" href="assets/whu-logo-icon.png">
```

**React:**
```jsx
<img 
  src="assets/whu-logo-icon.png"
  alt="WHU"
  style={{ width: '64px', height: '64px' }}
/>
```

**CSS:**
```css
.whu-icon {
  width: 64px;
  height: 64px;
  background: url('assets/whu-logo-icon.png') no-repeat center;
  background-size: contain;
}
```

---

## Logo Specifications Comparison

| Aspect | Full Logo | Icon Only |
|--------|-----------|-----------|
| **File** | whu-logo-full.png | whu-logo-icon.png |
| **Size** | 15 KB | 11 KB |
| **Dimensions** | 585 × 184 px | 200 × 200 px |
| **Aspect Ratio** | ~3.18:1 | 1:1 (square) |
| **Format** | PNG with transparency | PNG with transparency |
| **Min Width** | 120px (digital) | 40px (digital) |
| **Best For** | Headers, banners, primary branding | Icons, favicons, small spaces |
| **Colors** | WHU Blue (#2C4592) | Multi-color pattern |

---

## Usage Scenarios

### Scenario 1: Website Header (Full Logo)
```jsx
<header style={{ 
  background: '#2C4592', 
  padding: '20px 40px',
  display: 'flex',
  alignItems: 'center'
}}>
  <img 
    src="assets/whu-logo-full.png"
    alt="WHU"
    style={{ 
      height: '50px',
      filter: 'brightness(0) invert(1)' // White on blue
    }}
  />
</header>
```

### Scenario 2: Document Header (Full Logo)
```python
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
section = doc.sections[0]
header = section.header

# Add logo to header (right-aligned)
paragraph = header.paragraphs[0]
run = paragraph.add_run()
run.add_picture('assets/whu-logo-full.png', width=Inches(1.2))
paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
```

### Scenario 3: Favicon (Icon)
```html
<!-- In your HTML <head> -->
<link rel="icon" type="image/png" sizes="32x32" href="assets/whu-logo-icon.png">
<link rel="apple-touch-icon" sizes="180x180" href="assets/whu-logo-icon.png">
```

### Scenario 4: Presentation Slide (Full Logo)
```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[0])

# Add logo to top right corner
left = Inches(8.5)
top = Inches(0.2)
width = Inches(1.3)
slide.shapes.add_picture('assets/whu-logo-full.png', left, top, width=width)
```

---

## Base64 Embedding

For situations where you can't reference external files, use the base64-encoded versions:

### Full Logo Base64
**File**: `logo_full_base64.txt`
- 19,728 characters of base64 data
- Embeddable directly in HTML/CSS

**Usage:**
```html
<img src="data:image/png;base64,[PASTE_CONTENT_FROM_FILE]" alt="WHU Logo">
```

### Icon Base64
**File**: `logo_icon_base64.txt`
- 14,456 characters of base64 data
- Embeddable directly in HTML/CSS

**Usage:**
```html
<img src="data:image/png;base64,[PASTE_CONTENT_FROM_FILE]" alt="WHU Icon">
```

---

## Logo Clear Space

Always maintain clear space around the logo:

```
Minimum Clear Space = Logo Height × 0.5
Recommended Clear Space = Logo Height × 1.0
```

### Example:
If logo height is 50px:
- Minimum clear space: 25px on all sides
- Recommended clear space: 50px on all sides

```css
.whu-logo-container {
  padding: 50px; /* Clear space */
  display: inline-block;
}
```

---

## Color Adaptation

### On Light Backgrounds
Use logo as-is (default blue)

### On Dark Backgrounds
Apply white filter:
```css
.logo-on-dark {
  filter: brightness(0) invert(1);
}
```

### On Blue Background (#2C4592)
Place in white container:
```css
.logo-container {
  background: white;
  padding: 10px;
  border-radius: 4px;
  display: inline-block;
}
```

---

## Accessibility

Always include descriptive alt text:

### Full Logo
```html
alt="WHU Otto Beisheim School of Management"
alt="WHU Otto Beisheim School of Management Logo"
```

### Icon
```html
alt="WHU"
alt="WHU Icon"
alt="WHU Logo"
```

---

## File Locations

All logo assets are in the `assets/` folder:

```
assets/
├── whu-logo-full.png         (Primary logo with text)
├── whu-logo-icon.png          (Symbol/icon only)
├── logo_full_base64.txt       (Base64 encoded full logo)
├── logo_icon_base64.txt       (Base64 encoded icon)
└── LOGO_GUIDE.md              (This file)
```

---

## Quick Tips

✅ **Do:**
- Maintain aspect ratio
- Use adequate clear space
- Include alt text
- Test on different backgrounds
- Use appropriate size for context

❌ **Don't:**
- Stretch or distort
- Change colors
- Add effects (shadows, gradients)
- Rotate or flip
- Use on busy backgrounds without clear space

---

## Need More Help?

For complete logo usage guidelines, see:
- **LOGO_GUIDE.md** - Comprehensive usage guide
- **SKILL.md** - Main skill documentation
- **whu-brand-library.md** - Complete brand specifications

---

**Remember**: The logo is your primary brand identifier. Use it consistently and professionally! 🎨
