import json
import os
import matplotlib.pyplot as plt
import numpy as np

# Metric names for plotting (order matches data indices 1..4)
METRIC_NAMES = ["Hallucination", "Incompleteness", "Consistency", "Correctness"]
PATH, H, INC, CON, COR, SOUND = 0, 1, 2, 3, 4, 5


def load_results(json_path):
    """Load zero_shot.json or in_context_learning.json into a dict."""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def flatten_files_by_llm(results):
    """
    For each LLM, flatten all files across prompts into one list of entries.
    Each entry is (path, H, Inc, Con, Cor, Soundness) as in the JSON.
    """
    by_llm = {}
    for llm, prompt_lists in results.items():
        files = []
        for prompt_files in prompt_lists:
            for entry in prompt_files:
                files.append(entry)  # [path, H, I, C, Cor, Soundness]
        by_llm[llm] = files
    return by_llm


def best_mid_worst(entries):
    """
    Rank entries by Soundness (index 5), return (best, mid, worst).
    Each is [path, H, Inc, Con, Cor, Soundness].
    """
    if not entries:
        return None, None, None
    sorted_entries = sorted(entries, key=lambda e: e[SOUND])
    n = len(sorted_entries)
    best = sorted_entries[-1]
    worst = sorted_entries[0]
    mid_idx = n // 2
    mid = sorted_entries[mid_idx]
    return best, mid, worst


def plot_llm_best_mid_worst(ax, llm_name, best, mid, worst, title_suffix=""):
    """
    Bar chart: X = HICC categories, Y = score. Three bars per category (best, mid, worst).
    """
    x = np.arange(len(METRIC_NAMES))
    width = 0.25

    def vals(entry):
        return [entry[H], entry[INC], entry[CON], entry[COR]]

    bars1 = ax.bar(x - width, vals(best), width, label="Best (by soundness)", color="green", alpha=0.8)
    bars2 = ax.bar(x, vals(mid), width, label="Middle", color="gray", alpha=0.8)
    bars3 = ax.bar(x + width, vals(worst), width, label="Worst", color="red", alpha=0.8)

    ax.set_ylabel("Score (higher = better)")
    ax.set_title(f"{llm_name} {title_suffix}".strip())
    ax.set_xticks(x)
    ax.set_xticklabels(METRIC_NAMES)
    ax.legend(loc="lower right", fontsize=8)
    ax.set_ylim(0, 1.05)
    ax.axhline(1.0, color="black", linewidth=0.5, linestyle="--", alpha=0.5)


def plot_best_worst_llm_max_per_metric(ax, llm_name, files_for_max_each_metric):
    """
    For one LLM: we have 4 "champion" files (file with max H, max I, max C, max Cor).
    Plot each champion's scores across all 4 metrics (so 4 series).
    files_for_max_each_metric: list of 4 entries [path, H, I, C, Cor, Soundness]
    in order: champion for H, for I, for C, for Cor.
    """
    x = np.arange(len(METRIC_NAMES))
    width = 0.2

    # Legend: file that had the max score for that metric (shown across all 4 metrics)
    labels = ["Max Hallucination", "Max Incompleteness", "Max Consistency", "Max Correctness"]
    colors = ["#2ecc71", "#3498db", "#9b59b6", "#e74c3c"]

    for i, (entry, label) in enumerate(zip(files_for_max_each_metric, labels)):
        vals = [entry[H], entry[INC], entry[CON], entry[COR]]
        offset = (i - 1.5) * width
        ax.bar(x + offset, vals, width, label=label, color=colors[i], alpha=0.85)

    ax.set_ylabel("Score (higher = better)")
    # Subplot title: just the LLM; context (metric + 0-shot vs in-context) is in the figure suptitle
    ax.set_title(llm_name)
    ax.set_xticks(x)
    ax.set_xticklabels(METRIC_NAMES)
    ax.legend(loc="lower right", fontsize=7)
    ax.set_ylim(0, 1.05)


def get_all_files_flat(results):
    """One list of all (llm, entry) for ranking LLMs by mean soundness."""
    out = []
    for llm, prompt_lists in results.items():
        for prompt_files in prompt_lists:
            for entry in prompt_files:
                out.append((llm, entry))
    return out


def llm_mean_soundness(flattened_by_llm):
    """Return dict llm -> mean soundness (across all its files)."""
    return {
        llm: np.mean([e[SOUND] for e in entries])
        for llm, entries in flattened_by_llm.items()
        if entries
    }


def get_champion_files_per_metric(entries):
    """
    From a list of file entries, return 4 entries: the file that has max H, max I, max C, max Cor.
    Return: [entry_max_H, entry_max_I, entry_max_C, entry_max_Cor]
    """
    if not entries:
        return [None] * 4
    entry_max_H = max(entries, key=lambda e: e[H])
    entry_max_I = max(entries, key=lambda e: e[INC])
    entry_max_C = max(entries, key=lambda e: e[CON])
    entry_max_Cor = max(entries, key=lambda e: e[COR])
    return [entry_max_H, entry_max_I, entry_max_C, entry_max_Cor]


def run_zero_shot():
    json_path = "zero_shot.json"
    if not os.path.exists(json_path):
        print(f"Missing {json_path}")
        return
    results = load_results(json_path)
    run_charts(results, "zero_shot", "Zero-shot (no docs)")


def run_in_context():
    json_path = "in_context_learning.json"
    if not os.path.exists(json_path):
        print(f"Missing {json_path}")
        return
    results = load_results(json_path)
    run_charts(results, "in_context_learning", "In-context learning (with docs)")


def run_charts(results, prefix, title_suffix):
    flattened = flatten_files_by_llm(results)

    # ----- Chart type 1: Per-LLM best / mid / worst -----
    llms = sorted(flattened.keys())
    # print(llms)
    #Hotfix due to my mistake
    n_llms = len(llms)
    n_cols = 2
    n_rows = (n_llms + n_cols - 1) // n_cols
    fig1, axes1 = plt.subplots(n_rows, n_cols, figsize=(6 * n_cols, 4 * n_rows))
    if n_llms == 1:
        axes1 = np.array([axes1])
    axes1 = axes1.flatten()

    for idx, llm in enumerate(llms):
        entries = flattened[llm]
        best, mid, worst = best_mid_worst(entries)
        ax = axes1[idx]
        if best is not None:
            plot_llm_best_mid_worst(ax, llm, best, mid, worst, title_suffix)
        else:
            ax.set_title(f"{llm} (no data)")
    for j in range(n_llms, len(axes1)):
        axes1[j].set_visible(False)

    fig1.suptitle(f"Best / Middle / Worst file by soundness — {title_suffix}", fontsize=12, y=1.02)
    fig1.tight_layout()
    out1 = f"{prefix}_best_mid_worst_by_llm.png"
    fig1.savefig(out1, dpi=150, bbox_inches="tight")
    print(f"Saved {out1}")
    plt.close(fig1)

    # ----- Chart type 2: Best and worst LLM — file max in each metric -----
    mean_sound = llm_mean_soundness(flattened)
    if not mean_sound:
        return
    sorted_llms = sorted(mean_sound.keys(), key=lambda m: mean_sound[m])
    best_llm = sorted_llms[-1]
    worst_llm = sorted_llms[0]

    fig2, (ax_best, ax_worst) = plt.subplots(1, 2, figsize=(12, 5))

    champions_best = get_champion_files_per_metric(flattened[best_llm])
    champions_worst = get_champion_files_per_metric(flattened[worst_llm])

    plot_best_worst_llm_max_per_metric(ax_best, f"Best LLM: {best_llm}", champions_best)
    plot_best_worst_llm_max_per_metric(ax_worst, f"Worst LLM: {worst_llm}", champions_worst)

    fig2.suptitle(f"File with max in each HICC metric — {title_suffix}", fontsize=12, y=1.02)
    fig2.tight_layout()
    out2 = f"{prefix}_best_worst_llm_max_per_metric.png"
    fig2.savefig(out2, dpi=150, bbox_inches="tight")
    print(f"Saved {out2}")
    plt.close(fig2)


if __name__ == "__main__":
    run_zero_shot()
    run_in_context()
    print("Done.")
