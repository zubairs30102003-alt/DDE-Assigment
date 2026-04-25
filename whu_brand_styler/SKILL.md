---
name: whu-brand-styler
description: Apply WHU Otto Beisheim School of Management branding to any artifact, document, or presentation. This skill provides comprehensive brand styling including colors, fonts, logos, and layouts that align with WHU's professional academic identity. Use when creating or styling HTML artifacts, Word documents, PowerPoint presentations, or any content that should follow WHU brand guidelines.
---

# WHU Brand Styler

A comprehensive skill for applying WHU Otto Beisheim School of Management branding to any type of content output - from HTML artifacts to documents to presentations.

## Overview

This skill provides a complete branding library and application guidelines for creating professionally branded WHU content. It works across multiple output formats and ensures consistent visual identity.

## When to Use This Skill

Trigger this skill when:
- User requests WHU-branded content in any format
- User asks to "apply WHU branding" or "style with WHU brand"
- Creating content for WHU-related projects, research, or presentations
- User mentions "make it look professional" in a WHU context
- Converting generic content to WHU-branded format

## Core Brand Elements

### Color System
- **Primary**: WHU Blue (#2C4592) - for headers, accents, key elements
- **Secondary**: Light Blue (#808FBE), Dark Gray (#515256) - for supporting elements
- **Accent**: Red (#E7331A) - for links and callouts
- **Neutrals**: White, Black, Gray scale - for backgrounds and text

### Typography
- **Font Family**: Arial (primary) with Helvetica, sans-serif fallbacks
- **Hierarchy**: Clear size differentiation (36px → 28px → 24px → 20px → 16px)
- **Weight**: Bold for headings, Regular for body text

### Visual Identity
- **Logo**: WHU Otto Beisheim logos included in assets/ folder
  - `whu-logo-full.png` - Full logo with text (15 KB)
  - `whu-logo-icon.png` - Symbol/icon only (11 KB)
  - Base64 versions available for embedding
- **Spacing**: Generous white space, professional margins
- **Style**: Clean, structured, academic-professional aesthetic

## Logo Assets

This skill includes official WHU logos ready to use in any content:

### Available Logos
- **Full Logo** (`assets/whu-logo-full.png`) - 585×184px, 15 KB
  - Primary logo with "WHU Otto Beisheim School of Management" text
  - Use for: Headers, title pages, primary branding
  
- **Icon/Symbol** (`assets/whu-logo-icon.png`) - 200×200px, 11 KB
  - WHU geometric symbol only
  - Use for: Small spaces, favicons, app icons

### Quick Logo Usage

**In HTML/React:**
```jsx
<img 
  src="assets/whu-logo-full.png"
  alt="WHU Otto Beisheim School of Management"
  style={{ height: '50px' }}
/>
```

**In Python (docx):**
```python
from docx.shared import Inches
doc.add_picture('assets/whu-logo-full.png', width=Inches(1.5))
```

**In Python (pptx):**
```python
from pptx.util import Inches
slide.shapes.add_picture('assets/whu-logo-full.png', 
                         Inches(8.5), Inches(0.2), width=Inches(1.3))
```

**For complete logo usage guidelines, see:**
```bash
view /mnt/skills/user/whu-brand-styler/assets/LOGO_GUIDE.md
```

## Workflow by Output Type

### For HTML/React Artifacts

#### Step 1: Load Brand Library
```bash
view /mnt/skills/user/whu-brand-styler/references/whu-brand-library.md
```

#### Step 2: Apply Core Styles

**CSS Variables Setup:**
```jsx
const styles = {
  // Colors
  whuBlue: '#2C4592',
  whuLightBlue: '#808FBE',
  whuRed: '#E7331A',
  whuDarkGray: '#515256',
  whuLightGray: '#EEEBEA',
  
  // Typography
  fontFamily: 'Arial, Helvetica, sans-serif',
  fontSize: '16px',
  lineHeight: '1.5',
};
```

**Header Component:**
```jsx
<header style={{
  background: '#2C4592',
  color: 'white',
  padding: '20px 40px',
  fontFamily: 'Arial, sans-serif',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between'
}}>
  {/* WHU Logo */}
  <img 
    src="assets/whu-logo-full.png"
    alt="WHU Otto Beisheim School of Management"
    style={{
      height: '50px',
      filter: 'brightness(0) invert(1)' // White on blue background
    }}
  />
  <h1 style={{fontSize: '36px', fontWeight: 'bold', margin: 0}}>
    WHU Otto Beisheim School of Management
  </h1>
</header>
```

**Content Section:**
```jsx
<section style={{
  maxWidth: '1200px',
  margin: '0 auto',
  padding: '60px 20px',
  fontFamily: 'Arial, sans-serif'
}}>
  <h2 style={{
    color: '#2C4592',
    fontSize: '28px',
    fontWeight: 'bold',
    marginBottom: '20px'
  }}>
    Section Title
  </h2>
  <p style={{
    fontSize: '16px',
    lineHeight: '1.5',
    color: '#000000'
  }}>
    Body content here...
  </p>
</section>
```

**Button Styling:**
```jsx
<button style={{
  background: '#2C4592',
  color: 'white',
  border: 'none',
  padding: '12px 24px',
  fontSize: '16px',
  fontWeight: 'bold',
  borderRadius: '4px',
  cursor: 'pointer',
  fontFamily: 'Arial, sans-serif'
}}>
  Call to Action
</button>
```

#### Step 3: Apply to Full Artifact

When creating artifacts:
1. **Use Tailwind classes** that match WHU colors:
   - `bg-[#2C4592]` for WHU Blue backgrounds
   - `text-[#2C4592]` for WHU Blue text
   - `font-sans` for Arial/sans-serif
   
2. **Create custom color mappings**:
```jsx
// Define WHU-specific Tailwind-compatible styles
const whuColors = {
  primary: '#2C4592',
  secondary: '#808FBE',
  accent: '#E7331A'
};
```

3. **Structure layout** with WHU principles:
   - Clean navigation bar with WHU Blue
   - Generous white space (padding: 60-80px)
   - Card-based content with subtle borders
   - Professional footer with contact info

### For Word Documents (DOCX)

#### Step 1: Read Branding Library
```bash
view /mnt/skills/user/whu-brand-styler/references/whu-brand-library.md
```

#### Step 2: Apply Document Styles

When using the `docx` skill:

**Title/Header:**
```python
# Title style
doc.add_heading('Document Title', 0)
title = doc.paragraphs[-1]
title.runs[0].font.name = 'Arial'
title.runs[0].font.size = Pt(36)
title.runs[0].font.bold = True
title.runs[0].font.color.rgb = RGBColor(44, 69, 146)  # WHU Blue
```

**Headings:**
```python
# Heading 1
doc.add_heading('Section Heading', 1)
h1 = doc.paragraphs[-1]
h1.runs[0].font.name = 'Arial'
h1.runs[0].font.size = Pt(28)
h1.runs[0].font.color.rgb = RGBColor(44, 69, 146)

# Heading 2
doc.add_heading('Subsection', 2)
h2 = doc.paragraphs[-1]
h2.runs[0].font.name = 'Arial'
h2.runs[0].font.size = Pt(24)
h2.runs[0].font.color.rgb = RGBColor(44, 69, 146)
```

**Body Text:**
```python
# Paragraph
para = doc.add_paragraph('Body text content here...')
para.runs[0].font.name = 'Arial'
para.runs[0].font.size = Pt(11)
para.runs[0].font.color.rgb = RGBColor(0, 0, 0)
para.line_spacing = 1.5
```

**Bullet Points:**
```python
# WHU-style bullet points
para = doc.add_paragraph('Bullet point text', style='List Bullet')
para.runs[0].font.name = 'Arial'
para.runs[0].font.size = Pt(11)
# Note: Custom bullet character (§) requires style modification
```

**Header/Footer:**
```python
# Add header with logo placeholder
section = doc.sections[0]
header = section.header
header_para = header.paragraphs[0]
header_para.text = 'Document Name | WHU'
header_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
```

### For PowerPoint Presentations (PPTX)

#### Step 1: Use Existing WHU Template
If creating a full presentation, use the existing WHU presentation skills:
```bash
view /mnt/skills/user/whu-presentation-builder/SKILL.md
```

#### Step 2: Apply Brand Elements to Custom Slides

When building presentations from scratch:

**Title Slide:**
```python
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# Title
title_box = slide.shapes.title
title_box.text = "Presentation Title"
title_box.text_frame.paragraphs[0].font.name = 'Arial'
title_box.text_frame.paragraphs[0].font.size = Pt(44)
title_box.text_frame.paragraphs[0].font.bold = True
title_box.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

# Add blue background rectangle
from pptx.enum.shapes import MSO_SHAPE
blue_bg = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE,
    Inches(0), Inches(0),
    Inches(10), Inches(2)
)
blue_bg.fill.solid()
blue_bg.fill.fore_color.rgb = RGBColor(44, 69, 146)
blue_bg.line.color.rgb = RGBColor(44, 69, 146)
```

**Content Slide:**
```python
# Add header bar
header = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE,
    Inches(0), Inches(0),
    Inches(10), Inches(1)
)
header.fill.solid()
header.fill.fore_color.rgb = RGBColor(44, 69, 146)  # WHU Blue
header.line.fill.background()

# Add title in header
title_box = header.text_frame
title_box.text = "Slide Title"
title_box.paragraphs[0].font.name = 'Arial'
title_box.paragraphs[0].font.size = Pt(28)
title_box.paragraphs[0].font.bold = True
title_box.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
```

### For PDF Documents

#### Step 1: Create Document with Brand Styles

Use the `pdf` skill with WHU branding:

```bash
# Read brand library first
view /mnt/skills/user/whu-brand-styler/references/whu-brand-library.md

# Use pdf skill with WHU colors and fonts
python /mnt/skills/public/pdf/scripts/create_pdf.py
```

**Apply WHU Styles:**
- Set default font to Arial
- Use WHU Blue (#2C4592) for headers
- Apply consistent spacing and margins (1 inch / 2.5cm)
- Include WHU logo in header/footer if available

### For Markdown Documents

#### Step 1: Apply Styling Syntax

```markdown
# Document Title
*Style: 36px, Bold, WHU Blue*

## Section Heading
*Style: 28px, Bold, WHU Blue*

### Subsection
*Style: 24px, Bold, WHU Blue*

Body text using standard markdown formatting.

- Bullet points in WHU Blue (§)
- Second bullet point
- Third bullet point

> **Note:** Callout boxes can use light gray background (#EEEBEA)

[Link text](#) in WHU Red (#E7331A)
```

## Brand Application Checklist

Before delivering any WHU-branded content, verify:

### ✓ Colors
- [ ] Primary color is WHU Blue (#2C4592)
- [ ] Hyperlinks use WHU Red (#E7331A)
- [ ] Gray scale matches brand specifications
- [ ] Sufficient contrast for accessibility (4.5:1 minimum)

### ✓ Typography
- [ ] Arial is primary font throughout
- [ ] Heading hierarchy is clear (36px → 28px → 24px → 20px → 16px)
- [ ] Line height is 1.5 for body text
- [ ] Consistent font weights (Bold for headings, Regular for body)

### ✓ Layout
- [ ] Generous white space and margins
- [ ] Professional, clean aesthetic
- [ ] Content is left-aligned (not justified)
- [ ] Sections are clearly delineated

### ✓ Branding Elements
- [ ] WHU logo included (if applicable)
- [ ] Logo has proper clear space
- [ ] Bullet points use § symbol in WHU Blue
- [ ] Footer includes appropriate information

### ✓ Consistency
- [ ] All elements match brand guidelines
- [ ] No conflicting colors or fonts introduced
- [ ] Professional academic tone maintained
- [ ] Accessible to all users

## Quick Reference

### Color Codes
```
WHU Blue:        #2C4592 | rgb(44, 69, 146)
Light Blue:      #808FBE | rgb(128, 143, 190)
Dark Gray:       #515256 | rgb(81, 82, 86)
Very Light Gray: #EEEBEA | rgb(238, 235, 234)
WHU Red:         #E7331A | rgb(231, 51, 26)
```

### Typography Scale
```
Title:    36-44pt | 36px | 2.25rem
H1:       28-32pt | 28px | 1.75rem
H2:       24pt    | 24px | 1.5rem
H3:       20pt    | 20px | 1.25rem
Body:     11-12pt | 16px | 1rem
Caption:  9-10pt  | 14px | 0.875rem
```

### Spacing Units
```
Section padding:    60-80px
Card padding:       20-30px
Element margin:     20px
Paragraph spacing:  16px
Line height:        1.5 (body), 1.2 (headings)
```

## Example Applications

### Example 1: HTML Landing Page

```jsx
export default function WHULandingPage() {
  return (
    <div style={{fontFamily: 'Arial, sans-serif'}}>
      {/* Header */}
      <header style={{
        background: '#2C4592',
        color: 'white',
        padding: '20px 40px'
      }}>
        <h1 style={{fontSize: '36px', fontWeight: 'bold'}}>
          WHU Otto Beisheim School of Management
        </h1>
      </header>

      {/* Hero Section */}
      <section style={{
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '80px 20px',
        textAlign: 'center'
      }}>
        <h2 style={{
          fontSize: '44px',
          color: '#2C4592',
          fontWeight: 'bold',
          marginBottom: '20px'
        }}>
          Excellence in Management Education
        </h2>
        <p style={{fontSize: '18px', lineHeight: '1.6', color: '#515256'}}>
          Leading business school in Germany
        </p>
      </section>

      {/* Content Cards */}
      <section style={{
        background: '#EEEBEA',
        padding: '60px 20px'
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '30px'
        }}>
          {['Research', 'Teaching', 'Innovation'].map(item => (
            <div key={item} style={{
              background: 'white',
              padding: '30px',
              borderRadius: '8px',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
              <h3 style={{
                fontSize: '24px',
                color: '#2C4592',
                fontWeight: 'bold',
                marginBottom: '15px'
              }}>
                {item}
              </h3>
              <p style={{fontSize: '16px', lineHeight: '1.5'}}>
                Excellence in {item.toLowerCase()}
              </p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
```

### Example 2: Document Header Markdown

```markdown
---
title: "Research Report"
author: "WHU Otto Beisheim School of Management"
date: "2025"
header-includes: |
  \usepackage{xcolor}
  \definecolor{whu blue}{RGB}{44,69,146}
  \usepackage{fontspec}
  \setmainfont{Arial}
---

\textcolor{whu blue}{\huge\textbf{Research Report Title}}

\vspace{1cm}

## Executive Summary

Body text with standard formatting...
```

### Example 3: Presentation Slide Styling

```python
# Using python-pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

# Add WHU branded title
title_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(0.5),
    Inches(9), Inches(1)
)
text_frame = title_box.text_frame
p = text_frame.paragraphs[0]
p.text = "WHU Research Findings"
p.font.name = 'Arial'
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = RGBColor(44, 69, 146)
```

## Tips for Best Results

### 1. Start with Brand Library
Always read the comprehensive brand library before starting:
```bash
view /mnt/skills/user/whu-brand-styler/references/whu-brand-library.md
```

### 2. Prioritize Consistency
- Use the exact hex codes provided
- Don't substitute fonts or colors
- Maintain spacing ratios
- Follow layout patterns

### 3. Test Accessibility
- Ensure adequate color contrast
- Use semantic HTML heading hierarchy
- Provide alt text for images
- Test on multiple devices/sizes

### 4. Leverage Existing Skills
- Use `whu-presentation-builder` for full presentations
- Combine with `docx` skill for Word documents
- Use `pdf` skill for printable documents
- Build on `pptx` skill for custom slides

### 5. Maintain Professional Tone
- Clean, uncluttered layouts
- Academic-professional language
- High-quality imagery only
- Consistent visual hierarchy

## Troubleshooting

### Colors Don't Match
- Verify you're using exact hex codes: #2C4592 (not similar blues)
- Check RGB values if hex not supported: rgb(44, 69, 146)
- Ensure no transparency/opacity modifying colors

### Fonts Look Different
- Confirm Arial is available on system
- Use proper fallbacks: 'Arial, Helvetica, sans-serif'
- Check font weights: Bold vs Regular vs Italic
- Verify font sizes match scale (36px, 28px, 24px, etc.)

### Layout Feels Off
- Add more white space (increase padding to 60-80px)
- Check margins (should be generous, minimum 20px)
- Verify text alignment (left-aligned, not justified)
- Ensure visual hierarchy is clear

### Missing Logo
- Logo files may need to be requested from user
- Use text-based header as fallback: "WHU Otto Beisheim School of Management"
- Maintain brand colors even without logo image

## Dependencies

This skill references:
- **Brand Library**: `/mnt/skills/user/whu-brand-styler/references/whu-brand-library.md`
- **Logo Assets**: `/mnt/skills/user/whu-brand-styler/assets/`
  - `whu-logo-full.png` - Primary logo with text
  - `whu-logo-icon.png` - Symbol/icon only
  - Base64 encoded versions for embedding
- **Related Skills**: `whu-presentation-builder`, `whu-branded-deck`
- **Public Skills**: `docx`, `pptx`, `pdf` skills for document creation

## Related Resources

- Official WHU website: https://www.whu.edu
- WHU presentation builder skill for full presentations
- Brand library for comprehensive specifications
- Public document creation skills (docx, pptx, pdf)

---

**Remember**: The goal is consistent, professional application of WHU's academic brand identity across all formats. When in doubt, refer to the brand library and prioritize clarity, readability, and professional presentation.
