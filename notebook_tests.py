
from pathlib import Path
from test_utils import import_notebook


def test_lakehouse_retrieval(fabric_runtime):
    """Test that silver lakehouse is retrieved correctly"""
    # Arrange
    notebook_path = Path(__file__).parent / "fabric" / "fun_customers_to_silver.Notebook" / "notebook-content.py"
    notebook = import_notebook(notebook_path, fabric_runtime, name="customers_to_silver_notebook")

    # Act
    result = notebook.get_silver_lh()

    # Assert
    assert result.id == "test-lakehouse-id"
    fabric_runtime["mssparkutils"].lakehouse.get.assert_called_once_with("lh_gold")