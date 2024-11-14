# Axis Online

A comprehensive project management system for healthcare service analysis and tracking.

## Features

- Project Management
- Service Area Analysis
- Competitor Data Management
- Y-Line Translation
- Notes and Documentation
- Data Visualization
- Reporting

## Technology Stack

- Frontend: Streamlit
- Backend: FastAPI
- Database: SQL Server
- Authentication: Windows Authentication
- Data Processing: pandas, numpy
- Testing: pytest
- Deployment: Docker + Azure App Service

## Getting Started

### Prerequisites

- Python 3.9+
- SQL Server
- Docker (for deployment)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/s76354m/AxisOnline.git
   cd AxisOnline
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. Run the application:
   ```bash
   python -m streamlit run app/main.py
   ```

## Development

### Running Tests

python run_tests.py


### Code Style
This project follows PEP 8 style guidelines. Run linting with:

flake8 app tests

## Deployment

### Docker
docker build -t axisonline .
docker run -p 8501:8501 axisonline


### Azure App Service
Deployment instructions are available in the deployment guide.

## Documentation

- [User Guide](docs/user_guide.md)
- [API Documentation](docs/api.md)
- [Development Guide](docs/development.md)
- [Deployment Guide](docs/deployment.md)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is proprietary and confidential.

## Contact

Project Manager - [@s76354m](https://github.com/s76354m)

Project Link: [https://github.com/s76354m/AxisOnline](https://github.com/s76354m/AxisOnline)