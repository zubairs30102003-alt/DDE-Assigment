#!/bin/bash
#
# WHU Brand Styler - Installation Script
# Version 1.0.0
#

echo "================================================"
echo "  WHU Brand Styler Skill - Installation"
echo "================================================"
echo ""

# Define colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Installation directory
INSTALL_DIR="/mnt/skills/user/whu-brand-styler"

echo -e "${BLUE}Starting installation...${NC}"
echo ""

# Check if skill already exists
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}⚠️  WHU Brand Styler skill already exists at:${NC}"
    echo "   $INSTALL_DIR"
    echo ""
    read -p "Do you want to overwrite it? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Installation cancelled.${NC}"
        exit 0
    fi
    echo -e "${BLUE}Removing existing installation...${NC}"
    rm -rf "$INSTALL_DIR"
fi

# Create directory
echo -e "${BLUE}Creating skill directory...${NC}"
mkdir -p "$INSTALL_DIR"

# Copy files
echo -e "${BLUE}Copying skill files...${NC}"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/"

# Verify installation
if [ -f "$INSTALL_DIR/SKILL.md" ]; then
    echo ""
    echo -e "${GREEN}✓ Installation successful!${NC}"
    echo ""
    echo "================================================"
    echo "  WHU Brand Styler is now installed!"
    echo "================================================"
    echo ""
    echo "📍 Location: $INSTALL_DIR"
    echo ""
    echo "📚 Documentation:"
    echo "   • Main skill:        SKILL.md"
    echo "   • Quick reference:   references/quick-reference.md"
    echo "   • Brand library:     references/whu-brand-library.md"
    echo "   • Examples:          references/implementation-examples.md"
    echo ""
    echo "🚀 Usage:"
    echo "   Just mention 'WHU branding' in your requests!"
    echo ""
    echo "   Examples:"
    echo "   • 'Create an HTML page with WHU branding'"
    echo "   • 'Apply WHU style to this document'"
    echo "   • 'Make a presentation with WHU colors'"
    echo ""
    echo "🎨 Brand Elements:"
    echo "   • WHU Blue:    #2C4592"
    echo "   • Font:        Arial"
    echo "   • Bullet:      § (section symbol)"
    echo ""
    echo "For detailed instructions, see:"
    echo "   cat $INSTALL_DIR/README.md"
    echo ""
    echo -e "${GREEN}Happy branding! 🎨${NC}"
    echo ""
else
    echo ""
    echo -e "${YELLOW}⚠️  Installation may have failed.${NC}"
    echo "Please check the directory manually:"
    echo "   ls -la $INSTALL_DIR"
    exit 1
fi
