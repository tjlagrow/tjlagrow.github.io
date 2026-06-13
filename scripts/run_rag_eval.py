#!/usr/bin/env python3
import os
import sys
import json
import numpy as np
import math

# Add scripts folder to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag_utils import (
    PROJECT_ROOT, EMBEDDINGS_FILE, QUERIES_FILE, SimpleBM25,
    calculate_groundedness, calculate_citation_fidelity,
    calculate_hallucination_ratio, calculate_retrieval_metrics,
    preprocess_query
)

def main():
    print("=" * 60)
    print(" Waddles RAG Retrieval Evaluation System")
    print("=" * 60)
    
    # 1. Load Embeddings
    if not os.path.exists(EMBEDDINGS_FILE):
        print(f"Error: Vector database not found at {EMBEDDINGS_FILE}. Please run generate_embeddings.py first.")
        sys.exit(1)
        
    print(f"Loading vector database from {EMBEDDINGS_FILE}...")
    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
        vdb = json.load(f)
        
    embeddings_data = vdb["embeddings"]
    print(f"Loaded {len(embeddings_data)} database chunks.")
    
    # 2. Load Evaluation Queries
    if not os.path.exists(QUERIES_FILE):
        print(f"Error: Query database not found at {QUERIES_FILE}.")
        sys.exit(1)
        
    print(f"Loading evaluation queries from {QUERIES_FILE}...")
    with open(QUERIES_FILE, "r", encoding="utf-8") as f:
        queries = json.load(f)
    print(f"Loaded {len(queries)} evaluation queries.")
    
    # 3. Setup Indexers
    corpus = [node["text"] for node in embeddings_data]
    doc_embeddings = np.array([node["embedding"] for node in embeddings_data])
    bm25 = SimpleBM25(corpus)
    
    # Load embedding model
    print("Loading SentenceTransformer model ('all-MiniLM-L6-v2')...")
    from sentence_transformers import SentenceTransformer
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # 4. Run Evaluations
    intent_metrics = {}
    overall_retrieval = {
        "hit_at_3": [],
        "hit_at_5": [],
        "mrr": [],
        "ndcg": []
    }
    overall_generation = {
        "groundedness": [],
        "citation_fidelity": [],
        "hallucination_ratio": []
    }
    
    print("\nRunning evaluation sweeps across queries...")
    
    for idx, q_item in enumerate(queries):
        query_text = q_item["query"]
        intent = q_item["intent"]
        gt_titles = q_item.get("ground_truth_document_titles", [])
        gt_answer = q_item.get("ground_truth_answer", "")
        
        # Preprocess query
        clean_q = preprocess_query(query_text)
        
        # Retrieval: Hybrid Search (50% Dense, 50% Sparse)
        q_emb = embed_model.encode(clean_q, show_progress_bar=False)
        dense_scores = np.dot(doc_embeddings, q_emb)
        
        # Normalize scores
        dense_norm = (dense_scores - np.min(dense_scores)) / max((np.max(dense_scores) - np.min(dense_scores)), 1e-8)
        sparse_scores = bm25.get_scores(clean_q)
        sparse_norm = (sparse_scores - np.min(sparse_scores)) / max((np.max(sparse_scores) - np.min(sparse_scores)), 1e-8)
        
        hybrid_scores = 0.5 * dense_norm + 0.5 * sparse_norm
        top_indices = np.argsort(hybrid_scores)[::-1][:5]
        
        retrieved_nodes = [embeddings_data[i] for i in top_indices]
        retrieved_titles = [node["title"] for node in retrieved_nodes]
        retrieved_contexts = " ".join([node["text"] for node in retrieved_nodes])
        
        # Calculate retrieval metrics
        hit_3, hit_5, mrr, ndcg = calculate_retrieval_metrics(retrieved_titles, gt_titles, top_k=5)
        
        overall_retrieval["hit_at_3"].append(hit_3)
        overall_retrieval["hit_at_5"].append(hit_5)
        overall_retrieval["mrr"].append(mrr)
        overall_retrieval["ndcg"].append(ndcg)
        
        # Lexical heuristics for Groundedness & Citations using ground truth answers
        if gt_answer:
            groundedness = calculate_groundedness(gt_answer, retrieved_contexts)
            citation_fid = calculate_citation_fidelity(gt_answer, retrieved_contexts)
            halluc_ratio = calculate_hallucination_ratio(gt_answer, retrieved_contexts, clean_q)
            
            overall_generation["groundedness"].append(groundedness)
            overall_generation["citation_fidelity"].append(citation_fid)
            overall_generation["hallucination_ratio"].append(halluc_ratio)
        else:
            groundedness, citation_fid, halluc_ratio = 1.0, 1.0, 0.0
            
        # Group by Intent
        if intent not in intent_metrics:
            intent_metrics[intent] = {
                "count": 0, "hit_at_3": [], "hit_at_5": [],
                "mrr": [], "ndcg": [], "groundedness": []
            }
            
        intent_metrics[intent]["count"] += 1
        intent_metrics[intent]["hit_at_3"].append(hit_3)
        intent_metrics[intent]["hit_at_5"].append(hit_5)
        intent_metrics[intent]["mrr"].append(mrr)
        intent_metrics[intent]["ndcg"].append(ndcg)
        intent_metrics[intent]["groundedness"].append(groundedness)
        
    # Compile summary statistics
    summary_report = {
        "overall": {
            "total_queries": len(queries),
            "mean_hit_at_3": float(np.mean(overall_retrieval["hit_at_3"])),
            "mean_hit_at_5": float(np.mean(overall_retrieval["hit_at_5"])),
            "mean_mrr": float(np.mean(overall_retrieval["mrr"])),
            "mean_ndcg": float(np.mean(overall_retrieval["ndcg"])),
            "mean_groundedness": float(np.mean(overall_generation["groundedness"])) if overall_generation["groundedness"] else 1.0,
            "mean_citation_fidelity": float(np.mean(overall_generation["citation_fidelity"])) if overall_generation["citation_fidelity"] else 1.0,
            "mean_hallucination_ratio": float(np.mean(overall_generation["hallucination_ratio"])) if overall_generation["hallucination_ratio"] else 0.0
        },
        "by_intent": {}
    }
    
    for intent, metrics in intent_metrics.items():
        summary_report["by_intent"][intent] = {
            "count": metrics["count"],
            "hit_at_3": float(np.mean(metrics["hit_at_3"])),
            "hit_at_5": float(np.mean(metrics["hit_at_5"])),
            "mrr": float(np.mean(metrics["mrr"])),
            "ndcg": float(np.mean(metrics["ndcg"])),
            "groundedness": float(np.mean(metrics["groundedness"]))
        }
        
    # Write report to file
    report_file = os.path.join(PROJECT_ROOT, "artifacts", "rag_evaluation_report.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(summary_report, f, indent=2)
        
    # Print Markdown Summary table
    print("\n" + "=" * 60)
    print(" RAG EVALUATION SUMMARY REPORT")
    print("=" * 60)
    print(f"Total Queries Evaluated: {summary_report['overall']['total_queries']}")
    print(f"Mean Hit@3:            {summary_report['overall']['mean_hit_at_3']:.4f}")
    print(f"Mean Hit@5:            {summary_report['overall']['mean_hit_at_5']:.4f}")
    print(f"Mean MRR:              {summary_report['overall']['mean_mrr']:.4f}")
    print(f"Mean NDCG@5:           {summary_report['overall']['mean_ndcg']:.4f}")
    print(f"Mean Groundedness:     {summary_report['overall']['mean_groundedness']:.4f}")
    print(f"Mean Citation Fidelity: {summary_report['overall']['mean_citation_fidelity']:.4f}")
    print("-" * 60)
    print(f"{'Intent Category':<18} | {'Count':<5} | {'Hit@5':<6} | {'MRR':<6} | {'NDCG@5':<6} | {'Grounded':<8}")
    print("-" * 60)
    for intent, data in summary_report["by_intent"].items():
        print(f"{intent:<18} | {data['count']:<5} | {data['hit_at_5']:.3f} | {data['mrr']:.3f} | {data['ndcg']:.3f} | {data['groundedness']:.3f}")
    print("=" * 60)
    print(f"Saved JSON report to: {report_file}\n")

if __name__ == "__main__":
    main()
