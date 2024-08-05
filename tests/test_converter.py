import pytest

from luis_json_converter.converter import Converter


test_cases = [
    pytest.param(
    {
        "entities": [
            {
                "name": "Where",
                "children": [
                    {
                        "name": "WhereDatetimeV2",
                        "children": [],
                        "features": [{"modelName": "datetimeV2", "isRequired": True}]
                    },
                    {
                        "name": "WhereRange",
                        "children": [
                            {
                                "name": "WhereRangeDatetimeV2",
                                "children": [],
                                "features": [{"modelName": "datetimeV2", "isRequired": True}]
                            },
                            {
                                "name": "WhereRangeDimension",
                                "children": [],
                                "features": [{"modelName": "Dimensions", "isRequired": False}]
                            },
                            {
                                "name": "WhereRangeOrdering",
                                "children": [],
                                "features": [{"modelName": "_Order_expressions", "isRequired": False}]
                            }
                        ],
                        "features": []
                    },
                    {
                        "name": "WhereOperatorSumExact",
                        "children": [],
                        "features": []
                    }
                ]
            }
        ]
    },
    {
        "entities": [
            {
                "name": "Where",
                "children": [
                    {
                        "name": "DatetimeV2",
                        "children": [],
                        "features": [{"modelName": "datetimeV2", "isRequired": True}]
                    },
                    {
                        "name": "Range",
                        "children": [
                            {
                                "name": "DatetimeV2",
                                "children": [],
                                "features": [{"modelName": "datetimeV2", "isRequired": True}]
                            },
                            {
                                "name": "Dimension",
                                "children": [],
                                "features": [{"modelName": "Dimensions", "isRequired": False}]
                            },
                            {
                                "name": "Ordering",
                                "children": [],
                                "features": [{"modelName": "_Order_expressions", "isRequired": False}]
                            }
                        ],
                        "features": []
                    },
                    {
                        "name": "SumExact",
                        "children": [],
                        "features": []
                    }
                ]
            }
        ]
    },
    {
     'WhereDatetimeV2':'DatetimeV2',
     'WhereRange': 'Range',
     'WhereRangeDatetimeV2': 'DatetimeV2',
     'WhereRangeDimension': 'Dimension',
     'WhereRangeOrdering':'Ordering',
     'WhereOperatorSumExact':'SumExact'
    },
    id='Base Case'
    )
]

@pytest.mark.parametrize("input_data, expected_output, expected_mapping", test_cases)
def test_flatten_entities(input_data, expected_output, expected_mapping):
    # Arrange
    converter = Converter(input_data)
    # Act
    mapping = converter.flatten_entities()
    # Assert
    assert converter.clu_model == expected_output
    assert mapping == expected_mapping
