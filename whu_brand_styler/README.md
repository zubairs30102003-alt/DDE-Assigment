# WHU Brand Styler Skill

A comprehensive skill for applying WHU Otto Beisheim School of Management branding to any type of content - artifacts, documents, presentations, and more.

## Overview

This skill provides everything needed to create professionally branded WHU content across multiple formats:

- **HTML/React Artifacts** - Web pages, dashboards, interactive content
- **Word Documents** - Reports, papers, letters
- **PowerPoint Presentations** - Slides, pitch decks
- **PDF Documents** - Print materials, forms
- **Markdown Content** - Documentation, notes

## What's Included

### 📚 Core Files

1. **SKILL.md** - Complete skill documentation with workflows for each output type
2. **whu-brand-library.md** - Comprehensive branding specifications including:
   - Complete color palette with hex codes and usage guidelines
   - Typography system with font families, sizes, and hierarchy
   - Logo placement and specifications
   - Layout patterns for slides, documents, and web
   - Bullet point specifications
   - Image guidelines
   - Accessibility standards

3. **quick-reference.md** - Quick lookup cheatsheet with:
   - Color codes
   - Font sizes
   - Spacing values
   - Common code snippets
   - Pre-flight checklist

4. **Logo Assets** - Official WHU logos ready to use:
   - Full logo with text (whu-logo-full.png)
   - Symbol/icon only (whu-logo-icon.png)
   - Base64 versions for embedding
   - Comprehensive usage guide

## Key Features

### 🎨 Complete Brand System
- **Official Colors**: WHU Blue (#2C4592), complementary palette
- **Typography**: Arial-based hierarchy with proper sizing
- **Visual Identity**: Logos, layouts, spacing guidelines

### 🔧 Multi-Format Support
- HTML/React components with Tailwind classes
- Word document styling with python-docx
- PowerPoint layouts with python-pptx
- PDF creation with brand compliance
- Markdown templates

### ✅ Quality Assurance
- Accessibility guidelines (WCAG AA compliance)
- Brand consistency checklist
- Common troubleshooting solutions
- Example implementations

## Quick Start

### For HTML Artifacts
```jsx
// Apply WHU Blue header
<header style={{
  background: '#2C4592',
  color: 'white',
  padding: '20px 40px',
  fontFamily: 'Arial, sans-serif'
}}>
  <h1 style={{fontSize: '36px', fontWeight: 'bold'}}>
    WHU Otto Beisheim School of Management
  </h1>
</header>
```

### For Documents
```python
# WHU Blue heading
heading = doc.add_heading('Section Title', 1)
heading.runs[0].font.name = 'Arial'
heading.runs[0].font.size = Pt(28)
heading.runs[0].font.color.rgb = RGBColor(44, 69, 146)
```

### For Presentations
Use the existing `whu-presentation-builder` skill for full presentations, or apply WHU styles manually:
```python
# WHU Blue background
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(44, 69, 146)
```

## Brand Elements at a Glance

### Colors
- **Primary**: WHU Blue (#2C4592)
- **Secondary**: Light Blue (#808FBE), Dark Gray (#515256)
- **Accent**: Red (#E7331A) for links
- **Neutrals**: White, Black, grays

### Typography
- **Font**: Arial (Helvetica, sans-serif fallback)
- **Sizes**: 36px → 28px → 24px → 20px → 16px
- **Weights**: Bold (headings), Regular (body)

### Spacing
- **Sections**: 60-80px padding
- **Elements**: 20px margins
- **Line height**: 1.5 (body), 1.2 (headings)

## Installation

To use this skill:

1. Copy the entire `whu-brand-styler` folder to `/mnt/skills/user/`
2. The skill will be automatically available
3. Reference in conversations by mentioning "WHU branding" or "apply WHU brand"

## Usage Examples

### Example 1: Create WHU-branded Landing Page
```
"Create an HTML landing page for WHU's entrepreneurship program 
with proper branding"
```

Claude will:
1. Load the brand library
2. Apply WHU Blue (#2C4592) for headers
3. Use Arial fonts throughout
4. Add proper spacing and layout
5. Include branded buttons and cards

### Example 2: Style Research Report
```
"Create a Word document for my research report with WHU branding"
```

Claude will:
1. Apply WHU Blue to all headings
2. Use Arial font family
3. Set proper margins (1 inch)
4. Format bullet points with § symbol
5. Add header/footer with logo space

### Example 3: Brand Existing Content
```
"Apply WHU branding to this presentation outline"
```

Claude will:
1. Review the brand library
2. Add WHU Blue header bars
3. Format with Arial fonts
4. Apply consistent spacing
5. Include logo placement

## File Structure

```
whu-brand-styler/
├── SKILL.md                          # Main skill documentation
├── README.md                         # This file
├── references/
│   ├── whu-brand-library.md         # Complete branding specs
│   └── quick-reference.md           # Cheatsheet
└── assets/
    ├── whu-logo-full.png            # Primary WHU logo (15 KB)
    ├── whu-logo-icon.png            # WHU symbol/icon (11 KB)
    ├── logo_full_base64.txt         # Base64 encoded (for embedding)
    ├── logo_icon_base64.txt         # Base64 encoded (for embedding)
    └── LOGO_GUIDE.md                # Comprehensive logo usage guide
```

## Related Skills

This skill complements:
- **whu-presentation-builder** - Full PowerPoint presentations
- **whu-branded-deck** - WHU PowerPoint templates
- **docx** - Word document creation
- **pptx** - PowerPoint manipulation
- **pdf** - PDF generation

## Troubleshooting

### Colors Don't Match
✓ Use exact hex codes: #2C4592 (WHU Blue)  
✓ Check RGB values: rgb(44, 69, 146)  
✓ Avoid transparency/opacity modifications

### Fonts Look Wrong
✓ Confirm Arial availability  
✓ Use fallback: 'Arial, Helvetica, sans-serif'  
✓ Check font weights: Bold vs Regular

### Layout Issues
✓ Increase white space (60-80px padding)  
✓ Use generous margins (minimum 20px)  
✓ Left-align text (not justified)  
✓ Follow visual hierarchy

## Best Practices

1. **Always start** by viewing the brand library
2. **Use exact colors** - no approximations
3. **Maintain hierarchy** - proper heading levels
4. **Test accessibility** - minimum 4.5:1 contrast
5. **Keep it clean** - generous white space
6. **Stay consistent** - apply guidelines uniformly

## Accessibility Compliance

This skill ensures WCAG AA compliance:
- Minimum 4.5:1 contrast ratio for body text
- Minimum 3:1 contrast ratio for large text (18pt+)
- Semantic heading hierarchy
- Readable font sizes (minimum 16px for web)
- Alt text guidelines for images

## Version History

- **v1.0** (2025-11-11) - Initial release
  - Complete brand library
  - Multi-format support
  - Comprehensive documentation
  - Quick reference guide

## Credits

Created for WHU Otto Beisheim School of Management based on official PowerPoint template specifications.

Extracted branding elements:
- Color palette from corporate template
- Typography standards from official materials
- Layout patterns from WHU presentations
- Logo specifications from brand guidelines

## Support

For questions or issues:
1. Check the quick reference guide
2. Review the full brand library
3. Consult related WHU skills
4. Refer to official WHU branding materials

## License

This skill is created for use with WHU Otto Beisheim School of Management materials. All brand elements (colors, logos, typography) are property of WHU.

---

**Remember**: Consistency is key to professional branding. When in doubt, refer to the comprehensive brand library.
