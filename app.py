"""
Bicycle Helmet Data Fetcher and Filter

This module fetches bicycle helmet data from Virginia Tech's helmet safety database
and provides filtering capabilities based on various criteria.
"""

import argparse
import json
import logging
import re
import sys
from typing import Dict, List, Any
import requests


# Configuration
URL = "https://www.helmet.beam.vt.edu/js/bicycleData.js"
TIMEOUT = 30
MAX_THRESHOLD_FIELDS = {"cost", "score"}

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BicycleDataError(Exception):
    """Custom exception for bicycle data processing errors."""

    pass


def fetch_bicycle_data(url: str = URL) -> List[Dict[str, Any]]:
    """
    Fetch bicycle helmet data from the specified URL.

    Args:
        url: The URL to fetch data from

    Returns:
        List of dictionaries containing bicycle helmet data

    Raises:
        BicycleDataError: If data fetching or parsing fails
    """
    try:
        logger.info(f"Fetching data from {url}")
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        js_code = response.text

        # Extract the array assigned to bicycleDataRaw
        match = re.search(
            r"const\s+bicycleDataRaw\s*=\s*(\[.*?\]);", js_code, re.DOTALL
        )
        if not match:
            raise BicycleDataError("Could not find bicycleDataRaw in JS response")

        array_text = match.group(1)

        # Convert JS-like syntax to JSON
        json_text = array_text
        # Replace unquoted object keys with quoted keys
        json_text = re.sub(r"(\w+)(?=\s*:)", r'"\1"', json_text)
        # Replace single quotes with double quotes for string values
        json_text = re.sub(r"'([^']*)'", r'"\1"', json_text)

        data = json.loads(json_text)
        logger.info(f"Successfully fetched {len(data)} helmet records")
        return data

    except requests.RequestException as e:
        raise BicycleDataError(f"Failed to fetch data: {e}")
    except json.JSONDecodeError as e:
        raise BicycleDataError(f"Failed to parse JSON: {e}")


def filter_bicycle_data(data: List[Dict[str, Any]], **filters) -> List[Dict[str, Any]]:
    """
    Filter bicycle data based on provided criteria and sort by score (low to high).

    Args:
        data: List of dictionaries containing bicycle helmet data
        **filters: Keyword arguments for filtering
                  cost and score are treated as maximum values (inclusive)
                  other fields use exact match (case insensitive)

    Returns:
        List of filtered dictionaries sorted by score (ascending)

    Raises:
        BicycleDataError: If filtering fails
    """
    if not data:
        logger.warning("No data provided for filtering")
        return []

    try:
        filtered_data = []

        for item in data:
            if _item_matches_filters(item, filters):
                filtered_data.append(item)

        # Sort by score (low to high)
        filtered_data.sort(key=lambda x: float(x.get("score", float("inf"))))

        logger.info(f"Filtered {len(data)} items down to {len(filtered_data)} items")
        return filtered_data

    except Exception as e:
        raise BicycleDataError(f"Failed to filter data: {e}")


def _item_matches_filters(item: Dict[str, Any], filters: Dict[str, Any]) -> bool:
    """
    Check if an item matches all provided filters.

    Args:
        item: Dictionary representing a helmet record
        filters: Dictionary of field:value pairs to filter by

    Returns:
        True if item matches all filters, False otherwise
    """
    for field, value in filters.items():
        if field not in item:
            return False

        # Special handling for threshold fields
        if field in MAX_THRESHOLD_FIELDS:
            if not _check_threshold_filter(item[field], value, field):
                return False
        else:
            # Exact match for other fields (case insensitive)
            if str(item[field]).lower() != str(value).lower():
                return False

    return True


def _check_threshold_filter(item_value: Any, filter_value: Any, field: str) -> bool:
    """
    Check if item value is within threshold for cost/score fields.

    Args:
        item_value: Value from the helmet record
        filter_value: Maximum allowed value
        field: Field name (cost or score)

    Returns:
        True if item_value <= filter_value, False otherwise
    """
    try:
        if field == "cost":
            # Remove dollar sign and convert to float
            item_val = float(str(item_value).replace("$", ""))
        else:  # score
            item_val = float(item_value)

        max_val = float(filter_value)
        return item_val <= max_val

    except (ValueError, TypeError):
        logger.warning(
            f"Failed to convert {field} values: item={item_value}, filter={filter_value}"
        )
        return False


def print_results(filtered_data: List[Dict[str, Any]], filters: Dict[str, Any]) -> None:
    """
    Print filtered results in a formatted manner.

    Args:
        filtered_data: List of filtered helmet records
        filters: Dictionary of applied filters
    """
    print(f"\nFiltered data ({len(filtered_data)} items):")
    print("=" * 60)

    if not filtered_data:
        print("No helmets match your criteria.")
        return

    for i, item in enumerate(filtered_data, 1):
        print(f"\n{i}. {item.get('brand', 'Unknown')} - {item.get('model', 'Unknown')}")
        print(
            f"   Score: {item.get('score', 'N/A')} | Cost: {item.get('cost', 'N/A')} | Style: {item.get('style', 'N/A')}"
        )
        print(
            f"   Rating: {item.get('rating', 'N/A')} stars | Date: {item.get('date', 'N/A')}"
        )
        if item.get("certifications"):
            print(f"   Certifications: {item.get('certifications')}")
        print("-" * 60)

    # Print filter summary
    print("\nFILTER SUMMARY:")
    if not filters:
        print("No filters applied - showing all data")
    else:
        for key, value in filters.items():
            if key in MAX_THRESHOLD_FIELDS:
                print(f"Maximum {key.capitalize()}: {value}")
            else:
                print(f"{key.capitalize()}: {value}")
    print(f"Total results: {len(filtered_data)} items")
    print("=" * 60)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments for filtering bicycle data."""
    parser = argparse.ArgumentParser(
        description="Filter and display bicycle helmet safety data from Virginia Tech",
        epilog="Example: python bicycle_data_raw.py --style Road --cost 200 --score 15",
    )

    parser.add_argument(
        "--style",
        type=str,
        help="Filter by helmet style (e.g., Road, Mountain, Commuter)",
    )
    parser.add_argument(
        "--cost", type=float, help="Maximum cost filter in dollars (e.g., 100)"
    )
    parser.add_argument(
        "--score", type=float, help="Maximum score filter - lower is better (e.g., 10)"
    )
    parser.add_argument(
        "--brand", type=str, help="Filter by brand name (e.g., Giro, Specialized)"
    )
    parser.add_argument(
        "--rating",
        type=int,
        choices=[1, 2, 3, 4, 5],
        help="Filter by star rating (1-5)",
    )
    parser.add_argument("--date", type=str, help="Filter by date/year (e.g., 2023)")
    parser.add_argument(
        "--certifications", type=str, help="Filter by certifications (e.g., CPSC, MIPS)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    return parser.parse_args()


def main() -> None:
    """Main function to orchestrate data fetching and filtering."""
    args = parse_arguments()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Fetch data
        bicycle_data = fetch_bicycle_data()

        # Build filter dictionary from command line arguments
        filters = {
            k: v
            for k, v in vars(args).items()
            if v is not None and k not in ["verbose"]
        }

        # Apply filters
        filtered_data = filter_bicycle_data(bicycle_data, **filters)

        # Display results
        print_results(filtered_data, filters)

    except BicycleDataError as e:
        logger.error(f"Data processing error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
