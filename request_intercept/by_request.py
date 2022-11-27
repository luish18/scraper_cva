import requests
from tqdm import tqdm

def build_payload(mun: str, uf: str, ano: str) -> dict:

    base_payload = {
        "version": "1.0.0",
        "queries": [
            {
                "Query": {"Commands": [{"SemanticQueryDataShapeCommand": {
                    "Query": {
                        "Version": 2,
                        "From": [
                                        {
                                            "Name": "_",
                                            "Entity": "_Medidas",
                                            "Type": 0
                                        },
                                        {
                                            "Name": "b",
                                            "Entity": "Base CVA",
                                            "Type": 0
                                        }
                                        ],
                        "Select": [
                            {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Source": "_"}},
                                    "Property": "1 - GERAL CVA Soma Unidades"
                                },
                                "Name": "_Medidas.1 - GERAL CVA Soma Unidades"
                            },
                            {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Source": "_"}},
                                    "Property": "1 - GERAL CVA Soma Empréstimo"
                                },
                                "Name": "_Medidas.1 - GERAL CVA Soma Empréstimo"
                            },
                            {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Source": "_"}},
                                    "Property": "1 - GERAL CVA Media Emprestimo"
                                },
                                "Name": "_Medidas.1 - GERAL CVA Media Emprestimo"
                            },
                            {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Source": "_"}},
                                    "Property": "1 - GERAL CVA Desconto Total"
                                },
                                "Name": "_Medidas.1 - GERAL CVA Desconto Total"
                            },
                            {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Source": "_"}},
                                    "Property": "1 - GERAL CVA Media Desconto"
                                },
                                "Name": "_Medidas.1 - GERAL CVA Media Desconto"
                            },
                            {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Source": "_"}},
                                    "Property": "1 - GERAL CVA Media Renda"
                                },
                                "Name": "_Medidas.1 - GERAL CVA Media Renda"
                            },
                            {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Source": "_"}},
                                    "Property": "1 - GERAL CVA Media Tx Juros"
                                },
                                "Name": "_Medidas.1 - GERAL CVA Media Tx Juros"
                            },
                            {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "b"}},
                                    "Property": "faixaRenda_"
                                },
                                "Name": "Base CVA.faixaRenda_"
                            },
                            {
                                "Aggregation": {
                                    "Expression": {"Column": {
                                        "Expression": {"SourceRef": {"Source": "b"}},
                                        "Property": "vlr_compra"
                                    }},
                                    "Function": 1
                                },
                                "Name": "Sum(Base CVA.vlr_compra)"
                            }
                        ],
                        "Where": [{"Condition": {"Not": {"Expression": {"In": {
                            "Expressions": [{"Column": {
                                            "Expression": {"SourceRef": {"Source": "b"}},
                                            "Property": "faixaRenda_"
                                            }}],
                            "Values": [[{"Literal": {"Value": "null"}}]]
                        }}}}}, {"Condition": {"In": {
                                "Expressions": [{"Column": {
                                                "Expression": {"SourceRef": {"Source": "b"}},
                                                "Property": "ds_municipio"
                                                }}],
                                "Values": [[{"Literal": {"Value": ""}}]]
                                }}}, {"Condition": {"In": {
                                    "Expressions": [{"Column": {
                                        "Expression": {"SourceRef": {"Source": "b"}},
                                        "Property": "txt_sigla_uf"
                                    }}],
                                    "Values": [[{"Literal": {"Value": ""}}]]
                                }}}, {"Condition": {"In": {
                                    "Expressions": [{"Column": {
                                                    "Expression": {"SourceRef": {"Source": "b"}},
                                                    "Property": "num_ano_orcamento"
                                                    }}],
                                    "Values": [[{"Literal": {"Value": ""}}]]
                                }}}, {"Condition": {"Not": {"Expression": {"In": {
                                    "Expressions": [{"Column": {
                                        "Expression": {"SourceRef": {"Source": "b"}},
                                        "Property": "faixaRenda_"
                                    }}],
                                    "Values": [[{"Literal": {"Value": "null"}}]]
                                }}}}}, {"Condition": {"In": {
                                        "Expressions": [{"Column": {
                                            "Expression": {"SourceRef": {"Source": "b"}},
                                            "Property": "tp_orcamento"
                                        }}],
                                        "Values": [[{"Literal": {"Value": "'Apoio a Producao'"}}], [{"Literal": {"Value": "'Carta de Credito - Individual'"}}]]
                                        }}}],
                        "OrderBy": [
                            {
                                "Direction": 1,
                                "Expression": {"Column": {
                                    "Expression": {"SourceRef": {"Source": "b"}},
                                    "Property": "faixaRenda_"
                                }}
                            }
                        ]
                    },
                    "Binding": {
                        "Primary": {"Groupings": [
                            {
                                "Projections": [0, 1, 2, 3, 4, 5, 6, 7, 8],
                                "Subtotal": 1
                            }
                        ]},
                        "DataReduction": {
                            "DataVolume": 3,
                            "Primary": {"Window": {"Count": 500}}
                        },
                        "Version": 1
                    },
                    "ExecutionMetricsKind": 1
                }}]},
                "QueryId": "",
                "ApplicationContext": {
                    "DatasetId": "4997e9fa-2be4-4230-b8a2-e9946b52d813",
                    "Sources": [
                        {
                            "ReportId": "007599ed-2c6d-43ed-bcf1-8f61ff6c51e0",
                            "VisualId": "d4c78950397d100003c9"
                        }
                    ]
                }
            }
        ],
        "cancelQueries": [],
        "modelId": 1365069
    }

    base_payload["queries"][0]["Query"]["Commands"][0]["SemanticQueryDataShapeCommand"][
        "Query"]["Where"][2]["Condition"]["In"]["Values"][0][0]["Literal"]["Value"] = f"'{mun}'"

    base_payload["queries"][0]["Query"]["Commands"][0]["SemanticQueryDataShapeCommand"][
        "Query"]["Where"][3]["Condition"]["In"]["Values"][0][0]["Literal"]["Value"] = f"'{uf}'"

    base_payload["queries"][0]["Query"]["Commands"][0]["SemanticQueryDataShapeCommand"][
        "Query"]["Where"][4]["Condition"]["In"]["Values"][0][0]["Literal"]["Value"] = f"{ano}L"

    return base_payload


def get_muns(resp, n_muns: int) -> list:

    muns = resp["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]

    muns_list = []

    for i in range(n_muns):

        muns_list.append(muns[i]["G0"])

    return muns_list


def gen_mun_list(start_mun: str) -> dict:

    url = "https://wabi-brazil-south-b-primary-api.analysis.windows.net/public/reports/querydata"

    querystring = {"synchronous": "true"}

    base_payload = {
        "version": "1.0.0",
        "queries": [
            {
                "Query": {"Commands": [{"SemanticQueryDataShapeCommand": {
                    "Query": {
                        "Version": 2,
                        "From": [
                                        {
                                            "Name": "b",
                                            "Entity": "Base CVA",
                                            "Type": 0
                                        }
                                        ],
                        "Select": [
                            {
                                "Column": {
                                    "Expression": {"SourceRef": {"Source": "b"}},
                                    "Property": "ds_municipio"
                                },
                                "Name": "Base CVA.ds_municipio"
                            }
                        ],
                        "Where": [{"Condition": {"In": {
                            "Expressions": [{"Column": {
                                "Expression": {"SourceRef": {"Source": "b"}},
                                "Property": "num_ano_orcamento"
                            }}],
                            "Values": [[{"Literal": {"Value": "2022L"}}]]
                        }}}, {"Condition": {"Not": {"Expression": {"In": {
                            "Expressions": [{"Column": {
                                "Expression": {"SourceRef": {"Source": "b"}},
                                "Property": "faixaRenda_"
                            }}],
                            "Values": [[{"Literal": {"Value": "null"}}]]
                        }}}}}, {"Condition": {"In": {
                            "Expressions": [{"Column": {
                                "Expression": {"SourceRef": {"Source": "b"}},
                                "Property": "tp_orcamento"
                            }}],
                            "Values": [[{"Literal": {"Value": "'Apoio a Producao'"}}], [{"Literal": {"Value": "'Carta de Credito - Individual'"}}]]
                        }}}]
                    },
                    "Binding": {
                        "Primary": {"Groupings": [{"Projections": [0]}]},
                        "DataReduction": {
                            "DataVolume": 6,
                            "Primary": {"Window": {"RestartTokens": [[""]]}}
                        },
                        "IncludeEmptyGroups": True,
                        "Version": 1
                    },
                    "ExecutionMetricsKind": 1
                }}]},
                "QueryId": ""
            }
        ],
        "cancelQueries": [],
        "modelId": 1365069
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,pt;q=0.7",
        "ActivityId": "f01b6bc8-27e3-4f77-81cd-b875b160436e",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://app.powerbi.com",
        "Referer": "https://app.powerbi.com/",
        "RequestId": "50a6d5d9-f755-b0fa-cfcb-d22aabcfbd53",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "X-PowerBI-ResourceKey": "eab9145a-8fd6-40b3-8b55-5e602992bfb4",
        "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"'
    }

    mun = start_mun
    base_payload["queries"][0]["Query"]["Commands"][0]["SemanticQueryDataShapeCommand"][
        "Binding"]["DataReduction"]["Primary"]["Window"]["RestartTokens"][0][0] = f"'{mun}'"

    response = requests.request(
        "POST", url, json=base_payload, headers=headers, params=querystring).json()

    mun_list = []

    metrics = response["results"][0]["result"]["data"]["metrics"]["Events"][1]["Metrics"]["RowCount"]

    while metrics >= 4:

        new_muns = get_muns(response, metrics - 2)
        for n in new_muns:
            mun_list.append(n)

        mun = mun_list[-1]

        base_payload["queries"][0]["Query"]["Commands"][0]["SemanticQueryDataShapeCommand"][
            "Binding"]["DataReduction"]["Primary"]["Window"]["RestartTokens"][0][0] = f"'{mun}'"

        response = requests.request(
            "POST", url, json=base_payload, headers=headers, params=querystring).json()

        metrics = response["results"][0]["result"]["data"]["metrics"]["Events"][1]["Metrics"]["RowCount"]

    mun_dict = {}

    uf_payload = {
        "version": "1.0.0",
        "queries": [
            {
                "Query": {
                    "Commands": [
                        {
                            "SemanticQueryDataShapeCommand": {
                                "Query": {
                                    "Version": 2,
                                    "From": [
                                        {
                                            "Name": "b",
                                            "Entity": "Base CVA",
                                            "Type": 0
                                        }
                                    ],
                                    "Select": [
                                        {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "b"
                                                    }
                                                },
                                                "Property": "txt_sigla_uf"
                                            },
                                            "Name": "Base CVA.txt_sigla_uf"
                                        }
                                    ],
                                    "Where": [
                                        {
                                            "Condition": {
                                                "In": {
                                                    "Expressions": [
                                                        {
                                                            "Column": {
                                                                "Expression": {
                                                                    "SourceRef": {
                                                                        "Source": "b"
                                                                    }
                                                                },
                                                                "Property": "ds_municipio"
                                                            }
                                                        }
                                                    ],
                                                    "Values": [
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "'Indianópolis'"
                                                                }
                                                            }
                                                        ]
                                                    ]
                                                }
                                            }
                                        },
                                        {
                                            "Condition": {
                                                "In": {
                                                    "Expressions": [
                                                        {
                                                            "Column": {
                                                                "Expression": {
                                                                    "SourceRef": {
                                                                        "Source": "b"
                                                                    }
                                                                },
                                                                "Property": "num_ano_orcamento"
                                                            }
                                                        }
                                                    ],
                                                    "Values": [
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "2022L"
                                                                }
                                                            }
                                                        ]
                                                    ]
                                                }
                                            }
                                        },
                                        {
                                            "Condition": {
                                                "Not": {
                                                    "Expression": {
                                                        "In": {
                                                            "Expressions": [
                                                                {
                                                                    "Column": {
                                                                        "Expression": {
                                                                            "SourceRef": {
                                                                                "Source": "b"
                                                                            }
                                                                        },
                                                                        "Property": "faixaRenda_"
                                                                    }
                                                                }
                                                            ],
                                                            "Values": [
                                                                [
                                                                    {
                                                                        "Literal": {
                                                                            "Value": "null"
                                                                        }
                                                                    }
                                                                ]
                                                            ]
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                        {
                                            "Condition": {
                                                "In": {
                                                    "Expressions": [
                                                        {
                                                            "Column": {
                                                                "Expression": {
                                                                    "SourceRef": {
                                                                        "Source": "b"
                                                                    }
                                                                },
                                                                "Property": "tp_orcamento"
                                                            }
                                                        }
                                                    ],
                                                    "Values": [
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "'Apoio a Producao'"
                                                                }
                                                            }
                                                        ],
                                                        [
                                                            {
                                                                "Literal": {
                                                                    "Value": "'Carta de Credito - Individual'"
                                                                }
                                                            }
                                                        ]
                                                    ]
                                                }
                                            }
                                        }
                                    ]
                                },
                                "Binding": {
                                    "Primary": {
                                        "Groupings": [
                                            {
                                                "Projections": [
                                                    0
                                                ]
                                            }
                                        ]
                                    },
                                    "DataReduction": {
                                        "DataVolume": 3,
                                        "Primary": {
                                            "Window": {}
                                        }
                                    },
                                    "IncludeEmptyGroups": True,
                                    "Version": 1
                                },
                                "ExecutionMetricsKind": 1
                            }
                        }
                    ]
                },
                "QueryId": "",
                "ApplicationContext": {
                    "DatasetId": "4997e9fa-2be4-4230-b8a2-e9946b52d813",
                    "Sources": [
                        {
                            "ReportId": "007599ed-2c6d-43ed-bcf1-8f61ff6c51e0",
                            "VisualId": "a164ac500426e0d94cb0"
                        }
                    ]
                }
            }
        ],
        "cancelQueries": [],
        "modelId": 1365069
    }

    print("Getting ufs for each mun")
    for mun in tqdm(mun_list):

        uf_payload["queries"][0]["Query"]["Commands"][0]["SemanticQueryDataShapeCommand"][
            "Query"]["Where"][0]["Condition"]["In"]["Values"][0][0]["Literal"]["Value"] = f"'{mun}'"
        response = requests.request(
            "POST", url, json=uf_payload, headers=headers, params=querystring).json()

        try:

            mun_dict[mun] = [uf["G0"] for uf in response["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]]
        
        except KeyError:

            print(f"{mun} não contem dados")
            mun_dict[mun] = None

    return mun_dict


if __name__ == "__main__":

    url = "https://wabi-brazil-south-b-primary-api.analysis.windows.net/public/reports/querydata"

    querystring = {"synchronous": "true"}

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,pt;q=0.7",
        "ActivityId": "f01b6bc8-27e3-4f77-81cd-b875b160436e",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://app.powerbi.com",
        "Referer": "https://app.powerbi.com/",
        "RequestId": "50a6d5d9-f755-b0fa-cfcb-d22aabcfbd53",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "X-PowerBI-ResourceKey": "eab9145a-8fd6-40b3-8b55-5e602992bfb4",
        "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"'
    }

    print(gen_mun_list("Abadia de Goiás"))
