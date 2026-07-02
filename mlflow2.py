import mlflow

experiments = mlflow.search_experiments()

for exp in experiments:
    print(f"Experiment ID: {exp.experiment_id}")
    print(f"Name         : {exp.name}")
    print(f"Artifact URI : {exp.artifact_location}")
    print("-" * 50)

experiment = mlflow.get_experiment_by_name("LinearRegressionScratch")

runs = mlflow.search_runs(
    experiment_ids=[experiment.experiment_id]
)

print(runs)