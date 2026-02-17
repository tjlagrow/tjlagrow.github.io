---
layout: post
title: "Beyond Static Connectivity: The Role of Quasi-Periodic Patterns in Alzheimer's"
date: 2025-01-15 09:00:00 -0500
categories: research neuroscience
thumbnail: /assets/images/static_dynamic_header.png
tags: [fMRI, QPP, Alzheimer's, dynamics]
description: "How dynamic spatiotemporal patterns (QPPs) outperform static functional connectivity in classifying Alzheimer's disease pathology in mouse models."
---

![Static vs Dynamic Connectivity](/assets/images/static_dynamic_header.png)

Functional connectivity (FC) has long been the gold standard for understanding how different brain regions communicate. In thousands of papers, researchers scan a brain for 10 minutes, calculate the average correlation between every pair of regions, and produce a "connectome."

However, this approach suffers from a fundamental limitation: it assumes these connections are **static** over the course of scan. It collapses the rich, time-varying movie of brain activity into a single, frozen photograph.

My research in the MIND Lab challenges this assumption. By looking at **Quasi-Periodic Patterns (QPPs)**—recurring spatiotemporal events that drive much of the brain's functional architecture—we are finding that the *dynamics* of the brain break down long before the static structure does.

## The "Static" Limitation

Imagine trying to understand a symphony orchestra by looking at a long-exposure photograph taken over the entire concert.
*   You would see that the violins sit near the cellos (topology).
*   You would see that the percussion section is generally loud (amplitude).
*   But you would miss the music itself. You wouldn't know if they were playing Beethoven or Mozart. You wouldn't hear the tempo changes or the call-and-response between sections.

Traditional static FC is that long-exposure photograph. In neurodegenerative diseases like Alzheimer's, the "music"—the *timing* of neural communication—often falls out of sync long before the structural "wiring" physically disintegrates.

## Study Design: TG2576 Mouse Model

In our recent work, we utilized resting-state fMRI (rsfMRI) to examine these dynamics in **TG2576 mice**.
*   **The Model:** TG2576 is a well-established mouse model of amyloid pathology. These mice overexpress a mutant form of the human amyloid precursor protein (APP), leading to plaque deposition similar to human Alzheimer's.
*   **The Method:** Instead of just correlating regions, we used a pattern-finding algorithm to identify **QPPs**—repeating templates of brain-wide activity that last about 3 to 6 seconds in mice.

## Key Findings: The "Blurring" of Networks

Our analysis revealed a striking dynamic failure in the Alzheimer's mice that static analysis largely missed.

### 1. The Breakdown of Anti-Correlation
In a healthy brain (mouse or human), the **Default Mode Network (DMN)** and the **Task-Positive Network (TPN)** are natural antagonists. When you are focused on a task (TPN on), your internal monologue suppresses (DMN off). When you daydream (DMN on), your attention to the outside world fades (TPN off).
*   **Healthy Controls:** We observed robust QPPs where the DMN and TPN were strongly anti-correlated. They fired in a precise, alternating rhythm.
*   **TG2576 Mice:** This relationship collapsed. The DMN and TPN began to fire together, or their timing became "slushy." The sharp dynamic boundary between "internal" and "external" attention was blurred.

### 2. The "Blurring" Effect
We visualized this as a "phase portrait" of brain activity. Healthy brains traverse a wide, structured state space—moving decisively between specific network configurations. The Alzheimer's brains appeared "stuck" or "limited," unable to fully switch states. The networks were dynamically blurring together.

### 3. Superior Classification
Crucially, when we trained a classifier to distinguish healthy mice from TG2576 mice:
*   **Static FC:** Achieved moderate accuracy (~70%). The average connections were slightly weaker, but individual variability was high.
*   **Dynamic QPP Metrics:** Achieved significantly higher accuracy (>85%). By measuring the *strength* and *frequency* of these QPPs, we could detect pathology much more reliably.

## Why This Matters

This suggests that **dynamic biomarkers** could serve as reliable early warning signs.
*   **Early Detection:** If dynamic coordination fails before plaques fully take over, we might be able to detect "at-risk" brains years earlier.
*   **Mechanism:** It points to a failure of *inhibitory control*. The inability to shut down the DMN when the TPN comes online (and vice versa) suggests a breakdown in inter-neuron signaling that serves as the conductor of the orchestra.

By treating the brain as a dynamic system rather than a static graph, we can detect subtle network failures that traditional methods miss. We are moving from looking for "broken wires" to looking for "bad timing."
