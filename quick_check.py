import great_expectations as ge
from sqlalchemy import create_engine
from great_expectations.core.batch import BatchRequest, RuntimeBatchRequest
from great_expectations.checkpoint import SimpleCheckpoint


context = ge.get_context()

datasource_config = {
    "name": "DM_CustomerRegionalSales_datasource",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "SqlAlchemyExecutionEngine",
        "connection_string": "postgresql+psycopg2://postgres:password@localhost:5432/postgres",
    },
    "data_connectors": {
        "default_runtime_data_connector_name": {
            "class_name": "RuntimeDataConnector",
            "batch_identifiers": ["default_identifier_name"],
        },
        "default_inferred_data_connector_name": {
            "class_name": "InferredAssetSqlDataConnector",
            "include_schema_name": True,
        },
    },
}

context.add_datasource(**datasource_config)

batch_request = BatchRequest(
    datasource_name="DM_CustomerRegionalSales_datasource",
    data_connector_name="default_inferred_data_connector_name",
    data_asset_name="public.DM_CustomerRegionalSales",  # this is the name of the table you want to retrieve
)

suite_name = "odd_expectations_DM_CustomerRegionalSales_completeness"
validator = context.get_validator(
    batch_request=batch_request, expectation_suite_name = suite_name
)

checkpoint_config = {
    "class_name": "SimpleCheckpoint",
    "validations": [
        {
            "batch_request": batch_request,
            "expectation_suite_name": suite_name,
        }
    ],
}

checkpoint = SimpleCheckpoint(
    f"_tmp_checkpoint_{suite_name}", context, **checkpoint_config
)
results = checkpoint.run(result_format="SUMMARY", run_name="test")

validation_result_identifier = results.list_validation_result_identifiers()[0]
print(validation_result_identifier)