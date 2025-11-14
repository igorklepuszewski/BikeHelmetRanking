# Bicycle Helmet Safety Data Filter

A Python tool for fetching and filtering bicycle helmet safety data from Virginia Tech's helmet safety database. This tool helps cyclists find the safest helmets based on their specific requirements and budget.

## Features

- 🚴‍♂️ Fetches real-time data from Virginia Tech's bicycle helmet safety database
- 🔍 Advanced filtering by multiple criteria (style, cost, safety score, brand, etc.)
- 📊 Results sorted by safety score (lower is better)
- 💻 Command-line interface with comprehensive options
- 🛡️ Robust error handling and logging
- 📋 Clean, formatted output with filter summaries

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd bike_helmet_ranking
```

2. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies using Poetry:
```bash
poetry install
```

4. Activate the virtual environment:
```bash
poetry shell
```

## Usage

### Basic Usage

Run without filters to see all available helmets:
```bash
poetry run python app.py
# or if in activated shell:
python app.py
```

### Filtering Options

Filter helmets by various criteria:

```bash
# Find road helmets under $200 with safety score ≤ 15
poetry run python app.py --style Road --cost 200 --score 15

# Find Giro helmets with 5-star rating
poetry run python app.py --brand Giro --rating 5

# Find helmets from 2024 with MIPS certification
poetry run python app.py --date 2024 --certifications MIPS

# Enable verbose logging
poetry run python app.py --style Mountain --cost 150 --verbose
```

### Available Filters

| Filter | Type | Description | Example |
|--------|------|-------------|---------|
| `--style` | String | Helmet style (Road, Mountain, Commuter, etc.) | `--style Road` |
| `--cost` | Float | Maximum cost in dollars | `--cost 150` |
| `--score` | Float | Maximum safety score (lower is better) | `--score 10` |
| `--brand` | String | Brand name | `--brand "Specialized"` |
| `--rating` | Integer | Star rating (1-5) | `--rating 5` |
| `--date` | String | Year/date | `--date 2024` |
| `--certifications` | String | Safety certifications | `--certifications CPSC` |
| `--verbose` | Flag | Enable detailed logging | `--verbose` |

## Understanding Safety Scores

- **Lower scores are better** - they represent lower risk of head injury
- Scores are based on Virginia Tech's rigorous testing methodology
- The scoring system considers impact protection across multiple test scenarios
- Helmets with scores under 10 are considered excellent
- Scores between 10-15 are very good
- Scores above 20 should be avoided if possible

## Output Format

The tool displays results in a clean, readable format:

```
Filtered data (3 items):
============================================================

1. Specialized - S-Works Prevail III MIPS
   Score: 8.5 | Cost: $300 | Style: Road
   Rating: 5 stars | Date: 2024
   Certifications: CPSC, CE
------------------------------------------------------------

2. Giro - Aether MIPS
   Score: 9.2 | Cost: $350 | Style: Road
   Rating: 5 stars | Date: 2023
   Certifications: CPSC, CE
------------------------------------------------------------

3. Trek - Ballista MIPS
   Score: 12.1 | Cost: $280 | Style: Road
   Rating: 4 stars | Date: 2024
   Certifications: CPSC
------------------------------------------------------------

FILTER SUMMARY:
Style: Road
Maximum Cost: 400
Maximum Score: 15
Total results: 3 items
============================================================
```

## Data Source

This tool fetches data from Virginia Tech's Helmet Lab, which conducts independent safety testing of bicycle helmets. Their testing methodology is based on:

- Linear acceleration impacts
- Rotational acceleration impacts
- Multiple impact locations and velocities
- Real-world crash data analysis

Learn more at: [https://www.helmet.beam.vt.edu/](https://www.helmet.beam.vt.edu/)

## Project Structure

```
bike_helmet_ranking/
├── README.md                 # This file
├── app.py                   # Main application
├── bicycle_data_raw.py      # Alternative implementation
├── pyproject.toml           # Poetry configuration
└── poetry.lock              # Locked dependencies
```

## Error Handling

The application includes comprehensive error handling for:

- Network connectivity issues
- Invalid data formats
- Parsing errors
- Invalid filter values
- Keyboard interruption

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Include comprehensive docstrings
- Add logging for debugging and monitoring

### Testing

To test the application:

```bash
# Test basic functionality
poetry run python app.py --style Road --cost 100

# Test with verbose output
poetry run python app.py --brand Giro --verbose

# Test error handling (invalid URL)
# Modify URL constant and run
```

### Development Dependencies

Add development dependencies:
```bash
# Add development tools
poetry add --group dev pytest ruff mypy pre-commit

# Install pre-commit hooks
poetry run pre-commit install

# Run pre-commit on all files
poetry run pre-commit run --all-files

# Run code formatting
poetry run ruff format .

# Run linting
poetry run ruff check . --fix

# Run type checking
poetry run mypy app.py

# Run tests (if implemented)
poetry run pytest
```

## License

This project is open source. Please respect Virginia Tech's data usage terms when using this tool.

## Disclaimer

This tool is for informational purposes only. Always verify helmet safety information independently and ensure any helmet you purchase meets your local safety regulations. The authors are not responsible for any decisions made based on this data.

## Support

If you encounter issues or have questions:

1. Check the verbose output with `--verbose` flag
2. Ensure you have internet connectivity
3. Verify that the Virginia Tech data source is accessible
4. Open an issue on GitHub with details about your problem

---

**Stay safe and happy cycling! 🚴‍♂️🚴‍♀️**
