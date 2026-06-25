from databricks.connect import DatabricksSession
from databricks.sdk import WorkspaceClient
from databricks.labs.dqx.engine import DQEngine
from databricks.labs.dqx.rule import DQRowRule
from databricks.labs.dqx.pii.nlp_engine_config import NLPEngineConfig
from databricks.labs.dqx.pii.pii_detection_funcs import does_not_contain_pii

spark = DatabricksSession.builder.serverless().getOrCreate()
ws = WorkspaceClient()
# Initialize the DQX engine:
dq_engine = DQEngine(WorkspaceClient())

# Define the DQX rule with default nlp model:
checks = [
    DQRowRule(
        criticality="error",
        check_func=does_not_contain_pii,
        column="val",
        name="does_not_contain_pii",
    )
]

# Create some sample data:
data = [
    ["My name is John Smith"],
    ["The sky is blue, road runner"],
    ["Jane Smith sent an email to sara@info.com"],
    [None],
]
df = spark.createDataFrame(data, "val string")

# Run the checks and display the output:
checked_df = dq_engine.apply_checks(df, checks)
checked_df.show()

checks = [
    # Define a PII check with a lower threshold (more sensitivity):
    DQRowRule(
        criticality="error",
        check_func=does_not_contain_pii,
        check_func_kwargs={"threshold": 0.5},
        column="val",
        name="does_not_contain_pii_lower_threshold",
    ),
    # Define a PII check with a subset of named entities:
    DQRowRule(
        criticality="error",
        check_func=does_not_contain_pii,
        check_func_kwargs={
            "entities": ["EMAIL_ADDRESS"],
        },
        column="val",
        name="contains_email_address_data",
    ),
    # Define a PII check with a built-in named-entity recognizer (SpaCy medium):
    DQRowRule(
        criticality="error",
        check_func=does_not_contain_pii,
        check_func_kwargs={
            "entities": ["PERSON", "LOCATION"],
            "nlp_engine_config": NLPEngineConfig.SPACY_MEDIUM
        },
        column="val",
        name="contains_person_or_address_data",
    ),
    # Define a PII check with a built-in named-entity recognizer (SpaCy medium):
    DQRowRule(
        criticality="error",
        check_func=does_not_contain_pii,
        check_func_kwargs={
            "entities": ["PERSON", "LOCATION"],
            "nlp_engine_config": NLPEngineConfig.SPACY_MEDIUM
        },
        column="val",
        name="contains_person_or_address_data",
    ),
]

# Create some sample data:
data = [
    ["My name is John Smith and I live at 123 Main St New York, NY 07008"],
    ["The sky is blue, road runner"],
    ["Jane Smith sent an email to sara@info.com"],
    [None],
]
df = spark.createDataFrame(data, "val string")

# Run the checks and display the output:
checked_df = dq_engine.apply_checks(df, checks)
checked_df.show()

# Define the NLP configuration:
nlp_engine_config = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en", "model_name": "en_core_web_md"}]
}

checks = [
    # Define a PII check with a custom named-entity recognizer (Stanford De-Identifier Base):
    DQRowRule(
        criticality="error",
        check_func=does_not_contain_pii,
        check_func_kwargs={"nlp_engine_config": nlp_engine_config},
        column="val",
        name="contains_pii_custom_recognizer",
    ),
]

# Initialize the DQX engine:
dq_engine = DQEngine(WorkspaceClient())

# Create some sample data:
data = [
    ["My name is John Smith and I live at 123 Main St New York, NY 07008"],
    ["The sky is blue, road runner"],
    ["Jane Smith sent an email to sara@info.com"],
    [None],
]
df = spark.createDataFrame(data, "val string")

# Run the checks and display the output:
checked_df = dq_engine.apply_checks(df, checks)
checked_df.show()
