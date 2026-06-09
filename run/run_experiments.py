import os
import subprocess
import argparse
import sys

# Define the experiment suites based on the paper's axes and repository configs
EXPERIMENTS = {
    "structural_awareness": [
        # Edge Detection
        "configs/StructuralAwareness/edge-gin.yaml",
        "configs/StructuralAwareness/edge-graphormer.yaml",
        "configs/StructuralAwareness/edge-tf.yaml",
        
        # Triangle Counting
        "configs/StructuralAwareness/triangle-gin.yaml",
        "configs/StructuralAwareness/triangle-graphormer.yaml",
        "configs/StructuralAwareness/triangle-tf.yaml",
        
        # Circular Skip Links (CSL)
        "configs/StructuralAwareness/csl-gin.yaml",
        "configs/StructuralAwareness/csl-graphormer.yaml",
        "configs/StructuralAwareness/csl-tf.yaml",
    ],
    "heterophilic": [
        # Actor
        "configs/GPS/actor-GPS.yaml",
        "configs/Graphormer/actor-Graphormer.yaml",
        
        # WebKB (Cornell, Texas, Wisconsin)
        "configs/GPS/webkb-cor-GPS.yaml",
        "configs/Graphormer/webkb-cor-Graphormer.yaml",
        "configs/GPS/webkb-tex-GPS.yaml",
        "configs/Graphormer/webkb-tex-Graphormer.yaml",
        "configs/GPS/webkb-wis-GPS.yaml",
        "configs/Graphormer/webkb-wis-Graphormer.yaml",
        
        # Wikipedia Network (Chameleon, Squirrel)
        "configs/GPS/wn-chameleon-GPS.yaml",
        "configs/Graphormer/wn-chameleon-Graphormer.yaml",
        "configs/GPS/wn-squirrel-GPS.yaml",
        "configs/Graphormer/wn-squirrel-Graphormer.yaml",
    ]
}

def run_experiment(config_path):
    """Runs a single experiment using main.py"""
    if not os.path.exists(config_path):
        print(f"[WARNING] Config not found: {config_path}. Skipping...")
        return False

    print(f"\n{'='*60}")
    print(f"🚀 STARTING EXPERIMENT: {config_path}")
    print(f"{'='*60}")
    
    # Construct the command
    cmd = [
        sys.executable, "main.py", 
        "--cfg", config_path, 
        "wandb.use", "False"  # Disabled to prevent hanging on login prompts
    ]
    
    try:
        # Run the command and stream output to the console
        subprocess.run(cmd, check=True)
        print(f"\n✅ FINISHED: {config_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ FAILED: {config_path} (Exit code: {e.returncode})")
        return False

def main():
    parser = argparse.ArgumentParser(description="Run Graph Transformer Experiments")
    parser.add_argument(
        "--suite", 
        type=str, 
        choices=["structural_awareness", "heterophilic", "all"], 
        default="all",
        help="Which suite of experiments to run."
    )
    args = parser.parse_args()

    # Ensure we are running from the root directory
    if not os.path.exists("main.py"):
        print("Error: main.py not found. Please run this script from the root repository directory.")
        sys.exit(1)

    suites_to_run = EXPERIMENTS.keys() if args.suite == "all" else [args.suite]

    total_runs = 0
    successful_runs = 0

    for suite in suites_to_run:
        print(f"\n\n{'#'*60}")
        print(f"⚙️ EXECUTING SUITE: {suite.upper()}")
        print(f"{'#'*60}")
        
        for config in EXPERIMENTS[suite]:
            total_runs += 1
            if run_experiment(config):
                successful_runs += 1

    print(f"\n\n📊 EXPERIMENT SUMMARY")
    print(f"Total Attempted:  {total_runs}")
    print(f"Total Successful: {successful_runs}")
    print(f"Total Failed:     {total_runs - successful_runs}")

if __name__ == "__main__":
    main()
