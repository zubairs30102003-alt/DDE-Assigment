# WHU Brand Styler - Implementation Examples

This file contains practical, ready-to-use examples for applying WHU branding across different formats.

## Example 1: HTML Landing Page (React)

```jsx
import React from 'react';

export default function WHULandingPage() {
  const styles = {
    colors: {
      whuBlue: '#2C4592',
      lightBlue: '#808FBE',
      red: '#E7331A',
      darkGray: '#515256',
      lightGray: '#EEEBEA',
      white: '#FFFFFF',
      black: '#000000'
    },
    fonts: {
      family: 'Arial, Helvetica, sans-serif'
    }
  };

  return (
    <div style={{ fontFamily: styles.fonts.family }}>
      {/* Header */}
      <header style={{
        background: styles.colors.whuBlue,
        color: styles.colors.white,
        padding: '20px 40px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <h1 style={{
          fontSize: '28px',
          fontWeight: 'bold',
          margin: 0
        }}>
          WHU
        </h1>
        <nav style={{ display: 'flex', gap: '30px' }}>
          <a href="#" style={{
            color: styles.colors.white,
            textDecoration: 'none',
            fontSize: '16px'
          }}>Programs</a>
          <a href="#" style={{
            color: styles.colors.white,
            textDecoration: 'none',
            fontSize: '16px'
          }}>Research</a>
          <a href="#" style={{
            color: styles.colors.white,
            textDecoration: 'none',
            fontSize: '16px'
          }}>About</a>
        </nav>
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
          fontWeight: 'bold',
          color: styles.colors.whuBlue,
          marginBottom: '20px'
        }}>
          Excellence in Management Education
        </h2>
        <p style={{
          fontSize: '18px',
          lineHeight: '1.6',
          color: styles.colors.darkGray,
          marginBottom: '40px'
        }}>
          Germany's #1 business school driving innovation and leadership
        </p>
        <button style={{
          background: styles.colors.whuBlue,
          color: styles.colors.white,
          border: 'none',
          padding: '12px 32px',
          fontSize: '16px',
          fontWeight: 'bold',
          borderRadius: '4px',
          cursor: 'pointer'
        }}>
          Explore Programs
        </button>
      </section>

      {/* Features Grid */}
      <section style={{
        background: styles.colors.lightGray,
        padding: '60px 20px'
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto'
        }}>
          <h3 style={{
            fontSize: '28px',
            fontWeight: 'bold',
            color: styles.colors.whuBlue,
            textAlign: 'center',
            marginBottom: '40px'
          }}>
            Our Core Strengths
          </h3>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: '30px'
          }}>
            {[
              { title: 'Research Excellence', desc: 'Leading research in management and entrepreneurship' },
              { title: 'Global Network', desc: 'Partnerships with top business schools worldwide' },
              { title: 'Career Success', desc: '95% placement rate within 3 months of graduation' }
            ].map((item, idx) => (
              <div key={idx} style={{
                background: styles.colors.white,
                padding: '30px',
                borderRadius: '8px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
              }}>
                <h4 style={{
                  fontSize: '20px',
                  fontWeight: 'bold',
                  color: styles.colors.whuBlue,
                  marginBottom: '15px'
                }}>
                  {item.title}
                </h4>
                <p style={{
                  fontSize: '16px',
                  lineHeight: '1.5',
                  color: styles.colors.black
                }}>
                  {item.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{
        background: styles.colors.darkGray,
        color: styles.colors.white,
        padding: '40px 20px',
        textAlign: 'center'
      }}>
        <p style={{ fontSize: '14px', margin: 0 }}>
          © 2025 WHU Otto Beisheim School of Management
        </p>
      </footer>
    </div>
  );
}
```

## Example 2: Word Document Styling (Python)

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_whu_document():
    """Create a WHU-branded Word document"""
    doc = Document()
    
    # WHU Colors
    WHU_BLUE = RGBColor(44, 69, 146)
    DARK_GRAY = RGBColor(81, 82, 86)
    BLACK = RGBColor(0, 0, 0)
    
    # Set document margins (1 inch)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
    
    # Title
    title = doc.add_heading('Research Report on Entrepreneurship', 0)
    title_run = title.runs[0]
    title_run.font.name = 'Arial'
    title_run.font.size = Pt(36)
    title_run.font.bold = True
    title_run.font.color.rgb = WHU_BLUE
    
    # Subtitle
    subtitle = doc.add_paragraph('WHU Otto Beisheim School of Management')
    subtitle_format = subtitle.paragraph_format
    subtitle_format.space_after = Pt(24)
    subtitle_run = subtitle.runs[0]
    subtitle_run.font.name = 'Arial'
    subtitle_run.font.size = Pt(14)
    subtitle_run.font.color.rgb = DARK_GRAY
    
    # Heading 1
    h1 = doc.add_heading('Executive Summary', 1)
    h1_run = h1.runs[0]
    h1_run.font.name = 'Arial'
    h1_run.font.size = Pt(28)
    h1_run.font.color.rgb = WHU_BLUE
    
    # Body paragraph
    body = doc.add_paragraph(
        'This report examines the current state of entrepreneurship in Germany, '
        'with a focus on academic entrepreneurship and technology transfer. '
        'Our research indicates significant opportunities for innovation...'
    )
    body_format = body.paragraph_format
    body_format.line_spacing = 1.5
    body_format.space_after = Pt(12)
    body_run = body.runs[0]
    body_run.font.name = 'Arial'
    body_run.font.size = Pt(11)
    body_run.font.color.rgb = BLACK
    
    # Heading 2
    h2 = doc.add_heading('Key Findings', 2)
    h2_run = h2.runs[0]
    h2_run.font.name = 'Arial'
    h2_run.font.size = Pt(24)
    h2_run.font.color.rgb = WHU_BLUE
    
    # Bullet points (WHU style)
    bullet_items = [
        'German startups raised €8.5 billion in venture capital in 2024',
        'Academic spin-offs increased by 23% year-over-year',
        'Technology transfer offices reported improved efficiency'
    ]
    
    for item in bullet_items:
        bullet = doc.add_paragraph(item, style='List Bullet')
        bullet_run = bullet.runs[0]
        bullet_run.font.name = 'Arial'
        bullet_run.font.size = Pt(11)
        bullet_run.font.color.rgb = BLACK
    
    # Footer
    section = doc.sections[0]
    footer = section.footer
    footer_para = footer.paragraphs[0]
    footer_para.text = 'WHU Otto Beisheim School of Management | Page '
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_run = footer_para.runs[0]
    footer_run.font.name = 'Arial'
    footer_run.font.size = Pt(10)
    footer_run.font.color.rgb = DARK_GRAY
    
    # Save
    doc.save('whu_research_report.docx')
    print("WHU-branded document created successfully!")

if __name__ == '__main__':
    create_whu_document()
```

## Example 3: PowerPoint Slide (Python)

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def create_whu_slide():
    """Create a WHU-branded PowerPoint slide"""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)  # 16:9 aspect ratio
    
    # WHU Colors
    WHU_BLUE = RGBColor(44, 69, 146)
    WHITE = RGBColor(255, 255, 255)
    BLACK = RGBColor(0, 0, 0)
    
    # Add blank slide
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    # Add blue header bar
    header_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(0),
        Inches(10), Inches(1)
    )
    header_shape.fill.solid()
    header_shape.fill.fore_color.rgb = WHU_BLUE
    header_shape.line.fill.background()
    
    # Add title in header
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.25),
        Inches(8), Inches(0.5)
    )
    title_frame = title_box.text_frame
    title_frame.text = "Entrepreneurship Research Findings"
    title_para = title_frame.paragraphs[0]
    title_para.font.name = 'Arial'
    title_para.font.size = Pt(28)
    title_para.font.bold = True
    title_para.font.color.rgb = WHITE
    
    # Add logo placeholder (white box)
    logo_box = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(9), Inches(0.1),
        Inches(0.8), Inches(0.8)
    )
    logo_box.fill.solid()
    logo_box.fill.fore_color.rgb = WHITE
    logo_box.line.fill.background()
    logo_text = logo_box.text_frame
    logo_text.text = "WHU"
    logo_para = logo_text.paragraphs[0]
    logo_para.alignment = PP_ALIGN.CENTER
    logo_para.font.name = 'Arial'
    logo_para.font.size = Pt(16)
    logo_para.font.bold = True
    logo_para.font.color.rgb = WHU_BLUE
    
    # Add bullet points
    content_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(1.5),
        Inches(9), Inches(3.5)
    )
    text_frame = content_box.text_frame
    text_frame.word_wrap = True
    
    # Bullet 1
    p1 = text_frame.paragraphs[0]
    p1.text = "§ Startup funding increased 23% year-over-year"
    p1.level = 0
    p1.font.name = 'Arial'
    p1.font.size = Pt(18)
    p1.font.color.rgb = BLACK
    
    # Bullet 2
    p2 = text_frame.add_paragraph()
    p2.text = "§ Academic spin-offs show strong growth trajectory"
    p2.level = 0
    p2.font.name = 'Arial'
    p2.font.size = Pt(18)
    p2.font.color.rgb = BLACK
    
    # Bullet 3
    p3 = text_frame.add_paragraph()
    p3.text = "§ Technology transfer offices improve efficiency"
    p3.level = 0
    p3.font.name = 'Arial'
    p3.font.size = Pt(18)
    p3.font.color.rgb = BLACK
    
    # Save presentation
    prs.save('whu_presentation.pptx')
    print("WHU-branded presentation created successfully!")

if __name__ == '__main__':
    create_whu_slide()
```

## Example 4: CSS Stylesheet for Web

```css
/* WHU Otto Beisheim Brand Stylesheet */

:root {
  /* Colors */
  --whu-blue: #2C4592;
  --whu-light-blue: #808FBE;
  --whu-red: #E7331A;
  --whu-dark-gray: #515256;
  --whu-medium-gray: #A29795;
  --whu-light-gray: #C7C1BF;
  --whu-very-light-gray: #EEEBEA;
  --whu-white: #FFFFFF;
  --whu-black: #000000;
  
  /* Typography */
  --font-primary: Arial, Helvetica, sans-serif;
  --font-size-title: 2.25rem;     /* 36px */
  --font-size-h1: 1.75rem;        /* 28px */
  --font-size-h2: 1.5rem;         /* 24px */
  --font-size-h3: 1.25rem;        /* 20px */
  --font-size-body: 1rem;         /* 16px */
  --font-size-small: 0.875rem;    /* 14px */
  
  /* Spacing */
  --spacing-xs: 0.5rem;           /* 8px */
  --spacing-sm: 1rem;             /* 16px */
  --spacing-md: 1.25rem;          /* 20px */
  --spacing-lg: 2rem;             /* 32px */
  --spacing-xl: 3.75rem;          /* 60px */
  --spacing-xxl: 5rem;            /* 80px */
}

/* Base Styles */
body {
  font-family: var(--font-primary);
  font-size: var(--font-size-body);
  line-height: 1.5;
  color: var(--whu-black);
  margin: 0;
  padding: 0;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
  font-weight: bold;
  line-height: 1.2;
  margin-top: 0;
}

h1 {
  font-size: var(--font-size-h1);
  color: var(--whu-blue);
  margin-bottom: var(--spacing-md);
}

h2 {
  font-size: var(--font-size-h2);
  color: var(--whu-blue);
  margin-bottom: var(--spacing-md);
}

h3 {
  font-size: var(--font-size-h3);
  color: var(--whu-blue);
  margin-bottom: var(--spacing-sm);
}

p {
  margin-bottom: var(--spacing-sm);
  line-height: 1.5;
}

a {
  color: var(--whu-red);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

/* Header */
.whu-header {
  background-color: var(--whu-blue);
  color: var(--whu-white);
  padding: var(--spacing-md) var(--spacing-lg);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.whu-header h1 {
  color: var(--whu-white);
  margin: 0;
  font-size: var(--font-size-h1);
}

.whu-nav a {
  color: var(--whu-white);
  margin-left: var(--spacing-lg);
  font-size: var(--font-size-body);
}

.whu-nav a:hover {
  color: var(--whu-light-blue);
  text-decoration: none;
}

/* Container */
.whu-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-xl) var(--spacing-md);
}

/* Buttons */
.whu-btn {
  font-family: var(--font-primary);
  font-size: var(--font-size-body);
  font-weight: bold;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.whu-btn-primary {
  background-color: var(--whu-blue);
  color: var(--whu-white);
}

.whu-btn-primary:hover {
  background-color: var(--whu-light-blue);
}

.whu-btn-secondary {
  background-color: var(--whu-white);
  color: var(--whu-blue);
  border: 2px solid var(--whu-blue);
}

.whu-btn-secondary:hover {
  background-color: var(--whu-light-blue);
  border-color: var(--whu-light-blue);
  color: var(--whu-white);
}

/* Cards */
.whu-card {
  background-color: var(--whu-white);
  border: 1px solid var(--whu-light-gray);
  border-radius: 8px;
  padding: var(--spacing-lg);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.whu-card h3 {
  color: var(--whu-blue);
  margin-top: 0;
}

/* Grid */
.whu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

/* Section */
.whu-section {
  padding: var(--spacing-xl) var(--spacing-md);
}

.whu-section-alt {
  background-color: var(--whu-very-light-gray);
}

/* Footer */
.whu-footer {
  background-color: var(--whu-dark-gray);
  color: var(--whu-white);
  padding: var(--spacing-lg) var(--spacing-md);
  text-align: center;
  font-size: var(--font-size-small);
}

/* Utility Classes */
.text-center {
  text-align: center;
}

.text-primary {
  color: var(--whu-blue);
}

.bg-primary {
  background-color: var(--whu-blue);
}

.bg-light {
  background-color: var(--whu-very-light-gray);
}
```

## Example 5: Markdown Template

```markdown
---
title: "WHU Research Report"
author: "WHU Otto Beisheim School of Management"
date: "2025"
---

<div style="color: #2C4592; font-size: 36px; font-weight: bold; font-family: Arial, sans-serif; margin-bottom: 20px;">
Research Report on German Entrepreneurship
</div>

<div style="color: #515256; font-size: 14px; font-family: Arial, sans-serif; margin-bottom: 40px;">
WHU Otto Beisheim School of Management | November 2025
</div>

---

<h2 style="color: #2C4592; font-size: 28px; font-weight: bold; font-family: Arial, sans-serif;">
Executive Summary
</h2>

This report examines the current state of entrepreneurship in Germany, with particular focus on academic entrepreneurship and technology transfer.

<h3 style="color: #2C4592; font-size: 24px; font-weight: bold; font-family: Arial, sans-serif;">
Key Findings
</h3>

<span style="color: #2C4592;">§</span> German startups raised €8.5 billion in venture capital in 2024

<span style="color: #2C4592;">§</span> Academic spin-offs increased by 23% year-over-year

<span style="color: #2C4592;">§</span> Technology transfer offices reported improved efficiency

<h2 style="color: #2C4592; font-size: 28px; font-weight: bold; font-family: Arial, sans-serif;">
Methodology
</h2>

Our research employed a mixed-methods approach combining quantitative analysis of startup data with qualitative interviews with key stakeholders.

---

<div style="background-color: #EEEBEA; padding: 20px; margin: 20px 0; border-radius: 4px;">
<strong>Note:</strong> For detailed methodology and additional data, please refer to the appendix.
</div>

---

<div style="text-align: center; color: #515256; font-size: 12px; margin-top: 40px;">
© 2025 WHU Otto Beisheim School of Management
</div>
```

## Usage Notes

### For HTML/React
- Copy the React component or CSS as a starting point
- Adjust content while maintaining structure
- Use exact color hex codes
- Keep spacing generous

### For Documents
- Run Python scripts to generate branded documents
- Modify content in the script before running
- Ensure Arial font is available
- Check margins and spacing

### For Presentations
- Use as template for individual slides
- Combine with `whu-presentation-builder` for full decks
- Maintain header bar style consistently
- Include logo placeholder

### For Web Stylesheets
- Link CSS file in HTML head
- Use provided utility classes
- Override specific styles as needed
- Maintain WHU color variables

---

**Remember**: These are starting templates. Adapt them to your specific needs while maintaining WHU brand consistency!
