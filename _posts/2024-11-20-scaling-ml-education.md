---
layout: post
title: "Scaling ML Education: Ops, Pedagogy, and Teaching 1,200 Students"
date: 2024-11-20 14:00:00 -0500
categories: education teaching
thumbnail: /assets/images/education_header.png
tags: [OMSCS, CS7641, pedagogy, scale]
description: "Strategies for running Georgia Tech's massive CS7641 course: Socratic lectures, DevOps for grading, and prioritizing analysis over code."
---

![Education at Scale](/assets/images/education_header.png)

Teaching Machine Learning at Georgia Tech's OMSCS (Online Master of Science in Computer Science) scale is not just a classroom challenge; it is a logistical and pedagogical feat that borders on distributed systems engineering.

In **CS7641 (Machine Learning)**, we host over **1,200 students per semester**. For context, a typical university lecture hall holds 50-100 students. We are teaching a population the size of a small town, distributed across every time zone on Earth, all simultaneously tackling complex problems like randomized optimization and reinforcement learning.

At this scale, the traditional "professor + grader" model collapses instantly. You cannot just "work harder." You are essentially running a mid-sized startup specialized in knowledge transfer.

To maintain rigor while scaling, we have shifted our philosophy from "Teaching" to **"Educational Systems Engineering."** Here is how we do it.

## 1. The "Why" Over the "How" (Analysis > Code)

Most introductory ML courses focus heavily on syntax: *"Here is how you import Scikit-Learn,"* or *"Here is how you call `.fit()`."*

We flip this. In the age of StackOverflow and Copilot, knowing the syntax for a Support Vector Machine is a commodity skill. Knowing *why* your SVM is overfitting or why your k-Means clustering failed on a non-convex dataset is a scarce, high-value skill.

*   **The Philosophy:** Code is a tool; insight is the product.
*   **The Implementation:** We treat coding as a prerequisite. We do not grade on whether your code runs (mostly). Our four major projects (Supervised Learning, Randomized Optimization, Unsupervised Learning, Reinforcement Learning) require **10-20 page analytical reports**.
*   **The Result:** Students don't just get a grade for hitting 90% accuracy. They can actually fail with 95% accuracy if they cannot explain *why* they got it. Conversely, a student whose model performed poorly but who wrote a brilliant analysis of the bias-variance trade-offs and hyperparameter sensitivity can earn an A. This forces students to move beyond "script kiddie" ML and become engineers.

## 2. DevOps for Education

Grading 1,200 analytical reports—each 10+ pages long—is impossible without massive structure. If you do the math, that’s 12,000+ pages of technical writing to grade every few weeks.

We solve this with a rigorous "DevOps" approach to course management:
*   **Hierarchical Staffing:** We employ 30+ TAs, organized into a military-like hierarchy.
    *   **Head TAs:** Manage the overall strategy and crisis response.
    *   **Section Leads:** Manage teams of graders and ensure calibration.
    *   **Graders:** Owners of specific subsets of students.
*   **CI/CD for Docs:** We treat assignments like software. Rubrics are version-controlled. Assignment descriptions are "patched" in real-time. We monitor student sentiment on Ed Discussion (our forum) like a server health metric. If we see a spike in confusion about "pruning methodology," we deploy a "hotfix" to the assignment FAQ within hours, not days.
*   **Automated Triage:** We use text classification to route student queries to the right subject matter expert immediately. A question about "Q-Learning convergence" is routed to the RL expert TA, not a generalist.

## 3. Socratic Delivery

Our lectures (originally designed by Charles Isbell and Michael Littman) use a unique **Socratic dialogue format**.

Instead of a "Sage on the Stage" reading slides, the videos feature two experts—a "Student" (Isbell) and a "Teacher" (Littman), who swap roles—debating a concept.
*   They interrupt each other.
*   They make mistakes and correct them.
*   They ask "stupid" questions that turn out to be profound.

This models the *critical thinking* process we want students to emulate. It shows that Machine Learning isn't about memorizing facts; it's about reasoning through trade-offs. It teaches students *how to think about ML*, not just what the definitions are.

## 4. Generative AI as a Tutor, Not a Crutch

The rise of ChatGPT and LLMs presented a crisis for many courses. Our response was not to ban it, but to integrate it with guardrails.
*   **The Policy:** You can use LLMs to generate code (since we care about analysis). You can use it to explain concepts. You *cannot* use it to write your report prose or generate your charts.
*   **The Reality:** We found that students who over-relied on AI wrote "hallucinated" analysis. They would claim their Neural Network did X because the AI said so, even when their graphs clearly showed Y.
*   **The Lesson:** We now teach students to treat AI like a junior intern: useful for grunt work, but dangerous if you don't verify its output. This is a critical skill for the modern workforce.

Scaling education isn't just about recording videos; it's about building a robust delivery infrastructure that makes high-quality feedback possible at scale. It transforms the role of the TA from "grader" to "mentor" and "debugger of ideas."
