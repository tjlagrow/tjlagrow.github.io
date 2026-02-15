---
layout: post
title: "Scaling ML Education: Ops, Pedagogy, and Teaching 1,200 Students"
date: 2024-11-20 14:00:00 -0500
categories: education teaching
tags: [OMSCS, CS7641, pedagogy, scale]
description: "Strategies for running Georgia Tech's massive CS7641 course: Socratic lectures, DevOps for grading, and prioritizing analysis over code."
---

Teaching Machine Learning at Georgia Tech's OMSCS scale is a logistical and pedagogical feat. In **CS7641 (Machine Learning)**, we host over 1,200 students per semester. At this scale, the traditional "professor + grader" model collapses. You are essentially running a mid-sized startup specialized in knowledge transfer.

To maintain rigor while scaling, we have shifted our philosophy from "Teaching" to **"Educational Systems Engineering."**

### 1. The "Why" Over the "How" (Analysis > Code)
Many ML courses focus on syntax: *"Here is how you import Scikit-Learn."* We flip this.
*   **The Philosophy:** Code is a commodity; insight is scarce.
*   **The Implementation:** We treat coding as a prerequisite tool, not the learning objective. Our four major projects (Supervised, Randomized Optimization, Unsupervised, RL) require 10-20 page analytical reports. 
*   **The Result:** Students don't just get a grade for hitting 90% accuracy; they get graded on *explaining why* their decision tree overfitted or why k-means failed on a specific dataset.

### 2. DevOps for Education
Grading 1,200 analytical reports is impossible without massive structure.
*   **Staffing:** We employ 30+ TAs, organized into a hierarchy of Head TAs and Section Leads.
*   **CI/CD for Docs:** We treat assignments like software. Rubrics are version-controlled. Assignment descriptions are "patched" in real-time based on student confusion (measured via Ed Discussion sentiment).
*   **Automated Triage:** We use tooling to route student queries to the right subject matter expert immediately, minimizing latency.

### 3. Socratic Delivery
Our lectures (originally by Isbell & Littman) use a Socratic dialogue format. Instead of a monologue, two experts debate a concept. This models the *critical thinking* process we want students to emulate. It shows that ML isn't about memorizing facts, but about reasoning through trade-offs.

### 4. Generative AI as a Tutor, Not a Crutch
We are actively researching how to integrate GenAI. We encourage students to use AI for coding (since we care about analysis), but we are building guardrails to ensure they use it to *accelerate* learning, not bypass it.

Scaling education isn't just about recording videos; it's about building a robust delivery infrastructure that makes high-quality feedback possible at scale.
