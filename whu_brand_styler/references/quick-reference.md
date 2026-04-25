# WHU Brand Styler - Quick Reference Cheatsheet

## 🎨 Color Palette

```
PRIMARY
WHU Blue:    #2C4592  rgb(44, 69, 146)    [Headers, Titles, Accents]
White:       #FFFFFF  rgb(255, 255, 255)  [Backgrounds, Light text]
Black:       #000000  rgb(0, 0, 0)        [Body text]

SECONDARY
Light Blue:  #808FBE  rgb(128, 143, 190)  [Secondary accents]
Dark Gray:   #515256  rgb(81, 82, 86)     [Secondary text]
Light Gray:  #C7C1BF  rgb(199, 193, 191)  [Borders, dividers]
VL Gray:     #EEEBEA  rgb(238, 235, 234)  [Subtle backgrounds]

ACCENT
WHU Red:     #E7331A  rgb(231, 51, 26)    [Links, Callouts]
```

## ✍️ Typography

```
FONT FAMILY
Primary:     Arial, Helvetica, sans-serif
Weights:     Bold (headings), Regular (body)

SIZE SCALE
Title:       36-44pt / 36px / 2.25rem
H1:          28-32pt / 28px / 1.75rem
H2:          24pt    / 24px / 1.5rem
H3:          20pt    / 20px / 1.25rem
Body:        11-12pt / 16px / 1rem
Small:       9-10pt  / 14px / 0.875rem

LINE HEIGHT
Headings:    1.2
Body:        1.5
Captions:    1.4
```

## 📐 Spacing

```
SECTIONS
Padding:     60-80px vertical, 20px horizontal

ELEMENTS
Cards:       20-30px padding
Margins:     20px between elements
Paragraphs:  16px spacing

DOCUMENT MARGINS
All sides:   1 inch (2.5cm)
```

## 🔘 Bullet Points

```
Level 1:     § (Section symbol) in WHU Blue (#2C4592)
Level 2:     ○ (Circle) in Light Blue (#808FBE)
Level 3:     – (En dash) in Dark Gray (#515256)

Indent:      0.25-0.5 inches
Hanging:     0.25 inches
```

## 🖼️ Layout Patterns

### HTML Navigation
```
Background:  #2C4592 (WHU Blue)
Height:      60-70px
Logo:        40px height, left-aligned
Links:       16px Arial, White
Hover:       #808FBE (Light Blue)
```

### Document Header
```
Height:      0.75 inches
Font:        12pt Arial, Dark Gray
Logo:        Top right, 0.75-1 inch width
Border:      Optional 1px Light Gray (#C7C1BF)
```

### Presentation Header Bar
```
Background:  #2C4592 (WHU Blue) full-width
Height:      ~1 inch
Title:       28-32pt Arial Bold, White
Logo:        White box, top right corner
```

### Content Cards
```
Background:  White
Border:      1px solid #C7C1BF
Radius:      4-8px
Shadow:      0 2px 4px rgba(0,0,0,0.1)
Padding:     20-30px
```

## 🔲 Buttons

### Primary Button
```
Background:  #2C4592 (WHU Blue)
Text:        White, Arial Bold, 16px
Padding:     12px 24px
Radius:      4px
Hover:       #808FBE (Light Blue)
```

### Secondary Button
```
Background:  White
Border:      2px solid #2C4592
Text:        #2C4592, Arial Bold, 16px
Hover:       Background #808FBE, Border #808FBE
```

## 📏 Logo Guidelines

```
PLACEMENT
Presentations:  Top right (content), Bottom right (title)
Documents:      Header top right or footer
Web:            Navigation bar or footer

SPECIFICATIONS
Minimum Size:   120px width (digital), 1 inch (print)
Clear Space:    Logo height × 0.5 on all sides
Background:     White box for visibility
Format:         SVG preferred, PNG with transparency
```

## 🎯 Quick Copy-Paste

### CSS Variables
```css
:root {
  --whu-blue: #2C4592;
  --whu-light-blue: #808FBE;
  --whu-red: #E7331A;
  --whu-dark-gray: #515256;
  --whu-light-gray: #EEEBEA;
  --font-primary: Arial, Helvetica, sans-serif;
}
```

### React Style Object
```javascript
const whuStyles = {
  colors: {
    primary: '#2C4592',
    secondary: '#808FBE',
    accent: '#E7331A',
    darkGray: '#515256',
    lightGray: '#EEEBEA'
  },
  fonts: {
    family: 'Arial, Helvetica, sans-serif',
    sizes: {
      title: '36px',
      h1: '28px',
      h2: '24px',
      h3: '20px',
      body: '16px'
    }
  }
};
```

### HTML Header Template
```html
<header style="background: #2C4592; color: white; padding: 20px 40px; font-family: Arial, sans-serif;">
  <h1 style="font-size: 36px; font-weight: bold; margin: 0;">
    WHU Otto Beisheim School of Management
  </h1>
</header>
```

### Python-pptx Header
```python
from pptx.util import Pt
from pptx.dml.color import RGBColor

# WHU Blue header
header.fill.solid()
header.fill.fore_color.rgb = RGBColor(44, 69, 146)

# White text
p.font.name = 'Arial'
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = RGBColor(255, 255, 255)
```

## ✅ Pre-Flight Checklist

Before delivery, verify:
- [ ] WHU Blue (#2C4592) used for primary elements
- [ ] Arial font family throughout
- [ ] Proper heading hierarchy (36→28→24→20→16px)
- [ ] Minimum 4.5:1 contrast ratio
- [ ] Generous white space (60-80px padding)
- [ ] Logo included with clear space
- [ ] WHU Red (#E7331A) for links only
- [ ] Left-aligned text (not justified)
- [ ] Consistent spacing and margins
- [ ] Professional, clean aesthetic

## 🚀 Common Use Cases

**Create HTML artifact with WHU branding:**
```
1. Use Tailwind class: bg-[#2C4592]
2. Set font: font-sans (Arial fallback)
3. Apply heading colors: text-[#2C4592]
4. Add generous padding: p-16 or p-20
```

**Style Word document:**
```
1. Title: 36pt Arial Bold, WHU Blue
2. H1: 28pt Arial Bold, WHU Blue
3. Body: 11pt Arial Regular, Black
4. Margins: 1 inch all sides
```

**Format presentation slide:**
```
1. Header bar: Full-width, WHU Blue (#2C4592), 1" height
2. Title: 28-32pt Arial Bold, White, in header
3. Body: 16-18pt Arial Regular, Black
4. Logo: White box, top right
```

## 🔗 Related Skills

- `whu-presentation-builder` - Full WHU presentations
- `whu-branded-deck` - WHU PowerPoint templates
- `docx` - Word document creation
- `pptx` - PowerPoint creation
- `pdf` - PDF document generation

---

**Pro Tip:** Always start by viewing the full brand library at:
`/mnt/skills/user/whu-brand-styler/references/whu-brand-library.md`
