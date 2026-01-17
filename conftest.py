import pytest
from unittest.mock import Mock, MagicMock
import sys

@pytest.fixture
def fabric_runtime():
    """
    Fake Fabric runtime environment:
    - spark
    - mssparkutils
    - dbutils (optional)
    """
    # Mock the Spark and Fabric libraries before importing
    sys.modules['pyspark'] = MagicMock()
    sys.modules['pyspark.sql'] = MagicMock()
    sys.modules['sempy'] = MagicMock()
    sys.modules['sempy.fabric'] = MagicMock()
    sys.modules['delta'] = MagicMock()
    sys.modules['delta.tables'] = MagicMock()

    spark = MagicMock(name="SparkSession")

    mssparkutils = MagicMock(name="mssparkutils")
    mssparkutils.lakehouse = Mock()
    mssparkutils.lakehouse.get = Mock()
    mssparkutils.lakehouse.get.return_value.id = "test-lakehouse-id"

    dbutils = MagicMock(name="dbutils")

    return {
        "spark": spark,
        "mssparkutils": mssparkutils,
        "dbutils": dbutils,
    }