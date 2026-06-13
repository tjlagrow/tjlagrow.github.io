import os
import numpy as np
import matplotlib.pyplot as plt
from rag_utils import IMAGE_OUT_DIR

def generate_expanded_plots(results):
    print("\nCompiling premium Matplotlib benchmark charts...")
    
    # Modern design token settings
    plt.rcParams['figure.facecolor'] = '#f8fafc'  # Slate-50 background
    plt.rcParams['axes.facecolor'] = '#ffffff'
    plt.rcParams['axes.edgecolor'] = '#cbd5e1'   # Slate-300 borders
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.color'] = '#f1f5f9'        # Slate-100 grid lines
    plt.rcParams['grid.linestyle'] = '-'
    plt.rcParams['grid.linewidth'] = 0.8
    
    # Typography configuration
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Inter', 'DejaVu Sans', 'Arial', 'Helvetica']
    plt.rcParams['text.color'] = '#0f172a'        # Slate-900 text
    plt.rcParams['axes.labelcolor'] = '#334155'   # Slate-700 labels
    plt.rcParams['xtick.color'] = '#64748b'       # Slate-500 ticks
    plt.rcParams['ytick.color'] = '#64748b'
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['axes.titlepad'] = 12
    
    # Legend styling
    plt.rcParams['legend.frameon'] = True
    plt.rcParams['legend.framealpha'] = 0.95
    plt.rcParams['legend.facecolor'] = '#ffffff'
    plt.rcParams['legend.edgecolor'] = '#e2e8f0'
    plt.rcParams['legend.fontsize'] = 9

    # Colors definition
    PRIMARY = "#4f46e5"    # Indigo
    SECONDARY = "#06b6d4"  # Cyan
    ACCENT_ROSE = "#f43f5e" # Rose
    ACCENT_AMBER = "#f59e0b" # Amber
    ACCENT_EMERALD = "#10b981" # Emerald
    ACCENT_PURPLE = "#8b5cf6"  # Violet
    ACCENT_PINK = "#ec4899"    # Pink

    def style_axes(ax, title, xlabel=None, ylabel=None, show_legend=True):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#cbd5e1')
        ax.spines['bottom'].set_color('#cbd5e1')
        ax.set_title(title, fontweight='bold', pad=12)
        if xlabel:
            ax.set_xlabel(xlabel, labelpad=6)
        if ylabel:
            ax.set_ylabel(ylabel, labelpad=6)
        ax.set_axisbelow(True)
        if show_legend and ax.get_legend_handles_labels()[0]:
            legend = ax.legend(frameon=True, facecolor='#ffffff', edgecolor='#e2e8f0', fontsize=8)
            legend.get_frame().set_linewidth(0.8)

    # 1. Chunking Ratio Recall (Phase 1)
    p1 = results.get("Phase 1: Retrieval Parameters", {})
    ratios_keys = ["chunk_Ratio A (Child 30 / Parent 150)", "chunk_Ratio B (Child 50 / Parent 200)", "chunk_Ratio C (Child 100 / Parent 500)"]
    if all(k in p1 for k in ratios_keys):
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = ["Ratio A\n(30/150 words)", "Ratio B\n(50/200 words)", "Ratio C\n(100/500 words)"]
        hit3_vals = [p1[k]["hit_at_3"] for k in ratios_keys]
        mrr_vals = [p1[k]["mrr"] for k in ratios_keys]
        
        x = np.arange(len(labels))
        width = 0.3
        
        ax.bar(x - width/2, hit3_vals, width, label="Recall@3", color=PRIMARY, alpha=0.9)
        ax.bar(x + width/2, mrr_vals, width, label="MRR", color=SECONDARY, alpha=0.9)
        
        style_axes(ax, "Hierarchical Chunk Ratios: Search Performance", ylabel="Retrieval Score")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylim(0, 1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "chunk_ratio_recall.png"), dpi=150)
        plt.close()
        
    # 2. Parameter Trade-offs (Phase 1 K and cutoffs)
    k_keys = [f"ret_K_{k}" for k in [2, 3, 5, 8]]
    if all(k in p1 for k in k_keys):
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = ["K=2", "K=3", "K=5", "K=8"]
        hit3_vals = [p1[k]["hit_at_3"] for k in k_keys]
        mrr_vals = [p1[k]["mrr"] for k in k_keys]
        
        ax.plot(labels, hit3_vals, marker='o', linewidth=2.5, color=SECONDARY, label="Recall@3",
                markerfacecolor=SECONDARY, markeredgecolor='white', markeredgewidth=1.5, markersize=8)
        ax.plot(labels, mrr_vals, marker='s', linewidth=2.5, color=ACCENT_AMBER, label="MRR",
                markerfacecolor=ACCENT_AMBER, markeredgecolor='white', markeredgewidth=1.5, markersize=8)
        
        style_axes(ax, "Retrieval Cutoff (K) Parameter Trade-offs", ylabel="Score")
        ax.set_ylim(min(mrr_vals) * 0.95, 1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "parameter_tradeoffs.png"), dpi=150)
        plt.close()

    # 3. Quantization recall impact
    quant_keys = ["quant_float32", "quant_int8", "quant_binary"]
    if all(k in p1 for k in quant_keys):
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = ["Float32 (Full)", "Int8 (Quantized)", "Binary (1-Bit)"]
        hit3_vals = [p1[k]["hit_at_3"] for k in quant_keys]
        mrr_vals = [p1[k]["mrr"] for k in quant_keys]
        
        x = np.arange(len(labels))
        width = 0.3
        ax.bar(x - width/2, hit3_vals, width, label="Recall@3", color=ACCENT_ROSE, alpha=0.9)
        ax.bar(x + width/2, mrr_vals, width, label="MRR", color="#fb923c", alpha=0.9)
        
        style_axes(ax, "Vector Index Quantization Search Quality", ylabel="Performance Score")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylim(0, 1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "quantization_impact.png"), dpi=150)
        plt.close()

    # 4. Local Generator Comparison (Phase 2)
    p2 = results.get("Phase 2: Generator Model Comparison", {})
    if p2:
        models = [m for m in p2.keys() if not m.startswith("Decoding:") and not m.startswith("Repetition Penalty:")]
        if models:
            fig, ax = plt.subplots(figsize=(8, 5))
            rouge_vals = [p2[m]["rouge_l"] for m in models]
            sim_vals = [p2[m]["semantic_similarity"] for m in models]
            
            x = np.arange(len(models))
            width = 0.3
            ax.bar(x - width/2, rouge_vals, width, label="ROUGE-L Overlap", color=PRIMARY, alpha=0.9)
            ax.bar(x + width/2, sim_vals, width, label="Semantic Similarity", color=SECONDARY, alpha=0.9)
            
            style_axes(ax, "Generator Performance: ROUGE-L vs. Semantic Similarity", ylabel="Score")
            ax.set_xticks(x)
            ax.set_xticklabels(models, rotation=15)
            ax.set_ylim(0, 1.05)
            plt.tight_layout()
            plt.savefig(os.path.join(IMAGE_OUT_DIR, "generation_comparison.png"), dpi=150)
            plt.close()

            # 4b. Local Generator Integrity & Diversity Comparison
            if any("lexical_diversity_ttr" in p2[m] for m in models):
                fig, ax = plt.subplots(figsize=(8, 5))
                ttr_vals = [p2[m].get("lexical_diversity_ttr", 0.0) for m in models]
                ground_vals = [p2[m].get("groundedness", 0.0) for m in models]
                
                ax.bar(x - width/2, ttr_vals, width, label="Lexical Diversity (TTR)", color=ACCENT_PINK, alpha=0.9)
                ax.bar(x + width/2, ground_vals, width, label="Groundedness (Context Reference)", color=ACCENT_AMBER, alpha=0.9)
                
                style_axes(ax, "Generator Integrity: Lexical TTR vs. Groundedness", ylabel="Score")
                ax.set_xticks(x)
                ax.set_xticklabels(models, rotation=15)
                ax.set_ylim(0, 1.05)
                plt.tight_layout()
                plt.savefig(os.path.join(IMAGE_OUT_DIR, "generation_integrity.png"), dpi=150)
                plt.close()

            # 22. Latency vs. Quality Pareto Frontier
            fig, ax = plt.subplots(figsize=(7, 5))
            latencies = [p2[m]["latency_sec"] for m in models]
            groundedness_vals = [p2[m]["groundedness"] for m in models]
            colors_list = [PRIMARY, SECONDARY, ACCENT_ROSE, ACCENT_AMBER, ACCENT_PURPLE][:len(models)]
            sizes = [150, 220, 290, 360, 430][:len(models)]
            
            ax.scatter(latencies, groundedness_vals, s=sizes, c=colors_list, alpha=0.85, edgecolors='#334155', linewidth=1.2)
            for i, txt in enumerate(models):
                ax.annotate(txt, (latencies[i], groundedness_vals[i]), xytext=(8, -3), textcoords='offset points', fontweight='bold', fontsize=8, color='#0f172a')
                
            style_axes(ax, "Pareto Frontier: Generation Latency vs. Groundedness", "Average Latency (seconds, log scale)", "Groundedness Score", show_legend=False)
            ax.set_ylim(-0.05, 1.05)
            ax.set_xscale('log')
            ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%.2fs'))
            plt.tight_layout()
            plt.savefig(os.path.join(IMAGE_OUT_DIR, "latency_vs_recall.png"), dpi=150)
            plt.close()

            # 23. All-metrics Heatmap Matrix
            metrics_labels = ["ROUGE-L", "Semantic Cos.", "Groundedness", "Faithfulness", "Refusal Adher."]
            matrix_data = []
            for m in models:
                matrix_data.append([
                    p2[m].get("rouge_l", 0.0),
                    p2[m].get("semantic_similarity", 0.0),
                    p2[m].get("groundedness", 0.0),
                    p2[m].get("judge_faithfulness", 0.0),
                    p2[m].get("refusal_adherence", 0.0)
                ])
            matrix_data = np.array(matrix_data)
            
            fig, ax = plt.subplots(figsize=(8, 5))
            im = ax.imshow(matrix_data, cmap="YlGnBu", aspect="auto", vmin=0, vmax=1)
            
            ax.set_xticks(np.arange(len(metrics_labels)))
            ax.set_yticks(np.arange(len(models)))
            ax.set_xticklabels(metrics_labels)
            ax.set_yticklabels(models)
            plt.setp(ax.get_xticklabels(), rotation=25, ha="right", rotation_mode="anchor")
            
            for i in range(len(models)):
                for j in range(len(metrics_labels)):
                    val = matrix_data[i, j]
                    txt_color = "white" if val > 0.6 else "#0f172a"
                    ax.text(j, i, f"{val:.2f}", ha="center", va="center", color=txt_color, fontweight='bold', fontsize=9)
            
            cbar = ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
            cbar.ax.tick_params(labelsize=8)
            cbar.outline.set_visible(False)
            
            style_axes(ax, "Generator Comprehensive Metrics Heatmap Matrix", show_legend=False)
            ax.grid(False)
            plt.tight_layout()
            plt.savefig(os.path.join(IMAGE_OUT_DIR, "metrics_comparison.png"), dpi=150)
            plt.close()

    # 5. Persona Adherence & Few-Shot Anchoring (Phase 3)
    p3 = results.get("Phase 3: Persona & Few-Shot Adherence", {})
    if p3:
        fig, ax = plt.subplots(figsize=(9, 5))
        shots = list(range(11))
        x_ticks = [f"{s}-sh" for s in shots]
        
        persona_configs = [
            ("helpful", PRIMARY),
            ("sassy", ACCENT_ROSE),
            ("pirate", SECONDARY),
            ("cynical_redditor", ACCENT_PURPLE)
        ]
        
        for persona, color in persona_configs:
            if persona in p3:
                conformance = [p3[persona][f"shot_{s}"]["json_conformance"] for s in shots]
                style_dens = [p3[persona][f"shot_{s}"]["style_density"] for s in shots]
                p_label = persona.replace("_", " ").title()
                
                ax.plot(x_ticks, conformance, linestyle="-", marker="o", color=color, label=f"{p_label} JSON Conformance",
                        markerfacecolor=color, markeredgecolor='white', markeredgewidth=1.2, markersize=6)
                ax.plot(x_ticks, style_dens, linestyle="--", marker="s", color=color, label=f"{p_label} Style Density",
                        markerfacecolor='white', markeredgecolor=color, markeredgewidth=1.2, markersize=5)
                
        style_axes(ax, "Few-Shot Style Anchoring vs. JSON Conformance Curve", xlabel="Shot Count Examples")
        ax.set_ylim(-0.05, 1.15)
        ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True, fontsize=8)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "persona_adherence.png"), dpi=150)
        plt.close()

    # 6. Few-shot Trade-offs (Phase 3 Groundedness & Length)
    if p3 and any("groundedness" in p3[persona].get("shot_0", {}) for persona in p3):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
        shots = list(range(11))
        x_ticks = [f"{s}-sh" for s in shots]
        
        for persona, color in [("helpful", PRIMARY), ("sassy", ACCENT_ROSE), ("pirate", SECONDARY), ("cynical_redditor", ACCENT_PURPLE)]:
            if persona in p3:
                ground_vals = [p3[persona][f"shot_{s}"].get("groundedness", 0.0) for s in shots]
                len_vals = [p3[persona][f"shot_{s}"].get("length", 0.0) for s in shots]
                p_label = persona.replace("_", " ").title()
                
                ax1.plot(x_ticks, ground_vals, marker="o", color=color, label=p_label,
                         markerfacecolor=color, markeredgecolor='white', markeredgewidth=1.2, markersize=6)
                ax2.plot(x_ticks, len_vals, marker="s", color=color, label=p_label,
                         markerfacecolor=color, markeredgecolor='white', markeredgewidth=1.2, markersize=6)
                
        style_axes(ax1, "Answer Groundedness vs. Shot Count", xlabel="Shot Count")
        ax1.set_ylim(-0.05, 1.05)
        
        style_axes(ax2, "Answer Length vs. Shot Count", xlabel="Shot Count", ylabel="Characters")
        
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "fewshot_tradeoffs.png"), dpi=150)
        plt.close()

    # 7. Data Construction Formats (Phase 4)
    p4 = results.get("Phase 4: Data Construction and Accessibility", {})
    format_keys = ["Format: Raw Text", "Format: XML Tagged", "Format: JSON Array"]
    if all(k in p4 for k in format_keys):
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = ["Raw Text", "XML Tagged", "JSON Array"]
        faith_vals = [p4[k]["judge_faithfulness"] for k in format_keys]
        ground_vals = [p4[k]["groundedness"] for k in format_keys]
        cite_vals = [p4[k]["citation_fidelity"] for k in format_keys]
        
        x = np.arange(len(labels))
        width = 0.22
        ax.bar(x - width, faith_vals, width, label="Judge Faithfulness", color=PRIMARY, alpha=0.9)
        ax.bar(x, ground_vals, width, label="Groundedness", color=SECONDARY, alpha=0.9)
        ax.bar(x + width, cite_vals, width, label="Citation Fidelity", color=ACCENT_PURPLE, alpha=0.9)
        
        style_axes(ax, "Context Formatting Ingestion Structure Impact", ylabel="Evaluation Score")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylim(0, 1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "data_construction_formats.png"), dpi=150)
        plt.close()

    # 8. Lost in the Middle Ordering (Phase 4)
    ordering_keys = ["Ordering: First (Best)", "Ordering: Middle", "Ordering: Last"]
    if all(k in p4 for k in ordering_keys):
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = ["First (Primacy)", "Middle (Center)", "Last (Recency)"]
        faith_vals = [p4[k]["judge_faithfulness"] for k in ordering_keys]
        rel_vals = [p4[k]["judge_relevance"] for k in ordering_keys]
        
        ax.plot(labels, faith_vals, marker='o', linewidth=2.5, color=ACCENT_ROSE, label="Judge Faithfulness",
                markerfacecolor=ACCENT_ROSE, markeredgecolor='white', markeredgewidth=1.5, markersize=8)
        ax.plot(labels, rel_vals, marker='s', linewidth=2.5, color=ACCENT_AMBER, label="Judge Relevance",
                markerfacecolor=ACCENT_AMBER, markeredgecolor='white', markeredgewidth=1.5, markersize=8)
        
        style_axes(ax, "Lost-in-the-Middle: Document Position Impact", ylabel="Evaluation Score")
        ax.set_ylim(min(faith_vals + rel_vals) * 0.9, 1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "lost_in_the_middle_ordering.png"), dpi=150)
        plt.close()

    # 9. Metadata Enrichment Impact (Phase 4)
    metadata_keys = ["Metadata: Rich (Enriched)", "Metadata: None (Raw Text)"]
    if all(k in p4 for k in metadata_keys):
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = ["Metadata Rich", "No Metadata"]
        faith_vals = [p4[k]["judge_faithfulness"] for k in metadata_keys]
        ground_vals = [p4[k]["groundedness"] for k in metadata_keys]
        cite_vals = [p4[k]["citation_fidelity"] for k in metadata_keys]
        
        x = np.arange(len(labels))
        width = 0.22
        ax.bar(x - width, faith_vals, width, label="Judge Faithfulness", color=PRIMARY, alpha=0.9)
        ax.bar(x, ground_vals, width, label="Groundedness", color=SECONDARY, alpha=0.9)
        ax.bar(x + width, cite_vals, width, label="Citation Fidelity", color=ACCENT_PURPLE, alpha=0.9)
        
        style_axes(ax, "Metadata Enrichment on Grounded Fact Extraction", ylabel="Score")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylim(0, 1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "metadata_enrichment_impact.png"), dpi=150)
        plt.close()

    # 10. Prompt Instruction Impact (Phase 5)
    p5 = results.get("Phase 5: Prompt Engineering and Context Robustness", {})
    prompt_keys = ["System: Strict Refusal", "System: Sycophantic", "System: Default"]
    if all(k in p5 for k in prompt_keys):
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = ["Strict Refusal", "Sycophantic", "Default/Persona"]
        faith_vals = [p5[k]["judge_faithfulness"] for k in prompt_keys]
        refusal_vals = [p5[k]["refusal_adherence"] for k in prompt_keys]
        halluc_vals = [p5[k]["hallucination_ratio"] for k in prompt_keys]
        
        x = np.arange(len(labels))
        width = 0.22
        ax.bar(x - width, faith_vals, width, label="Judge Faithfulness", color=SECONDARY, alpha=0.9)
        ax.bar(x, refusal_vals, width, label="Refusal Adherence", color=ACCENT_EMERALD, alpha=0.9)
        ax.bar(x + width, halluc_vals, width, label="Hallucination Ratio", color=ACCENT_ROSE, alpha=0.9)
        
        style_axes(ax, "System Prompt Framing (im_start message) Impact", ylabel="Scores")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylim(0, 1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "prompt_instruction_impact.png"), dpi=150)
        plt.close()

    # 11. Context Volume Impact (Phase 5)
    volume_keys = ["Volume: 1 Snippet", "Volume: 4 Snippets (Default)", "Volume: 12 Snippets"]
    if all(k in p5 for k in volume_keys):
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = ["1 Snippet", "4 Snippets", "12 Snippets"]
        faith_vals = [p5[k]["judge_faithfulness"] for k in volume_keys]
        halluc_vals = [p5[k]["hallucination_ratio"] for k in volume_keys]
        
        ax.plot(labels, faith_vals, marker='o', linewidth=2.5, color=ACCENT_PURPLE, label="Judge Faithfulness",
                markerfacecolor=ACCENT_PURPLE, markeredgecolor='white', markeredgewidth=1.5, markersize=8)
        ax.plot(labels, halluc_vals, marker='s', linewidth=2.5, color=ACCENT_AMBER, label="Hallucination Ratio",
                markerfacecolor=ACCENT_AMBER, markeredgecolor='white', markeredgewidth=1.5, markersize=8)
        
        style_axes(ax, "Context Volume Scaling: Recall vs. Hallucination", ylabel="Score")
        ax.set_ylim(-0.05, 1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "context_volume_impact.png"), dpi=150)
        plt.close()

    # 12. Adversarial Distractor Robustness (Phase 5)
    distractor_keys = ["Robustness: Normal", "Robustness: Distractor Injected"]
    if all(k in p5 for k in distractor_keys):
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = ["Normal Context", "Distractor Injected"]
        refusal_vals = [p5[k]["refusal_adherence"] for k in distractor_keys]
        faith_vals = [p5[k]["judge_faithfulness"] for k in distractor_keys]
        halluc_vals = [p5[k]["hallucination_ratio"] for k in distractor_keys]
        
        x = np.arange(len(labels))
        width = 0.22
        ax.bar(x - width, faith_vals, width, label="Judge Faithfulness", color=SECONDARY, alpha=0.9)
        ax.bar(x, refusal_vals, width, label="Refusal Adherence", color=ACCENT_EMERALD, alpha=0.9)
        ax.bar(x + width, halluc_vals, width, label="Hallucination Ratio", color=ACCENT_ROSE, alpha=0.9)
        
        style_axes(ax, "Adversarial Noise: Distractor Snippet Robustness", ylabel="Score")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylim(0, 1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "adversarial_distractor_robustness.png"), dpi=150)
        plt.close()

    # 13. RRF Tuning Sweep (Phase 1)
    rrf_const_keys = [f"rrf_const_{c}" for c in [10, 30, 60, 100, 150]]
    if all(k in p1 for k in rrf_const_keys):
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = ["C=10", "C=30", "C=60", "C=100", "C=150"]
        hit3_vals = [p1[k]["hit_at_3"] for k in rrf_const_keys]
        mrr_vals = [p1[k]["mrr"] for k in rrf_const_keys]
        
        ax.plot(labels, hit3_vals, marker='o', linewidth=2.5, color=ACCENT_AMBER, label="Recall@3",
                markerfacecolor=ACCENT_AMBER, markeredgecolor='white', markeredgewidth=1.5, markersize=8)
        ax.plot(labels, mrr_vals, marker='s', linewidth=2.5, color=ACCENT_EMERALD, label="MRR",
                markerfacecolor=ACCENT_EMERALD, markeredgecolor='white', markeredgewidth=1.5, markersize=8)
        
        style_axes(ax, "Reciprocal Rank Fusion (RRF) Constant Optimization", ylabel="Score")
        ax.set_ylim(min(mrr_vals) * 0.95, 1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "rrf_parameter_tuning.png"), dpi=150)
        plt.close()

    # 14. Decoding Strategy and Repetition Sweeps (Phase 2)
    dec_keys = ["Decoding: Greedy", "Decoding: Top-P (temp=0.7, p=0.9)", "Decoding: Top-K (temp=0.7, k=40)"]
    rep_keys = [f"Repetition Penalty: {p}" for p in ["1.0", "1.05", "1.1", "1.15", "1.2", "1.25"]]
    if all(k in p2 for k in dec_keys) and all(k in p2 for k in rep_keys):
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = ["Greedy", "Top-P (Nucleus)", "Top-K"]
        struct_vals = [p2[k]["structure_fidelity"] for k in dec_keys]
        ttr_vals = [p2[k]["lexical_diversity_ttr"] for k in dec_keys]
        
        x = np.arange(len(labels))
        width = 0.3
        ax.bar(x - width/2, struct_vals, width, label="Structure Compliance", color=PRIMARY, alpha=0.9)
        ax.bar(x + width/2, ttr_vals, width, label="Lexical Diversity (TTR)", color=ACCENT_PINK, alpha=0.9)
        
        style_axes(ax, "Decoding Strategy Impact on Formatting & Diversity", ylabel="Score")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylim(0, 1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "decoding_strategy_impact.png"), dpi=150)
        plt.close()
        
        fig, ax = plt.subplots(figsize=(7, 5))
        rep_labels = ["1.00 (None)", "1.05", "1.10", "1.15", "1.20", "1.25"]
        rep_ttrs = [p2[k]["lexical_diversity_ttr"] for k in rep_keys]
        rep_structs = [p2[k]["structure_fidelity"] for k in rep_keys]
        
        ax.plot(rep_labels, rep_ttrs, marker='o', linewidth=2.5, color=ACCENT_PINK, label="Lexical TTR",
                markerfacecolor=ACCENT_PINK, markeredgecolor='white', markeredgewidth=1.5, markersize=8)
        ax.plot(rep_labels, rep_structs, marker='s', linewidth=2.5, color=PRIMARY, label="JSON Conformance",
                markerfacecolor=PRIMARY, markeredgecolor='white', markeredgewidth=1.5, markersize=8)
        
        ax.axvline(x=2, color=ACCENT_AMBER, linestyle=':', linewidth=1.5, alpha=0.8)
        ax.text(2.1, 0.8, "Sweet Spot (1.10)", color=ACCENT_AMBER, fontweight='bold', fontsize=8)
        
        style_axes(ax, "Repetition Penalty Sweeps (SmolLM2-360M)", ylabel="Score")
        ax.set_ylim(-0.05, 1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "repetition_penalty_sweeps.png"), dpi=150)
        plt.close()

    # 15. Rerank Cutoff Sweeps (Phase 4)
    cutoff_keys = ["Rerank Cutoff: 2", "Rerank Cutoff: 4 (Default)", "Rerank Cutoff: 6", "Rerank Cutoff: 8", "Rerank Cutoff: 12"]
    if all(k in p4 for k in cutoff_keys):
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = ["Cutoff=2", "Cutoff=4", "Cutoff=6", "Cutoff=8", "Cutoff=12"]
        faith_vals = [p4[k]["judge_faithfulness"] for k in cutoff_keys]
        ground_vals = [p4[k]["groundedness"] for k in cutoff_keys]
        
        ax.plot(labels, faith_vals, marker='o', linewidth=2.5, color="#14b8a6", label="Judge Faithfulness",
                markerfacecolor="#14b8a6", markeredgecolor='white', markeredgewidth=1.5, markersize=8)
        ax.plot(labels, ground_vals, marker='s', linewidth=2.5, color=ACCENT_PURPLE, label="Groundedness",
                markerfacecolor=ACCENT_PURPLE, markeredgecolor='white', markeredgewidth=1.5, markersize=8)
        
        style_axes(ax, "Reranker Sentence Selection Limit Impact", ylabel="Score")
        ax.set_ylim(-0.05, 1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "reranker_cutoff_impact.png"), dpi=150)
        plt.close()

    # 16. Ingestion Style Comparison (Phase 4)
    ingest_keys = ["Ingestion: Parent Paragraph Chunks", "Ingestion: Sentence-level Snippets (Default)"]
    if all(k in p4 for k in ingest_keys):
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = ["Parent Paragraphs\n(Hierarchical)", "Sentence Snippets\n(Sentence-level)"]
        faith_vals = [p4[k]["judge_faithfulness"] for k in ingest_keys]
        ground_vals = [p4[k]["groundedness"] for k in ingest_keys]
        
        x = np.arange(len(labels))
        width = 0.3
        ax.bar(x - width/2, faith_vals, width, label="Judge Faithfulness", color=ACCENT_ROSE, alpha=0.9)
        ax.bar(x + width/2, ground_vals, width, label="Groundedness", color=SECONDARY, alpha=0.9)
        
        style_axes(ax, "Ingestion Chunking Style RAG Performance", ylabel="Score")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylim(0, 1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "parent_vs_child_ingestion.png"), dpi=150)
        plt.close()

    # 17. Multi-Distractor Density sweeps (Phase 5)
    dist_density_keys = ["Robustness: 0 Distractors", "Robustness: 1 Distractor", "Robustness: 2 Distractors", "Robustness: 4 Distractors", "Robustness: 8 Distractors"]
    if all(k in p5 for k in dist_density_keys):
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = ["0 Dist.", "1 Dist.", "2 Dist.", "4 Dist.", "8 Dist."]
        faith_vals = [p5[k]["judge_faithfulness"] for k in dist_density_keys]
        ground_vals = [p5[k]["groundedness"] for k in dist_density_keys]
        halluc_vals = [p5[k]["hallucination_ratio"] for k in dist_density_keys]
        
        ax.plot(labels, faith_vals, marker='o', linewidth=2.5, color=ACCENT_EMERALD, label="Judge Faithfulness",
                markerfacecolor=ACCENT_EMERALD, markeredgecolor='white', markeredgewidth=1.5, markersize=8)
        ax.plot(labels, ground_vals, marker='s', linewidth=2.5, color=PRIMARY, label="Groundedness",
                markerfacecolor=PRIMARY, markeredgecolor='white', markeredgewidth=1.5, markersize=8)
        ax.plot(labels, halluc_vals, marker='^', linewidth=2.5, color=ACCENT_ROSE, label="Hallucination Ratio",
                markerfacecolor=ACCENT_ROSE, markeredgecolor='white', markeredgewidth=1.5, markersize=8)
        
        ax.axvline(x=3, color=ACCENT_ROSE, linestyle=':', linewidth=1.5, alpha=0.6)
        ax.text(3.1, 0.9, "Attention Distraction Threshold", color=ACCENT_ROSE, fontsize=8, fontweight='bold')
        
        style_axes(ax, "Attention Distraction: Model Robustness vs. Noise Density", ylabel="Score")
        ax.set_ylim(-0.05, 1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "distractor_density_threshold.png"), dpi=150)
        plt.close()

    # 18. Adversarial Jailbreak Adherence (Phase 5)
    jailbreak_keys = ["Robustness: Normal", "Robustness: Jailbreak Attack"]
    if all(k in p5 for k in jailbreak_keys):
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = ["Normal Query", "Jailbreak Attack"]
        refusal_vals = [p5[k]["refusal_adherence"] for k in jailbreak_keys]
        faith_vals = [p5[k]["judge_faithfulness"] for k in jailbreak_keys]
        
        x = np.arange(len(labels))
        width = 0.3
        ax.bar(x - width/2, refusal_vals, width, label="Refusal Adherence", color=ACCENT_PURPLE, alpha=0.9)
        ax.bar(x + width/2, faith_vals, width, label="Judge Faithfulness", color=ACCENT_AMBER, alpha=0.9)
        
        style_axes(ax, "Jailbreak Vulnerability: Safety Refusal Adherence", ylabel="Score")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylim(0, 1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "jailbreak_refusal_adherence.png"), dpi=150)
        plt.close()

    # 19. Attention Token Stress tests (Phase 5)
    stress_keys = [f"Attention Stress: {t} tokens" for t in [512, 1024, 2048, 4096]]
    if all(k in p5 for k in stress_keys):
        fig, ax = plt.subplots(figsize=(7, 5))
        labels = ["512 Tokens", "1024 Tokens", "2048 Tokens", "4096 Tokens"]
        faith_vals = [p5[k]["judge_faithfulness"] for k in stress_keys]
        ground_vals = [p5[k]["groundedness"] for k in stress_keys]
        
        ax.plot(labels, faith_vals, marker='o', linewidth=2.5, color=ACCENT_EMERALD, label="Judge Faithfulness",
                markerfacecolor=ACCENT_EMERALD, markeredgecolor='white', markeredgewidth=1.5, markersize=8)
        ax.plot(labels, ground_vals, marker='s', linewidth=2.5, color=ACCENT_AMBER, label="Groundedness",
                markerfacecolor=ACCENT_AMBER, markeredgecolor='white', markeredgewidth=1.5, markersize=8)
        
        style_axes(ax, "Attention Stress Test: Context Expansion Window Impact", ylabel="Score")
        ax.set_ylim(-0.05, 1.05)
        plt.tight_layout()
        plt.savefig(os.path.join(IMAGE_OUT_DIR, "attention_stress_token_limit.png"), dpi=150)
        plt.close()

    print("Matplotlib premium figure compilation complete. Saved plots in assets/images/ablation/.")
