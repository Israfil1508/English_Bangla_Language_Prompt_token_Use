from __future__ import annotations
import argparse
import json
from pathlib import Path
from token_analysis.config import ROOT, ExperimentConfig
from token_analysis.dataset.dataset_loader import load_dataset
from token_analysis.dataset.dataset_validator import validate_pairs
from token_analysis.llm.ollama_client import OllamaClient
from token_analysis.experiment.runner import run_experiment
from token_analysis.experiment.cache_controller import measure_reference, caching_protocol
from token_analysis.metrics.comparison import make_comparisons
from token_analysis.analysis.statistics import summarize
from token_analysis.visualization.charts import generate_charts
from token_analysis.analysis.report import generate_report


def main(argv=None):
    parser = argparse.ArgumentParser(description="English vs Bangla token cost experiment")
    parser.add_argument("action", choices=["check", "validate", "smoke", "run", "analyze", "overhead"])
    parser.add_argument("--dataset", type=Path, default=ROOT / "data" / "dataset.tsv")
    parser.add_argument("--results", type=Path, default=ROOT / "results" / "raw" / "results.csv")
    parser.add_argument("--fresh", action="store_true", help="Overwrite existing raw results")
    args = parser.parse_args(argv)
    config = ExperimentConfig()
    if args.action == "check":
        print(json.dumps(OllamaClient(config).healthcheck(), ensure_ascii=False, indent=2))
        return
    pairs = load_dataset(args.dataset)
    validate_pairs(pairs)
    if args.action == "validate":
        print(f"Dataset valid: {len(pairs)} aligned prompt pairs")
        return
    if args.action == "overhead":
        client = OllamaClient(config)
        print("Caching limitation:", caching_protocol())
        print("Reference repeated requests:", json.dumps(measure_reference(client), indent=2))
        return
    if args.action in ("smoke", "run"):
        client = OllamaClient(config)
        stats = run_experiment(pairs, client, config, args.results,
                               max_pairs=2 if args.action == "smoke" else None,
                               resume=not args.fresh)
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return
    comparisons = ROOT / "results" / "processed" / "comparison.csv"
    print("Pairs:", make_comparisons(args.results, comparisons))
    summary = summarize(comparisons, config.seed)
    files = generate_charts(comparisons, ROOT / "results" / "charts")
    report = ROOT / "results" / "processed" / "summary.json"
    report.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print("Generated charts:", *files, sep="\n")
    print("Summary:", report)
    generated = generate_report(summary, ROOT / "data" / "quality_review.csv",
                                ROOT / "reports" / "generated_report.md")
    print("Generated report draft:", generated)

if __name__ == "__main__":
    main()
