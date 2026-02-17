---
layout: post
title: "Cross-Species Functional Connectivity: The Translational Bridge"
date: 2024-09-10 10:00:00 -0400
categories: research neuroscience
thumbnail: /assets/images/cross_species_header.png
tags: [fMRI, translational, mice, human]
description: "Mapping homologous brain networks between rodents and humans to improve translational drug discovery."
---

![Cross Species Brain Networks](/assets/images/cross_species_header.png)

One of the most persistent failures in modern neuroscience—sometimes called the "Valley of Death"—is the Translation Gap. We often cure diseases in mice, identifying promising compounds that reverse Alzheimer's plaques or restore cognitive function in water mazes, only for those same treatments to fail catastrophically in human clinical trials.

The failure rate for Alzheimer’s drugs entering clinical trials is reportedly over 99%. Why?

A major culprit is the implicit assumption of a 1:1 mapping between mouse and human brain networks that doesn't fully exist. We model a complex human network disease (like the disintegration of the Default Mode Network in AD) in a species where the existence of that network is still debated.

My compilation, **"Functional Connectivity of the Brain Across Rodents and Humans"** (LaGrow, Xu, et al., *Frontiers in Neuroscience* 2022), addresses this by systematically mapping the homologous functional networks across species. We argue that to cross the Valley of Death, we need a better bridge—one built on functional homology, not just structural convenience.

## The "Rosetta Stone" of fMRI

To build this bridge, we utilized high-field fMRI. While human scanning is standard at 3 Tesla (or 7T for high-res work), rodent imaging requires significantly higher field strengths—typically 9.4T or 11.7T—to achieve sufficient signal-to-noise ratios in a brain weighing less than a gram.

By comparing resting-state connectivity (rs-fMRI) side-by-side, we essentially created a "Rosetta Stone" for brain networks. We asked: *For every major human resting-state network (RSN), what is the rodent equivalent?*

The answer is complex. Some networks map cleanly; others are unrecognizable.

---

## Key Homologies & Divergences

### 1. The Default Mode Network (DMN): The "Ghost" in the Machine
The DMN is the most studied network in humans—active when we are daydreaming, retrieving memories, or thinking about "self." It is also the first to go in Alzheimer's.

*   **In Humans:** The DMN is robust, dominated by the Posterior Cingulate Cortex (PCC), Precuneus, and Medial Prefrontal Cortex (mPFC). It is the structural core of the cortex.
*   **In Rodents:** For years, skeptics argued mice didn't *have* a DMN. Our review highlights that a "proto-DMN" does exist, anchored in the Anterior Cingulate and Retrosplenial Cortex. However, it looks different. It lacks the massive Prefrontal expansion seen in humans, and its coupling strength is weaker. It's less "dominant" than in humans.
    
**Why this matters:** If a drug targets the DMN in a mouse model, but the mouse DMN relies on different receptor distributions or connectivity hubs than the human version, we are targeting a phantom.

### 2. The Global Signal: Noise or Nuance?
*   **In Humans:** The Global Signal (GS)—the average activity across the whole brain—is often regressed out as "noise" (breathing, heart rate, motion).
*   **In Rodents:** In mice, the GS is huge. It often dominates the signal. Our work suggests this isn't just noise; it contains significant neural information related to arousal and vascular dynamics. Treating it as noise in mice can mathematically remove the very signal of interest (especially in models of vascular dementia or hypertension).

---

## The Dynamic Solution: Quasi-Periodic Patterns (QPPs)

Perhaps the most exciting finding in our review is that *static* connectivity (correlating Region A to Region B over 10 minutes) might be the wrong metric for translation.

Instead, we looked at dynamics. **Quasi-Periodic Patterns (QPPs)** are recurring waves of electrical and blood-oxygen activity that roll across the brain like a weather system.

Despite the structural differences between a smooth mouse brain (lissencephalic) and a folded human brain (gyrencephalic), the **QPPs are remarkably conserved**. In both species, we see an infraslow propagation of activity moving from lateral (sensory) regions to medial (default-mode) regions.

This suggests that this "lateral-to-medial" wave is a fundamental principle of mammalian brain organization, preserved across 70 million years of evolution. It is a more robust translational target than any single static connection.

## The Anesthesia Confounder

A critical section of our review deals with the "Elephant in the MRI Scanner": Anesthesia.
*   Humans are scanned awake and thinking.
*   Mice are almost always scanned under anesthesia (Isoflurane or Medetomidine) to keep them still.

Anesthesia fundamentally alters the firing rates and coupling of neurons. We found that the choice of anesthetic can completely flip network correlations. For example, Medetomidine preserves certain networks but suppresses the Global Signal; Isoflurane induces bursting patterns that can mimic pathology.

We argue that true translation requires awake mouse imaging (which requires extensive training) or careful accounting for these anesthetic states.

## Implications for Drug Discovery

Understanding these distinctions is vital. If we want to test an Alzheimer's drug, we shouldn't just look for "memory improvement" in a mouse. We should look for the *repair of the specific functional network dynamics* that we know are broken in humans.

Our framework provides a "lookup table" to help researchers contextualize rodent fMRI findings. It allows us to say: *"Okay, this drug restored the Prefrontal-Hippocampal coupling in the mouse. In humans, that coupling corresponds to the pathway used for episodic memory retrieval, so this is a valid target."*

Without this map, we are just guessing.

**Read the full review:** [Frontiers in Neuroscience (2022)](https://www.frontiersin.org/articles/10.3389/fnins.2022.816331/full)
