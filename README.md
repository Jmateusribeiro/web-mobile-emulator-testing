# Web Mobile Emulator Testing

A Selenium-based test automation framework for testing mobile web applications using browser emulation. This project uses pytest and the Page Object Model pattern to test the Twitch mobile website.

## Goal

Test mobile web functionality by emulating different mobile devices (iOS and Android) in Chrome and Edge browsers without requiring physical devices or emulators.

## Features

- Mobile device emulation (iPhone 8, Pixel 7)
- Page Object Model architecture
- Parallel test execution support
- HTML reporting with screenshots
- Environment-based configuration
- Comprehensive logging

## Requirements

- Python 3.8+
- Chrome or Edge browser

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Jmateusribeiro/web-mobile-emulator-testing
cd web-mobile-emulator-testing
```

2. Install dependencies:
```bash
pip install -e .
```

Or using requirements.txt:
```bash
pip install -r requirements.txt
```

3. (Optional) Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Running Tests

### Basic execution:
```bash
pytest
```

### Run with specific browser:
```bash
pytest --Browser=Chrome
pytest --Browser=Edge
```

### Run in parallel:
```bash
pytest -n 4
```

### Using the batch file (Windows):
```bash
run_tests.bat
```

## Project Structure

```
web-mobile-emulator-testing/
│
├── config/                          # Configuration modules
│   ├── settings.py                  # Global settings and environment variables
│   ├── browser_config.py            # Browser setup and options
│   └── device_profiles.py           # Mobile device configurations
│
├── pages/                           # Page Object Model classes
│   ├── base_page.py                 # Base class with common methods
│   ├── home_page.py                 # Twitch home page
│   ├── search_page.py               # Search functionality
│   └── stream_page.py               # Stream viewing page
│
├── tests/                           # Test files
│   ├── conftest.py                  # Pytest fixtures and configuration
│   └── test_load_streaming.py       # Streaming tests
│
├── reports/                         # Test reports and logs
│   ├── report.html                  # HTML test report
│   ├── test_execution.log           # Detailed test logs
│   └── evidences/                   # Screenshots
│
├── pyproject.toml                   # Project configuration and dependencies
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
└── README.md                        # This file
```

### Key Components

- **config/**: Centralized configuration for browsers, devices, and settings
- **pages/**: Page objects representing web pages with locators and methods
- **tests/**: Test cases and pytest configuration
- **reports/**: Generated test reports, logs, and screenshots

## Configuration

### Environment Variables (.env)

```bash
BASE_URL=https://m.twitch.tv/        # Target URL
BROWSER=Chrome                       # Default browser (Chrome/Edge)
DEFAULT_WAIT_TIMEOUT=5               # Element wait timeout in seconds
HEADLESS=false                       # Headless mode (true/false)
```

### Device Profiles

Add new mobile devices in `config/device_profiles.py`:
```python
DEVICE_NAME = DeviceProfile(
    name="Device Name",
    width=375,
    height=667,
    pixel_ratio=2.0,
    user_agent="Mozilla/5.0..."
)
```

## Test Reports

After running tests, view the HTML report:
```
reports/report.html
```

Logs are available at:
```
reports/test_execution.log
```

Screenshots are saved to:
```
reports/evidences/
```
