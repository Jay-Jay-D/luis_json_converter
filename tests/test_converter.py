import json
import tempfile
from pathlib import Path

from luis_json_converter.converter import Converter


def test_converter():
    # Arrange
    input_path = Path("./tests/test_data/test_case_input.json")
    output_path = Path(tempfile.NamedTemporaryFile(delete_on_close=False).name)

    expected_output = json.loads(Path("./tests/test_data/test_case_expected_output.json").open("r", encoding="utf-8").read())
    expected_mapping = {
        "WhereDatetimeV2": "DatetimeV2",
        "WhereRange": "Range",
        "WhereRangeDatetimeV2": "DatetimeV2",
        "WhereRangeDimension": "Dimension",
        "WhereRangeOrdering": "Ordering",
        "WhereOperatorSumExact": "SumExact",
        "RankingQuantity": "Quantity",
        "RankingDimension": "Dimension",
        "RankingOrderAsc": "OrderAsc",
        "RankingOrderDesc": "OrderDesc",
    }
    converter = Converter(input_path, output_path)
    # Act and Assert
    assert converter.convert()
    assert converter.clu_model == expected_output
    assert converter.mapping == expected_mapping
