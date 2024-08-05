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
                            "features": [
                                {"modelName": "datetimeV2", "isRequired": True}
                            ],
                        },
                        {
                            "name": "WhereRange",
                            "children": [
                                {
                                    "name": "WhereRangeDatetimeV2",
                                    "children": [],
                                    "features": [
                                        {"modelName": "datetimeV2", "isRequired": True}
                                    ],
                                },
                                {
                                    "name": "WhereRangeDimension",
                                    "children": [],
                                    "features": [
                                        {"modelName": "Dimensions", "isRequired": False}
                                    ],
                                },
                                {
                                    "name": "WhereRangeOrdering",
                                    "children": [],
                                    "features": [
                                        {
                                            "modelName": "_Order_expressions",
                                            "isRequired": False,
                                        }
                                    ],
                                },
                            ],
                            "features": [],
                        },
                        {
                            "name": "WhereOperatorSumExact",
                            "children": [],
                            "features": [],
                        },
                    ],
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
                            "features": [
                                {"modelName": "datetimeV2", "isRequired": True}
                            ],
                        },
                        {
                            "name": "Range",
                            "children": [
                                {
                                    "name": "DatetimeV2",
                                    "children": [],
                                    "features": [
                                        {"modelName": "datetimeV2", "isRequired": True}
                                    ],
                                },
                                {
                                    "name": "Dimension",
                                    "children": [],
                                    "features": [
                                        {"modelName": "Dimensions", "isRequired": False}
                                    ],
                                },
                                {
                                    "name": "Ordering",
                                    "children": [],
                                    "features": [
                                        {
                                            "modelName": "_Order_expressions",
                                            "isRequired": False,
                                        }
                                    ],
                                },
                            ],
                            "features": [],
                        },
                        {"name": "SumExact", "children": [], "features": []},
                    ],
                }
            ]
        },
        {
            "WhereDatetimeV2": "DatetimeV2",
            "WhereRange": "Range",
            "WhereRangeDatetimeV2": "DatetimeV2",
            "WhereRangeDimension": "Dimension",
            "WhereRangeOrdering": "Ordering",
            "WhereOperatorSumExact": "SumExact",
        },
        id="Base Case",
    ),
    pytest.param(
        {
            "entities": [
                {
                    "name": "Ranking",
                    "children": [
                        {
                            "name": "RankingQuantity",
                            "children": [],
                            "features": [{"modelName": "number", "isRequired": True}],
                        },
                        {
                            "name": "RankingDimension",
                            "children": [],
                            "features": [
                                {"modelName": "Dimensions", "isRequired": True}
                            ],
                        },
                        {
                            "name": "RankingOrderAsc",
                            "children": [],
                            "features": [
                                {
                                    "modelName": "_TrainingListOrderAsc",
                                    "isRequired": False,
                                }
                            ],
                        },
                        {
                            "name": "RankingOrderDesc",
                            "children": [],
                            "features": [
                                {
                                    "modelName": "_TrainingListOrderDesc",
                                    "isRequired": False,
                                }
                            ],
                        },
                    ],
                    "roles": [],
                    "features": [],
                }
            ],
            "utterances": [
                {
                    "text": "2 atributo3 con peores metrica4",
                    "intent": "QueryToData",
                    "entities": [
                        {
                            "entity": "Ranking",
                            "startPos": 0,
                            "endPos": 21,
                            "children": [
                                {
                                    "entity": "RankingQuantity",
                                    "startPos": 0,
                                    "endPos": 0,
                                    "children": [],
                                },
                                {
                                    "entity": "RankingDimension",
                                    "startPos": 2,
                                    "endPos": 10,
                                    "children": [],
                                },
                                {
                                    "entity": "RankingOrderAsc",
                                    "startPos": 12,
                                    "endPos": 21,
                                    "children": [],
                                },
                            ],
                        }
                    ],
                }
            ],
        },
        {
            "entities": [
                {
                    "name": "Ranking",
                    "children": [
                        {
                            "name": "Quantity",
                            "children": [],
                            "features": [{"modelName": "number", "isRequired": True}],
                        },
                        {
                            "name": "Dimension",
                            "children": [],
                            "features": [
                                {"modelName": "Dimensions", "isRequired": True}
                            ],
                        },
                        {
                            "name": "OrderAsc",
                            "children": [],
                            "features": [
                                {
                                    "modelName": "_TrainingListOrderAsc",
                                    "isRequired": False,
                                }
                            ],
                        },
                        {
                            "name": "OrderDesc",
                            "children": [],
                            "features": [
                                {
                                    "modelName": "_TrainingListOrderDesc",
                                    "isRequired": False,
                                }
                            ],
                        },
                    ],
                    "roles": [],
                    "features": [],
                }
            ],
            "utterances": [
                {
                    "text": "2 atributo3 con peores metrica4",
                    "intent": "QueryToData",
                    "entities": [
                        {
                            "entity": "Ranking",
                            "startPos": 0,
                            "endPos": 21,
                            "children": [
                                {
                                    "entity": "Quantity",
                                    "startPos": 0,
                                    "endPos": 0,
                                    "children": [],
                                },
                                {
                                    "entity": "Dimension",
                                    "startPos": 2,
                                    "endPos": 10,
                                    "children": [],
                                },
                                {
                                    "entity": "OrderAsc",
                                    "startPos": 12,
                                    "endPos": 21,
                                    "children": [],
                                },
                            ],
                        }
                    ],
                }
            ],
        },
        {
            "RankingQuantity": "Quantity",
            "RankingDimension": "Dimension",
            "RankingOrderAsc": "OrderAsc",
            "RankingOrderDesc": "OrderDesc",
        },
        id="Update utterances.",
    ),
]


@pytest.mark.parametrize("input_data, expected_output, expected_mapping", test_cases)
def test_flatten_entities(input_data, expected_output, expected_mapping):
    # Arrange
    converter = Converter(input_data)
    # Act
    mapping = converter.flatten_entities()
    converter.update_utterances()
    # Assert
    assert converter.clu_model == expected_output
    assert mapping == expected_mapping
