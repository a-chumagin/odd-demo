import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport
import great_expectations as ge

from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:password@localhost:5432/postgres')
df = pd.read_sql_query('select * from "DM_CustomerRegionalSales"',con=engine)
profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)

data_context = ge.data_context.DataContext(context_root_dir="./great_expectations/")

# Create the suite
suite = profile.to_expectation_suite(
    suite_name="odd_expectations_DM_CustomerRegionalSales",
    data_context=data_context,
    save_suite=False,
    run_validation=False,
    build_data_docs=False,
)

# Save the suite
data_context.save_expectation_suite(suite)

# Run validation on your dataframe
batch = ge.dataset.PandasDataset(df, expectation_suite=suite)

results = data_context.run_validation_operator(
    "action_list_operator", assets_to_validate=[batch]
)
validation_result_identifier = results.list_validation_result_identifiers()[0]

# Build and open data docs
data_context.build_data_docs()
data_context.open_data_docs(validation_result_identifier)
