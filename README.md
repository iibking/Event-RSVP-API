# Event RSVP System V1

A comprehensive event management and RSVP system designed to streamline event organization, registration, and attendee management.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Team](#team)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Event RSVP System is a modern, scalable solution for managing events and handling RSVP operations. Built with FastAPI and Python, it provides a robust backend API for event creation, management, and attendee registration.

## Features

- **Event Management**: Create, update, and manage events
- **RSVP Handling**: Seamless attendee registration and response tracking
- **RESTful API**: Clean and intuitive API endpoints for integration
- **Data Validation**: Comprehensive schema validation for all operations
- **Modular Architecture**: Well-organized codebase with separation of concerns

## Project Structure

```
app/
├── main.py                 # Application entry point
├── api/
│   └── v1/                 # API version 1
│       ├── event.py        # Event endpoints
│       └── rsvp.py         # RSVP endpoints
├── core/
│   └── db.py               # Database configuration
├── schemas/
│   ├── event_schema.py     # Event data models
│   └── rsvp_schema.py      # RSVP data models
├── service/                # Business logic layer
└── testing/
    └── test.py             # Test suite
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd Event-RSVP-System-V1
```

2. Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To start the application:

```bash
uvicorn main:app
```

The server will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

## Team

This project was developed by a dedicated team of developers:

| Name                                | Role        |
| ----------------------------------- | ----------- |
| Kpamor Raphael Terngu (Raph)        | Team Member |
| Olawoyin Jeremiah Eniola (Jeremiah) | Team Member |
| Abdullahi Ataurrahman (G.Man)       | Team Member |
| Omaku Andrew (Andrew-deb)               | Team Member |
| Abagun Omotoyosi (Error')           | Team Member |
| Okeke Kenechukwu (Kene)             | Team Member |
| Kosisochukwu Emmanuel Okoye (Sage)  | Team Member |
| Ibrahim King Ibrahim (King)         | Team Member |
| Damilola Awopegba (Damilola A)      | Team Member |
| Law Adagbon                         | Team Member |

## Contributing

To contribute to this project:

1. Create a feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
3. Push to the branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

## License

This project is proprietary and developed for educational purposes by the Alschool team.