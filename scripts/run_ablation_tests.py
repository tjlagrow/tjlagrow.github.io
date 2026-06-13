#!/usr/bin/env python3
import os
import sys
import json
import argparse
import numpy as np

# Add scripts folder to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag_utils import (
    CHECKPOINT_FILE, RESULTS_FILE, QUERIES_FILE, EMBEDDINGS_FILE,
    PERSONA_EXAMPLES, get_system_specs, SimpleBM25, run_dynamic_rechunking
)
from plot_generator import generate_expanded_plots
from ablation_phases import run_phase1, run_phase2, run_phase3, run_phase4, run_phase5

def main():
    parser = argparse.ArgumentParser(description="Waddles RAG Ablation Benchmarking Pipeline (Modular Edition)")
    parser.add_argument("--phase", type=str, default="all", choices=["1", "2", "3", "4", "5", "all"],
                        help="Run a specific ablation phase or 'all' (default: all)")
    parser.add_argument("--plot-only", action="store_true", help="Skip testing and only compile visualizations from cached checkpoint")
    parser.add_argument("--clear-checkpoint", action="store_true", help="Clear the checkpoint file and restart from scratch")
    args = parser.parse_args()

    if args.clear_checkpoint:
        if os.path.exists(CHECKPOINT_FILE):
            os.remove(CHECKPOINT_FILE)
            print(f"Cleared checkpoint file: {CHECKPOINT_FILE}")

    # Load system hardware specifications
    print("Collecting system hardware specifications...")
    specs = get_system_specs()
    print("System Hardware Specifications:")
    for k, v in specs.items():
        print(f"  {k}: {v}")

    # Load results/checkpoints
    ablation_results = {}
    if os.path.exists(CHECKPOINT_FILE):
        print(f"Resumed checkpoint. Loaded results for existing phases.")
        with open(CHECKPOINT_FILE, "r") as f:
            try:
                ablation_results = json.load(f)
            except Exception:
                ablation_results = {}
    
    # Save system specifications
    ablation_results["System Specifications"] = specs

    if args.plot_only:
        if not ablation_results:
            print("No cached checkpoint results found to plot. Run without --plot-only first.")
            sys.exit(1)
        generate_expanded_plots(ablation_results)
        sys.exit(0)

    # Initialize Embedding & Reranker Models
    print("Initializing local embedding and re-ranking models...")
    from sentence_transformers import SentenceTransformer, CrossEncoder
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    reranker_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    # Load Queries Database
    print(f"Loading query database from {QUERIES_FILE}...")
    with open(QUERIES_FILE, "r", encoding="utf-8") as f:
        queries_data = json.load(f)

    # Ingestion Flow (Default: Child 50 / Parent 200)
    db_items = run_dynamic_rechunking(200, 50, embed_model)
    doc_embeddings = np.array([node["embedding"] for node in db_items])
    
    # Setup base corpus BM25 Index
    corpus = [node["text"] for node in db_items]
    bm25 = SimpleBM25(corpus)

    # Subset of 6 queries for slow LLM benchmarks
    core_queries = [
        queries_data[0],   # Teaching in-scope
        queries_data[12],  # Research in-scope
        queries_data[30],  # Teaching/Research hybrid in-scope
        queries_data[40],  # General portfolio in-scope
        queries_data[50],  # Out-of-scope adversarial 1
        queries_data[55]   # Out-of-scope adversarial 2
    ]

    # Execute Phase 1
    if args.phase in ["1", "all"]:
        run_phase1(embed_model, doc_embeddings, db_items, bm25, queries_data, ablation_results)
        # Generate plot updates
        try: generate_expanded_plots(ablation_results)
        except Exception as e: print(f"Plot update failed: {e}")

    # Execute Phase 2
    if args.phase in ["2", "all"]:
        run_phase2(embed_model, reranker_model, db_items, doc_embeddings, core_queries, ablation_results)
        try: generate_expanded_plots(ablation_results)
        except Exception as e: print(f"Plot update failed: {e}")

    # Execute Phase 3
    if args.phase in ["3", "all"]:
        run_phase3(embed_model, reranker_model, db_items, doc_embeddings, core_queries, PERSONA_EXAMPLES, ablation_results)
        try: generate_expanded_plots(ablation_results)
        except Exception as e: print(f"Plot update failed: {e}")

    # Execute Phase 4
    if args.phase in ["4", "all"]:
        run_phase4(embed_model, reranker_model, db_items, doc_embeddings, core_queries, ablation_results)
        try: generate_expanded_plots(ablation_results)
        except Exception as e: print(f"Plot update failed: {e}")

    # Execute Phase 5
    if args.phase in ["5", "all"]:
        run_phase5(embed_model, reranker_model, db_items, doc_embeddings, core_queries, ablation_results)

    # Compile Final Results
    with open(RESULTS_FILE, "w") as f:
        json.dump(ablation_results, f, indent=2)
    print(f"\nFinal expanded results compiled and written to {RESULTS_FILE}")

    # Generate final plots
    generate_expanded_plots(ablation_results)

if __name__ == "__main__":
    main()
