"""Schema definitions for ingestion."""

CANONICAL_COLUMNS = [
    "date",
    "instrument",
    "close",
    "volume",
    "market",
    "currency",
    "source",
    "dataset_id",
]

LONG_REQUIRED_COLUMNS = {"date", "instrument"}
LONG_PRICE_COLUMNS = {"close", "adj_close"}
LONG_OPTIONAL_COLUMNS = {"volume", "market", "currency"}

FORMAT_LONG = "long"
FORMAT_WIDE = "wide"
