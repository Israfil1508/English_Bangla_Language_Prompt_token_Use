from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def generate_charts(comparison_path: Path, output_dir: Path) -> list[Path]:
    df = pd.read_csv(comparison_path, encoding="utf-8-sig")
    if df.empty:
        raise ValueError("Cannot plot empty comparisons")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    created = []

    fig, ax = plt.subplots(figsize=(13, 5))
    positions = list(range(len(df)))
    ax.plot(positions, df.english_input_tokens, marker=".", label="English")
    ax.plot(positions, df.bangla_input_tokens, marker=".", label="Bangla")
    ax.set(title="Input tokens by aligned prompt pair", xlabel="Pair index", ylabel="Input tokens")
    ax.legend()
    fig.tight_layout()
    path = output_dir / "input_tokens_by_pair.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    created.append(path)

    categories = df.groupby("category").agg({"english_input_tokens": "sum", "bangla_input_tokens": "sum"})
    ratios = categories.bangla_input_tokens / categories.english_input_tokens.replace(0, float("nan"))
    fig, ax = plt.subplots(figsize=(9, 5))
    ratios.sort_values().plot(kind="barh", ax=ax)
    ax.set(title="Bangla / English input token ratio by category", xlabel="Token ratio")
    fig.tight_layout()
    path = output_dir / "category_ratios.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    created.append(path)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(["English", "Bangla"], [df.english_cost_usd.sum(), df.bangla_cost_usd.sum()])
    ax.set(title="Total notional inference cost", ylabel="USD (hypothetical)")
    fig.tight_layout()
    path = output_dir / "notional_cost.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    created.append(path)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.boxplot([df.english_latency_s, df.bangla_latency_s])
    ax.set_xticks([1, 2], ["English", "Bangla"])
    ax.set(title="Response latency by language", ylabel="Seconds")
    fig.tight_layout()
    path = output_dir / "latency.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    created.append(path)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.hist(df.input_token_ratio.dropna(), bins=12)
    ax.set(title="Distribution of pairwise input token ratios", xlabel="Bangla / English", ylabel="Pairs")
    fig.tight_layout()
    path = output_dir / "ratio_distribution.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    created.append(path)
    return created
