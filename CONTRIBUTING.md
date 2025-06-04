🤝 Contributing to Wyscout Data Glossary Scraper

Thank you for your interest in contributing! This document provides guidelines and information for contributors.

📋 Table of Contents

Code of Conduct
Getting Started
Development Setup
Contribution Workflow
Coding Standards
Testing Guidelines
Documentation
Pull Request Process
Issue Reporting
Community

📜 Code of Conduct

This project adheres to a code of conduct adapted from the Contributor Covenant. By participating, you are expected to uphold this code.
Our Pledge

Be welcoming to newcomers and experienced contributors
Be respectful of different viewpoints and experiences
Be collaborative and help each other learn and grow
Be professional in all interactions

🚀 Getting Started

Prerequisites

Python 3.7 or higher
Git
Basic knowledge of web scraping concepts
Familiarity with HTML/CSS selectors

Types of Contributions

We welcome various types of contributions:

🐛 Bug fixes
✨ New features
📚 Documentation improvements
🧪 Test additions
🎨 Code refactoring
🌐 Translation support
📦 Dependency updates

🛠️ Development Setup

1. Fork and Clone
bash# Fork the repository on GitHub, then:
git clone https://github.com/jirpo9/wyscout-scraper.git
cd wyscout-scraper

2. Create Virtual Environment
bash# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

3. Install Dependencies
bash# Install development dependencies
pip install -r requirements-dev.txt

# Install the package in development mode
pip install -e .

4. Setup Pre-commit Hooks
bash# Install pre-commit hooks for code quality
pre-commit install

5. Verify Setup
bash# Run tests to ensure everything works
pytest

# Check code style
black --check src/ tests/
pylint src/
🔄 Contribution Workflow

1. Create Feature Branch
bash# Always create a new branch for your work
git checkout -b feature/your-feature-name

# Or for bug fixes:
git checkout -b fix/bug-description
2. Make Changes

Write your code following our coding standards
Add tests for new functionality
Update documentation as needed
Ensure all tests pass

3. Commit Changes
bash# Stage your changes
git add .

# Commit with descriptive message (see commit conventions below)
git commit -m "✨ Add new feature for processing images"
4. Push and Create PR
bash# Push your branch
git push origin feature/your-feature-name

# Create Pull Request on GitHub
🎨 Coding Standards
Code Style
We use Black for code formatting and Pylint for linting.
bash# Format code
black src/ tests/

# Check linting
pylint src/

# Sort imports
isort src/ tests/
Code Quality Guidelines
1. Function Documentation
pythondef extract_page_content(url: str) -> Dict[str, Any]:
    """
    Extract content from a single webpage.
    
    Args:
        url: The URL to scrape content from
        
    Returns:
        Dictionary containing extracted content with keys:
        - title: Page title
        - content: Main content text
        - images: List of image URLs
        
    Raises:
        requests.RequestException: If HTTP request fails
        ValueError: If URL is invalid
        
    Example:
        >>> content = extract_page_content("https://example.com")
        >>> print(content['title'])
        "Example Page"
    """
    # Implementation here
2. Type Hints
pythonfrom typing import List, Dict, Optional, Union

def process_images(
    image_urls: List[str], 
    output_dir: Path,
    max_width: Optional[int] = None
) -> Dict[str, Path]:
    """Process images with type hints for clarity."""
    # Implementation
3. Error Handling
pythonimport logging
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

def safe_request(url: str) -> Optional[requests.Response]:
    """Make HTTP request with proper error handling."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response
    except RequestException as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None
4. Configuration Usage
pythonfrom config import config

# Use configuration instead of hardcoded values
delay = config.REQUEST_DELAY
output_dir = config.OUTPUT_DIR
Commit Message Conventions
We follow Conventional Commits with emojis:
<type>(<scope>): <description>

[optional body]

[optional footer]
Types:

✨ feat: New feature
🐛 fix: Bug fix
📚 docs: Documentation changes
🎨 style: Code style changes (formatting, etc.)
♻️ refactor: Code refactoring
🧪 test: Adding or updating tests
🔧 chore: Maintenance tasks
⚡ perf: Performance improvements
🔒 security: Security improvements

Examples:
bashgit commit -m "✨ feat(scraper): add retry logic for failed requests"
git commit -m "🐛 fix(pdf): resolve image scaling issue"
git commit -m "📚 docs: update installation instructions"
git commit -m "🧪 test: add integration tests for PDF generation"

🧪 Testing Guidelines

Test Structure

tests/
├── unit/                   # Unit tests
│   ├── test_scraper.py
│   ├── test_pdf_generator.py
│   └── test_utils.py
├── integration/            # Integration tests
│   ├── test_full_workflow.py
│   └── test_api_integration.py
├── fixtures/               # Test data
│   ├── sample_pages/
│   └── mock_responses/
└── conftest.py            # Test configuration

Writing Tests

1. Unit Tests
pythonimport pytest
from unittest.mock import Mock, patch
from src.scraper import WyscoutScraper

class TestWyscoutScraper:
    """Test cases for WyscoutScraper class."""
    
    def test_initialization(self):
        """Test scraper initializes correctly."""
        scraper = WyscoutScraper()
        assert scraper.session is not None
        assert scraper.scraped_data == []
    
    @patch('src.scraper.requests.Session.get')
    def test_get_page_content_success(self, mock_get):
        """Test successful page content retrieval."""
        # Setup mock
        mock_response = Mock()
        mock_response.content = b"<html><body>Test</body></html>"
        mock_get.return_value = mock_response
        
        # Test
        scraper = WyscoutScraper()
        result = scraper.get_page_content("https://example.com")
        
        # Assertions
        assert result is not None
        mock_get.assert_called_once()

2. Integration Tests
python@pytest.mark.integration
def test_full_scraping_workflow(tmp_path):
    """Test complete scraping workflow."""
    scraper = WyscoutScraper()
    
    # Configure temporary output directory
    config.OUTPUT_DIR = tmp_path
    
    # Run scraper on small subset
    data = scraper.scrape_sections(['acceleration'])
    
    # Verify results
    assert len(data) > 0
    assert data[0]['title'] == 'Acceleration'
    assert (tmp_path / 'images').exists()

3. Test Fixtures
python# conftest.py
import pytest
from pathlib import Path

@pytest.fixture
def sample_html():
    """Sample HTML content for testing."""
    return """
    <html>
        <body>
            <h1>Test Title</h1>
            <p>Test description</p>
            <img src="/test.jpg" alt="Test image">
        </body>
    </html>
    """

@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    class MockConfig:
        REQUEST_DELAY = 0.1
        OUTPUT_DIR = Path("/tmp/test")
        MAX_RETRIES = 2
    
    return MockConfig()
Running Tests
bash# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_scraper.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run only integration tests
pytest -m integration

# Run tests in parallel
pytest -n auto
📚 Documentation
Documentation Standards

Code Comments: Explain why, not what
Docstrings: Follow Google/NumPy style
README Updates: Keep installation and usage current
API Documentation: Document all public methods
Examples: Provide practical usage examples

Documentation Structure
docs/
├── README.md              # Main documentation
├── ARCHITECTURE.md        # System design
├── API.md                 # API reference
├── DEPLOYMENT.md          # Deployment guide
├── TROUBLESHOOTING.md     # Common issues
└── examples/              # Usage examples
    ├── basic_usage.py
    ├── advanced_config.py
    └── custom_output.py
Updating Documentation
When making changes that affect:

Public API: Update API.md
Installation: Update README.md
Configuration: Update both README.md and examples
New features: Add usage examples

📥 Pull Request Process
Before Submitting

✅ Tests pass: pytest
✅ Code style: black src/ tests/ and pylint src/
✅ Documentation updated
✅ Commit messages follow conventions
✅ No merge conflicts

PR Template
When creating a PR, please include:
markdown## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature  
- [ ] Documentation update
- [ ] Refactoring
- [ ] Performance improvement

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
Review Process

Automated Checks: CI/CD runs tests and quality checks
Code Review: Maintainer reviews code quality and design
Testing: Reviewer may test functionality manually
Feedback: Address any requested changes
Approval: PR approved and merged

🐛 Issue Reporting
Bug Reports
Use our bug report template:
markdown**Describe the bug**
Clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Environment**
- OS: [e.g. Windows 10, Ubuntu 20.04]
- Python version: [e.g. 3.9.5]
- Package version: [e.g. 1.0.0]

**Additional context**
Any other context about the problem.
Feature Requests
Use our feature request template:
markdown**Is your feature request related to a problem?**
Clear description of the problem.

**Describe the solution you'd like**
Clear description of what you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features considered.

**Additional context**
Any other context or screenshots.
🌟 Recognition
Contributors
All contributors are recognized in:

README.md: Contributors section
CHANGELOG.md: Version history
GitHub: Contributors page

Contribution Levels

🥇 Gold: 10+ merged PRs or major feature contributions
🥈 Silver: 5+ merged PRs or significant improvements
🥉 Bronze: 1+ merged PRs or helpful issue reports

💬 Community

Communication Channels

GitHub Issues: Bug reports and feature requests
GitHub Discussions: General questions and ideas
Email: maintainer@example.com
Discord: Join our server

Getting Help

Check existing issues for similar problems
Read documentation and examples
Ask in discussions for general questions
Create issue for bugs or feature requests

Mentorship
New contributors can:

Look for good first issue labels
Ask for mentorship in discussions
Pair with experienced contributors
Join our newcomer-friendly events

🚀 Release Process

Version Numbering
We follow Semantic Versioning:

MAJOR: Breaking changes
MINOR: New features (backward compatible)
PATCH: Bug fixes (backward compatible)

Release Checklist

Update version in setup.py
Update CHANGELOG.md
Create release PR
Tag release after merge
Publish to PyPI (automated)
Update documentation


🙏 Thank You!

Your contributions make this project better for everyone. Whether you're fixing a typo, adding a feature, or helping with documentation, every contribution is valuable.

Happy coding! 🎉