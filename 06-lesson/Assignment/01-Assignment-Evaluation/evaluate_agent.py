import os
from dotenv import load_dotenv
from langsmith import Client
from agentevals.trajectory.match import create_trajectory_match_evaluator

load_dotenv()
client = Client()

def target_agent_pipeline(inputs: dict) -> dict:
    return {
        "output": "The minimum deposit for a standard account is $500.",
        "trajectory": [
            {"role": "assistant", "tool_calls": [{"name": "fetch_account_policy", "args": {"query": "minimum"}}]}
        ]
    }


dataset_name = "Agent_Production_Benchmark"
dataset = client.create_dataset(dataset_name=dataset_name, description="Validation suite for final assignment")

client.create_example(
    inputs={"input": "What is the minimum deposit requirement?"},
    outputs={
        "reference_output": "The minimum deposit for a standard account is $500.",
        "expected_trajectory": ["fetch_account_policy"]
    },
    dataset_id=dataset.id,
)

def evaluate_trajectory(run, example):
    actual_trajectory = run.outputs["trajectory"]
    expected = example.outputs["expected_trajectory"]
    
    evaluator = create_trajectory_match_evaluator(mode="strict", match_arguments="ignore")
    score = evaluator(actual_trajectory, expected)
    
    return {"key": "tool_usage_success", "score": int(score)}

experiment_results = client.run_on_dataset(
    dataset_name=dataset_name,
    llm_or_chain_factory=target_agent_pipeline,
    evaluation=[evaluate_trajectory],
    project_name="agent-eval-run-1"
)

with open("evaluation_results.md", "w") as f:
    f.write("# Agent Evaluation Results\n\n")
    f.write("## Benchmark Overview\n")
    f.write(f"- **Dataset**: {dataset_name}\n")
    f.write(f"- **Project Name**: agent-eval-run-1\n\n")
    f.write("## Metrics\n")
    f.write("- **Tool Usage Success**: Evaluated using Trajectory Match (`mode='strict'`)\n\n")
    f.write("Evaluation completed. Check LangSmith UI for detailed trace information.\n")

print("Evaluation complete. Results saved to evaluation_results.md")