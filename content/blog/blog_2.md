---
slug: blog_2
title: Designing experiments you can actually believe
meta_description: Practical notes on designing experiments in messy products, from guardrails to pre-registration.
description: "Lessons from running experiments in messy products: guardrails, pre-registration, and why celebrated uplift often misleads."
pill: Experiments · Causality
published: "2024"
read_time: "~10 min read"
topics: Experiment design, causal inference
toc:
  - id: write-the-decision-memo
    label: Write the decision memo first
  - id: guardrails-and-pre-registration
    label: Guardrails and pre-registration
  - id: make-trade-offs-explicit
    label: Make trade-offs explicit
---

Most teams don't suffer from a lack of experiments; they suffer from experiments that are hard to interpret. Weeks of work lead to a slide that says "looks promising, but we're not sure".

This note collects a few patterns I've found helpful when designing experiments that lead to decisions instead of debates.

## Write the decision memo first {#write-the-decision-memo}

Before launching, write a short paragraph that future you could paste into a decision memo: what you'll do if the experiment wins, loses, or is inconclusive. If you can't fill that in, something about the design or the metric probably needs more work.

## Guardrails and pre-registration {#guardrails-and-pre-registration}

Pre-registration doesn't need to be heavy. A simple checklist of primary metric, guardrails, sample size, and stopping rules is often enough to avoid the worst garden-of-forking-paths problems.

Treat guardrails as part of the success criteria: "we'll ship if the primary metric improves by X and complaint rate, churn, and latency stay within these bands".

## Make trade-offs explicit {#make-trade-offs-explicit}

In real products, you rarely get a free lunch. A good experiment write-up should call out the expected trade-offs in plain language: who might be worse off, and by how much, even if the primary metric improves.

The goal isn't a perfect experiment. It's a design that lets your team make a clear, honest decision with the data you have.

I'm always interested in better ways to bring causal thinking into day-to-day product work. If you have war stories or questions here, I'd love to hear them.
