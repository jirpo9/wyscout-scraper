#!/usr/bin/env python3
"""
Wyscout Data Glossary Web Scraper
Scrapes all content from https://dataglossary.wyscout.com/ and creates a PDF document
"""

import requests
from bs4 import BeautifulSoup
import os
import time
import re
from urllib.parse import urljoin, urlparse
from pathlib import Path
import logging
from typing import List, Dict, Tuple
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus.tableofcontents import TableOfContents
from io import BytesIO
from PIL import Image as PILImage


# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

"""Scraper pro stahování a zpracování dat z Wyscout."""


class WyscoutScraper:
    def __init__(self, base_url: str = "https://dataglossary.wyscout.com/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

        # Create directories
        self.images_dir = Path("wyscout_images")
        self.images_dir.mkdir(exist_ok=True)

        # PDF styles
        self.styles = getSampleStyleSheet()
        self.create_custom_styles()

        # Storage for scraped content
        self.all_content = []

    def create_custom_styles(self):
        """Create custom styles for PDF generation"""
        self.styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=self.styles["Heading1"],
                fontSize=24,
                spaceAfter=20,
                textColor=colors.darkblue,
                alignment=1,  # Center alignment
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="SectionTitle",
                parent=self.styles["Heading2"],
                fontSize=16,
                spaceAfter=12,
                spaceBefore=20,
                textColor=colors.darkgreen,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="Description",
                parent=self.styles["Normal"],
                fontSize=12,
                spaceAfter=10,
                firstLineIndent=0,
            )
        )

    def get_page_content(self, url: str) -> BeautifulSoup:
        """Fetch and parse a web page"""
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url)
            response.raise_for_status()

            # Add delay to be respectful to the server
            time.sleep(1)

            return BeautifulSoup(response.content, "html.parser")
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def download_image(self, img_url: str, filename: str) -> str:
        """Download an image and return local path"""
        try:
            # Make URL absolute
            if img_url.startswith("/"):
                img_url = urljoin(self.base_url, img_url)

            response = self.session.get(img_url)
            response.raise_for_status()

            # Save image
            img_path = self.images_dir / filename
            with open(img_path, "wb") as f:
                f.write(response.content)

            logger.info(f"Downloaded image: {filename}")
            return str(img_path)

        except Exception as e:
            logger.error(f"Error downloading image {img_url}: {e}")
            return None

    def extract_links_from_main_page(self) -> List[str]:
        """Extract all internal links from the main page"""
        soup = self.get_page_content(self.base_url)
        if not soup:
            return []

        links = []
        # Find all links that start with /
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.startswith("/") and href != "/":
                # Make absolute URL
                full_url = urljoin(self.base_url, href)
                if full_url not in links:
                    links.append(full_url)

        logger.info(f"Found {len(links)} unique links to scrape")
        return links

    def extract_page_content(self, url: str) -> Dict:
        """Extract content from a single page"""
        soup = self.get_page_content(url)
        if not soup:
            return None

        content = {
            "url": url,
            "title": "",
            "description": "",
            "images": [],
            "details": [],
            "metrics": [],
            "raw_text": "",
        }

        # Extract title (usually the first h1 or the page title)
        title_elem = soup.find("h1")
        if title_elem:
            content["title"] = title_elem.get_text().strip()
        else:
            # Fallback to page title or URL path
            title_elem = soup.find("title")
            if title_elem:
                content["title"] = title_elem.get_text().strip()
            else:
                content["title"] = (
                    urlparse(url).path.strip("/").replace("_", " ").title()
                )

        # Extract main content
        main_content = soup.find("main") or soup.find("body")
        if main_content:
            # Extract description (usually first paragraph or div with substantial text)
            paragraphs = main_content.find_all(["p", "div"], recursive=True)
            for p in paragraphs:
                text = p.get_text().strip()
                if len(text) > 20 and not content["description"]:
                    content["description"] = text
                    break

            # Extract images - STAHUJE VŠECHNY OBRÁZKY!
            img_counter = 1
            for img in main_content.find_all("img"):
                img_src = img.get("src", "")
                img_alt = img.get("alt", f"Image {img_counter}")

                if img_src:
                    # Generate filename
                    filename = f"{content['title'].lower().replace(' ', '_')}_{img_counter}.jpg"
                    filename = re.sub(r"[^\w\-_\.]", "", filename)

                    # Download image - FYZICKY STÁHNE OBRÁZEK
                    local_path = self.download_image(img_src, filename)
                    if local_path:
                        content["images"].append(
                            {
                                "path": local_path,
                                "alt": img_alt,
                                "original_src": img_src,
                            }
                        )
                        logger.info(f"✅ Stažen obrázek: {filename}")
                    img_counter += 1

            # Extract details section
            details_section = main_content.find(text=re.compile(r"Details", re.I))
            if details_section:
                details_parent = details_section.parent
                if details_parent:
                    # Look for list items or paragraphs after "Details"
                    next_elements = details_parent.find_next_siblings()
                    for elem in next_elements:
                        if elem.name in ["ul", "ol"]:
                            for li in elem.find_all("li"):
                                content["details"].append(li.get_text().strip())
                        elif elem.name == "p" and elem.get_text().strip():
                            content["details"].append(elem.get_text().strip())

            # Extract metrics section
            metrics_section = main_content.find(
                text=re.compile(r"Available metrics", re.I)
            )
            if metrics_section:
                metrics_parent = metrics_section.parent
                if metrics_parent:
                    next_elements = metrics_parent.find_next_siblings()
                    for elem in next_elements:
                        if elem.get_text().strip():
                            content["metrics"].append(elem.get_text().strip())

            # Get all text for fallback
            content["raw_text"] = main_content.get_text().strip()

        return content

    def scrape_all_content(self):
        """Scrape content from main page and all linked pages"""
        logger.info("Starting to scrape Wyscout Data Glossary...")

        # Get main page content
        main_content = self.extract_page_content(self.base_url)
        if main_content:
            main_content["title"] = "Wyscout Data Glossary - Overview"
            self.all_content.append(main_content)

        # Get all links
        links = self.extract_links_from_main_page()

        # Scrape each linked page
        for i, link in enumerate(links, 1):
            logger.info(f"Scraping page {i}/{len(links)}: {link}")
            content = self.extract_page_content(link)
            if content:
                self.all_content.append(content)

            # Be respectful to the server
            time.sleep(1)

        logger.info(f"Scraped {len(self.all_content)} pages total")

    def resize_image_for_pdf(
        self, img_path: str, max_width: int = 400, max_height: int = 300
    ) -> str:
        """Resize image to fit in PDF"""
        try:
            with PILImage.open(img_path) as img:
                # Calculate new size maintaining aspect ratio
                img_width, img_height = img.size
                ratio = min(max_width / img_width, max_height / img_height)

                if ratio < 1:  # Only resize if image is larger
                    new_width = int(img_width * ratio)
                    new_height = int(img_height * ratio)
                    img = img.resize(
                        (new_width, new_height), PILImage.Resampling.LANCZOS
                    )

                    # Save resized image
                    resized_path = img_path.replace(".jpg", "_resized.jpg")
                    img.save(resized_path, "JPEG", quality=85)
                    return resized_path

            return img_path
        except Exception as e:
            logger.error(f"Error resizing image {img_path}: {e}")
            return img_path

    def create_pdf(self, filename: str = "wyscout_data_glossary.pdf"):
        """Create PDF document from scraped content"""
        logger.info(f"Creating PDF: {filename}")

        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []

        # Title page
        story.append(Paragraph("Wyscout Data Glossary", self.styles["CustomTitle"]))
        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph("Complete Reference Guide", self.styles["Heading2"]))
        story.append(Spacer(1, 0.3 * inch))
        story.append(
            Paragraph(f"Generated from: {self.base_url}", self.styles["Normal"])
        )
        story.append(PageBreak())

        # Table of contents
        story.append(Paragraph("Table of Contents", self.styles["Heading1"]))
        story.append(Spacer(1, 0.2 * inch))

        for i, content in enumerate(self.all_content):
            if content["title"]:
                story.append(
                    Paragraph(f"{i+1}. {content['title']}", self.styles["Normal"])
                )

        story.append(PageBreak())

        # Content pages
        for content in self.all_content:
            if not content:
                continue

            # Page title
            if content["title"]:
                story.append(Paragraph(content["title"], self.styles["SectionTitle"]))
                story.append(Spacer(1, 0.2 * inch))

            # Description
            if content["description"]:
                story.append(
                    Paragraph(content["description"], self.styles["Description"])
                )
                story.append(Spacer(1, 0.1 * inch))

            # Images
            for img_info in content["images"]:
                try:
                    resized_path = self.resize_image_for_pdf(img_info["path"])
                    img = Image(resized_path)
                    story.append(img)
                    if img_info["alt"]:
                        story.append(
                            Paragraph(
                                f"<i>{img_info['alt']}</i>", self.styles["Normal"]
                            )
                        )
                    story.append(Spacer(1, 0.1 * inch))
                except Exception as e:
                    logger.error(f"Error adding image to PDF: {e}")

            # Details section
            if content["details"]:
                story.append(Paragraph("<b>Details:</b>", self.styles["Normal"]))
                for detail in content["details"]:
                    story.append(Paragraph(f"• {detail}", self.styles["Normal"]))
                story.append(Spacer(1, 0.1 * inch))

            # Metrics section
            if content["metrics"]:
                story.append(
                    Paragraph("<b>Available Metrics:</b>", self.styles["Normal"])
                )
                for metric in content["metrics"]:
                    story.append(Paragraph(metric, self.styles["Normal"]))
                story.append(Spacer(1, 0.1 * inch))

            # Add page break between sections
            story.append(PageBreak())

        # Build PDF
        doc.build(story)
        logger.info(f"PDF created successfully: {filename}")


def main():
    """Main function to run the scraper"""
    scraper = WyscoutScraper()

    try:
        # Scrape all content
        scraper.scrape_all_content()

        # Create PDF
        scraper.create_pdf()

        logger.info("Scraping completed successfully!")
        logger.info(f"Images saved in: {scraper.images_dir}")
        logger.info("PDF created: wyscout_data_glossary.pdf")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
