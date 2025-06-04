🏗️ Architecture Documentation

System Overview

mermaidflowchart TD
    A[🌐 User] --> B[🚀 CLI Interface]
    B --> C[⚙️ Configuration Manager]
    C --> D[🕷️ Web Scraper Engine]
    
    D --> E[🔍 Page Discovery]
    D --> F[📄 Content Extractor]
    D --> G[🖼️ Image Downloader]
    
    E --> H[📊 URL Queue]
    F --> I[💾 Content Store]
    G --> J[🗂️ Image Store]
    
    I --> K[🔄 Data Processor]
    J --> K
    K --> L[📚 PDF Generator]
    K --> M[📝 Text Exporter]
    K --> N[🌐 HTML Exporter]
    
    L --> O[📄 Final PDF]
    M --> P[📄 Text Files]
    N --> Q[🌐 HTML Files]
    
    style A fill:#e3f2fd
    style D fill:#f3e5f5
    style K fill:#e8f5e8
    style O fill:#fff3e0

Detailed Component Architecture

1. Core Components
mermaidclassDiagram
    class WyscoutScraper {
        +session: Session
        +config: Config
        +scraped_data: List
        +scrape_all()
        +scrape_sections()
        +get_page_content()
        +extract_links()
    }
    
    class ContentExtractor {
        +extract_page_content()
        +parse_title()
        +parse_description()
        +parse_details()
        +parse_metrics()
    }
    
    class ImageProcessor {
        +download_image()
        +resize_image()
        +optimize_image()
        +validate_image()
    }
    
    class PDFGenerator {
        +create_document()
        +add_title_page()
        +add_toc()
        +add_content()
        +apply_styles()
    }
    
    WyscoutScraper --> ContentExtractor
    WyscoutScraper --> ImageProcessor
    WyscoutScraper --> PDFGenerator

2. Data Flow Architecture
mermaidsequenceDiagram
    participant U as User
    participant S as Scraper
    participant W as Website
    participant P as Processor
    participant G as Generator
    
    U->>S: Start scraping
    S->>W: GET main page
    W->>S: HTML content
    S->>S: Extract links
    
    loop For each page
        S->>W: GET page content
        W->>S: Page HTML
        S->>W: GET images
        W->>S: Image data
        S->>P: Store content
    end
    
    S->>G: Generate PDF
    G->>P: Process data
    P->>G: Formatted content
    G->>U: PDF document

3. Error Handling Flow
mermaidflowchart TD
    A[🌐 HTTP Request] --> B{Response OK?}
    B -->|Yes| C[✅ Process Content]
    B -->|No| D[❌ Error Occurred]
    
    D --> E{Retry Count < Max?}
    E -->|Yes| F[⏳ Wait Backoff]
    F --> G[🔄 Retry Request]
    G --> B
    
    E -->|No| H[📝 Log Error]
    H --> I[⏭️ Skip to Next]
    
    C --> J[💾 Store Data]
    I --> K[🏁 Continue Process]
    J --> K

Module Breakdown
Core Scraper (src/scraper.py)

Responsibilities:

Session management with proper headers
Rate limiting and retry logic
URL discovery and queue management
Coordinate content extraction

Key Methods:

pythondef scrape_all() -> List[Dict]:
    """Main orchestration method"""
    
def get_page_content(url: str) -> BeautifulSoup:
    """HTTP request with error handling"""
    
def extract_links_from_main_page() -> List[str]:
    """Discover all pages to scrape"""
Content Extractor (src/content_extractor.py)
Responsibilities:

HTML parsing and content extraction
Structure detection and normalization
Metadata extraction

Key Methods:

pythondef extract_page_content(soup: BeautifulSoup) -> Dict:
    """Extract all content from a page"""
    
def parse_sections(content: BeautifulSoup) -> Dict:
    """Parse specific content sections"""
Image Processor (src/image_processor.py)
Responsibilities:

Image downloading and validation
Format conversion and optimization
Size normalization for PDF

Key Methods:

pythondef download_image(url: str, filename: str) -> str:
    """Download and save image"""
    
def resize_for_pdf(image_path: str) -> str:
    """Optimize image for PDF inclusion"""
PDF Generator (src/pdf_generator.py)
Responsibilities:

PDF document structure and styling
Content layout and formatting
Table of contents generation

Key Methods:

pythondef create_document(data: List[Dict]) -> None:
    """Create complete PDF document"""
    
def add_styled_content(content: Dict) -> None:
    """Add formatted content section"""
Configuration Architecture
Environment-Based Configuration
mermaidgraph LR
    A[.env file] --> B[Config Class]
    C[.env.example] --> D[Documentation]
    B --> E[Scraper Components]
    B --> F[PDF Generator]
    B --> G[Image Processor]
    
    style A fill:#ffebee
    style B fill:#e8f5e8

Configuration Hierarchy

Environment Variables (highest priority)
Config file (config.py)
Default values (fallback)

Security Architecture

Data Protection

mermaidflowchart TD
    A[🔐 Sensitive Data] --> B[📁 .env file]
    B --> C[🚫 .gitignore]
    C --> D[❌ Not in Git]
    
    E[📋 Config Template] --> F[📄 .env.example]
    F --> G[✅ In Git]
    
    H[🔑 Runtime Loading] --> I[⚙️ Config Class]
    I --> J[🛡️ Environment Variables]


Security Features

Environment variable isolation
No hardcoded secrets
Input validation and sanitization
Safe file path handling
Rate limiting protection

Performance Architecture
Optimization Strategies
mermaidmindmap
  root((Performance))
    HTTP
      Session Reuse
      Connection Pooling
      Compression
    Memory
      Streaming Downloads
      Garbage Collection
      Batch Processing
    Storage
      Image Compression
      Efficient File I/O
      Cache Management
    Processing
      Lazy Loading
      Parallel Operations
      Progress Tracking

Resource Management

Memory efficient streaming
Disk space optimization
Network bandwidth management
CPU usage monitoring

Testing Architecture

Test Structure

mermaidgraph TD
    A[🧪 Test Suite] --> B[Unit Tests]
    A --> C[Integration Tests]
    A --> D[End-to-End Tests]
    
    B --> E[test_scraper.py]
    B --> F[test_pdf_generator.py]
    B --> G[test_image_processor.py]
    
    C --> H[test_integration.py]
    C --> I[test_workflow.py]
    
    D --> J[test_full_scrape.py]
    D --> K[test_output_validation.py]

Test Coverage Strategy

Unit Tests: 90%+ coverage for core logic
Integration Tests: Component interaction
Mocking: External dependencies (HTTP, file system)
Fixtures: Reusable test data

Deployment Architecture

Docker Strategy

mermaidgraph LR
    A[📝 Dockerfile] --> B[🐳 Base Image]
    B --> C[📦 Dependencies]
    C --> D[💻 Application]
    D --> E[🚀 Container]
    
    F[📋 docker-compose.yml] --> G[🔧 Multi-service]
    G --> H[💾 Volume Mounts]
    G --> I[🌐 Network Config]

CI/CD Pipeline

mermaidflowchart LR

    A[📝 Git Push] --> B[🔍 GitHub Actions]
    B --> C[🧪 Run Tests]
    C --> D[✅ Quality Checks]
    D --> E[🏗️ Build Docker]
    E --> F[📦 Create Release]
    F --> G[🚀 Deploy]

Extensibility Architecture

Plugin System Design

mermaidclassDiagram
    class BaseScraper {
        <<abstract>>
        +scrape()
        +extract_content()
        +save_data()
    }
    
    class WyscoutScraper {
        +scrape_wyscout_specific()
    }
    
    class GenericScraper {
        +scrape_generic_site()
    }
    
    class OutputGenerator {
        <<abstract>>
        +generate()
    }
    
    class PDFGenerator {
        +create_pdf()
    }
    
    class HTMLGenerator {
        +create_html()
    }
    
    BaseScraper <|-- WyscoutScraper
    BaseScraper <|-- GenericScraper
    OutputGenerator <|-- PDFGenerator
    OutputGenerator <|-- HTMLGenerator

Extension Points

Custom Scrapers: Inherit from BaseScraper
Output Formats: Implement OutputGenerator
Content Processors: Plugin architecture
Custom Styling: Template system

Monitoring and Logging

Logging Architecture

mermaidgraph TD

    A[📱 Application] --> B[📝 Structured Logging]
    B --> C[📊 Log Levels]
    B --> D[🎨 Colored Output]
    B --> E[📄 File Output]
    
    C --> F[🐛 DEBUG]
    C --> G[ℹ️ INFO]
    C --> H[⚠️ WARNING]
    C --> I[❌ ERROR]

Metrics Collection

Scraping statistics
Performance metrics
Error rates
Resource usage

Future Architecture Considerations
Scalability Improvements

Distributed Processing: Multiple worker nodes
Database Backend: Persistent storage
API Interface: RESTful service
Caching Layer: Redis/Memcached
Queue System: Celery/RQ for async processing

Technology Roadmap

mermaidtimeline

    title Technology Evolution
    
    section Current (v1.0)
        : Python Scripts
        : Local Processing
        : File Storage
    
    section Near Future (v1.5)
        : FastAPI Service
        : Docker Deployment
        : Database Storage
    
    section Long Term (v2.0)
        : Microservices
        : Cloud Native
        : ML Integration