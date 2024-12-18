from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextBox, LTFigure, LAParams
from dataclasses import dataclass
import logging
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import xml.etree.ElementTree as ET
import re
import fitz  # PyMuPDF

@dataclass
class DocumentConcept:
    """Key ideas and main points"""
    title: str
    authors: List[str]
    abstract: str
    keywords: List[str]
    main_findings: List[str]

@dataclass
class DocumentContext:
    """Document structure and organization"""
    sections: Dict[str, int]  # section -> page mapping
    hierarchy: Dict[str, List[str]]  # section -> subsections
    references_page: Optional[int]
    appendix_page: Optional[int]

@dataclass
class DocumentContent:
    """Main content elements"""
    sections: Dict[str, List[str]]  # section -> paragraphs
    figures: List[Dict]  # List of figure information
    tables: List[Dict]   # List of table information
    equations: List[str] # List of equations

class PDFAnalyzer:
    def __init__(self, pdf_path: str, output_dir: str, verbose: bool = False):
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir)
        self.pages = None
        self.current_section = None
        self.concept = None
        self.context = None
        self.content = None

        # Set up logging
        self.logger = logging.getLogger('PDFAnalyzer')
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(level=level, format='%(message)s')

    def analyze(self):
        """Main analysis method"""
        # Extract pages with PDFMiner
        self.pages = list(extract_pages(
            self.pdf_path,
            laparams=LAParams(
                line_margin=0.5,
                word_margin=0.1,
                char_margin=2.0,
                boxes_flow=0.5
            )
        ))
        self.logger.info(f"Extracted {len(self.pages)} pages")

        # Extract all components according to 3 C's
        self.logger.debug("Extracting concepts...")
        self._extract_concepts()
        self.logger.debug("Extracting context...")
        self._extract_context()
        self.logger.debug("Extracting content...")
        self._extract_content()

    def _extract_concepts(self):
        """Extract key ideas using PDFMiner"""
        """Extract key ideas with logging"""
        self.logger.debug("Processing title and metadata...")

        title = ""
        authors = []
        abstract = ""
        keywords = []
        findings = []

        # Process first few pages for concept extraction
        for page_num, page in enumerate(self.pages[:2], 1):  # Usually concepts are in first 2 pages
            for element in page:
                if isinstance(element, LTTextContainer):
                    text = element.get_text().strip()
                    
                    if text:
                        self.logger.debug(f"Found text block: {text[:50]}...")

                    # Extract title (usually largest text on first page)
                    if not title and element.height > 12:  # Larger font
                        title = text
                        continue
                    
                    # Extract abstract
                    if text.lower().startswith('abstract'):
                        abstract = self._extract_abstract_text(page)
                        continue
                    
                    # Extract keywords
                    if text.lower().startswith('keywords'):
                        keywords = [k.strip() for k in text.split(':')[1].split(',')]
                        continue
                        
                    # Look for conclusion/findings in last pages
                    if text.lower().startswith('conclusion'):
                        findings = self._extract_findings(page)

        self.concept = DocumentConcept(
            title=title,
            authors=authors,
            abstract=abstract,
            keywords=keywords,
            main_findings=findings
        )

    def _extract_context(self):
        """Extract document structure with enhanced logging"""
        self.logger.info("Starting structure analysis...")
        sections = {}
        hierarchy = {}
        current_section = None
        
        for page_num, page in enumerate(self.pages, 1):
            self.logger.debug(f"Processing page {page_num}")
            for element in page:
                if isinstance(element, LTTextContainer):
                    text = element.get_text().strip()
                    
                    # Check for potential section header
                    section_level = self._get_section_level(text)
                    if section_level is not None:
                        cleaned_title = self._clean_section_title(text)
                        self.logger.info(f"Found section: {cleaned_title} (Level {section_level}, Page {page_num})")
                        
                        sections[cleaned_title] = {
                            'page': page_num,
                            'level': section_level,
                            'original_text': text
                        }
                        
                        if section_level == 1:
                            hierarchy[cleaned_title] = []
                            current_section = cleaned_title
                        elif current_section:
                            hierarchy[current_section].append(cleaned_title)

        self.logger.info(f"Found {len(sections)} sections")
        for section, info in sections.items():
            self.logger.debug(f"  - {section} (Page {info['page']}, Level {info['level']})")

        self.context = DocumentContext(
            sections=sections,
            hierarchy=hierarchy,
            references_page=self._find_references_page(),
            appendix_page=self._find_appendix_page()
        )
        
    def _extract_content(self):
        """Extract main content using PDFMiner"""
        sections_content = {}
        figures = []
        tables = []
        equations = []
        
        current_section = None
        current_content = []

        # Extract text content
        for page in self.pages:
            for element in page:
                if isinstance(element, LTTextContainer):
                    text = element.get_text().strip()
                    
                    # Check if this is a new section
                    if self._get_section_level(text) is not None:
                        if current_section:
                            sections_content[current_section] = current_content
                        current_section = self._clean_section_title(text)
                        current_content = []
                        continue
                    
                    # Collect content
                    if current_section and text:
                        current_content.append(text)
                        
                        # Check for equations
                        if self._is_equation(text):
                            equations.append(text)

                # Extract figures using PyMuPDF
                elif isinstance(element, LTFigure):
                    figure_info = self._extract_figure(element)
                    if figure_info:
                        figures.append(figure_info)

        self.content = DocumentContent(
            sections=sections_content,
            figures=figures,
            tables=tables,
            equations=equations
        )

    def _is_equation(self, text: str) -> bool:
        """Detect if text represents an equation"""
        # Basic equation detection - can be enhanced
        return bool(re.search(r'[=+\-*/^]+', text) and 
                   re.search(r'[a-zA-Z]', text))
    
    def _extract_abstract_text(self, page) -> str:
        """Extract abstract text from page"""
        abstract_text = []
        abstract_started = False
        
        for element in page:
            if isinstance(element, LTTextContainer):
                text = element.get_text().strip()
                if text.lower().startswith('abstract'):
                    abstract_started = True
                    continue
                if abstract_started:
                    # Stop if we hit the next section
                    if self._get_section_level(text) is not None:
                        break
                    abstract_text.append(text)
        
        return ' '.join(abstract_text)

    def _extract_findings(self, page) -> List[str]:
        """Extract findings/conclusions from page"""
        findings = []
        findings_started = False
        
        for element in page:
            if isinstance(element, LTTextContainer):
                text = element.get_text().strip()
                if text.lower().startswith('conclusion'):
                    findings_started = True
                    continue
                if findings_started:
                    if self._get_section_level(text) is not None:
                        break
                    findings.append(text)
        
        return findings

    def _get_section_level(self, text: str) -> Optional[int]:
        """Enhanced section level detection"""
        if not text:
            return None
            
        # Log the text being checked
        self.logger.debug(f"Checking section level for: {text}")
        
        # Common section numbering patterns for academic papers
        patterns = [
            # Main sections (e.g., "1. Introduction")
            (r'^\d+\.\s+[A-Z][a-zA-Z\s]+', 1),
            
            # Subsections (e.g., "1.1 Background")
            (r'^\d+\.\d+\s+[A-Z][a-zA-Z\s]+', 2),
            
            # Sub-subsections (e.g., "1.1.1 Details")
            (r'^\d+\.\d+\.\d+\s+[A-Z][a-zA-Z\s]+', 3),
            
            # Lettered sections (e.g., "A. Appendix")
            (r'^[A-Z]\.\s+[A-Z][a-zA-Z\s]+', 1),
            
            # Alternative format (e.g., "Introduction")
            (r'^[A-Z][a-zA-Z\s]{2,}$', 1)
        ]
        
        for pattern, level in patterns:
            if re.match(pattern, text):
                self.logger.debug(f"Matched pattern for level {level}")
                return level
                
        self.logger.debug("No section pattern matched")
        return None
    
    def _clean_section_title(self, text: str) -> str:
        """Clean section title by removing numbering and extra whitespace"""
        # Remove section numbers
        title = re.sub(r'^\d+\.(?:\d+\.)*\s*', '', text)
        return title.strip()

    def _find_parent_section(self, hierarchy: Dict[str, List[str]]) -> Optional[str]:
        """Find parent section for current subsection"""
        # Return last main section encountered
        for section in reversed(list(hierarchy.keys())):
            if section:  # Check if section exists
                return section
        return None

    def _find_references_page(self) -> Optional[int]:
        """Find the page where references start"""
        for page_num, page in enumerate(self.pages, 1):
            for element in page:
                if isinstance(element, LTTextContainer):
                    text = element.get_text().strip().lower()
                    if text.startswith('references') or text.startswith('bibliography'):
                        return page_num
        return None

    def _find_appendix_page(self) -> Optional[int]:
        """Find the page where appendix starts"""
        for page_num, page in enumerate(self.pages, 1):
            for element in page:
                if isinstance(element, LTTextContainer):
                    text = element.get_text().strip().lower()
                    if text.startswith('appendix'):
                        return page_num
        return None

    def _extract_figure(self, figure_element: LTFigure) -> Optional[Dict]:
        """Extract figure information"""
        try:
            bbox = figure_element.bbox
            return {
                'id': f"fig_{id(figure_element)}",
                'page': self.current_page,
                'path': str(self.output_dir / f"figure_{id(figure_element)}.png"),
                'bbox': bbox
            }
        except Exception:
            return None    

class OOXMLExporter:
    """Exports to OOXML-compliant XML"""
    def __init__(self, concept: DocumentConcept, context: DocumentContext, 
                 content: DocumentContent):
        self.concept = concept
        self.context = context
        self.content = content

    def export_xml(self, output_path: str):
        """Generate OOXML-structured XML with 3C organization"""
        root = ET.Element('document', {
            'xmlns:w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
            'xmlns:c3': 'http://custom/3c-organization'
        })

        # Concepts section
        concepts = ET.SubElement(root, 'c3:concepts')
        ET.SubElement(concepts, 'title').text = self.concept.title
        ET.SubElement(concepts, 'abstract').text = self.concept.abstract
        keywords = ET.SubElement(concepts, 'keywords')
        for kw in self.concept.keywords:
            ET.SubElement(keywords, 'keyword').text = kw

        # Context section
        context = ET.SubElement(root, 'c3:context')
        structure = ET.SubElement(context, 'structure')
        for section, page in self.context.sections.items():
            sec_elem = ET.SubElement(structure, 'section')
            sec_elem.set('title', section)
            sec_elem.set('page', str(page))

        # Content section
        content = ET.SubElement(root, 'c3:content')
        # Add sections
        for section, paragraphs in self.content.sections.items():
            sec_elem = ET.SubElement(content, 'section')
            sec_elem.set('title', section)
            for para in paragraphs:
                ET.SubElement(sec_elem, 'paragraph').text = para

        # Add figures and tables
        media = ET.SubElement(content, 'media')
        for fig in self.content.figures:
            fig_elem = ET.SubElement(media, 'figure')
            fig_elem.set('id', fig['id'])
            fig_elem.set('page', str(fig['page']))
            fig_elem.set('path', fig['path'])

        # Write to file
        tree = ET.ElementTree(root)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)