---
slug: blog_3
title: The quiet parts of an ML system
meta_description: "A tour of the unglamorous components that make production ML systems work: feature stores, data contracts, and monitoring."
description: Feature stores, data contracts, monitoring, and the unglamorous pieces that decide whether a model survives in production.
pill: Systems · ML in production
published: "2023"
read_time: "~8 min read"
topics: Production ML, reliability
toc:
  - id: feature-definitions
    label: Feature definitions you can read and trust
  - id: data-contracts
    label: Data contracts and change management
  - id: monitoring
    label: Monitoring more than just the score
---

Most diagrams of ML systems are dominated by the model box: a big rectangle labeled "XGBoost" or "Transformer" with arrows going in and out. The rest of the boxes are left as an exercise for the reader.

In practice, the "other boxes" decide how reliable the system feels: how often it breaks, how easy it is to debug, and how painful it is to change.

## Feature definitions you can read and trust {#feature-definitions}

A feature store is less about fancy infrastructure and more about shared, versioned definitions. When a feature has a single, well-documented definition, you get fewer "wait, which version of active_days did you use?" conversations.

## Data contracts and change management {#data-contracts}

ML systems are downstream of everything. That means upstream schema changes, backfills, or pipeline outages can silently poison your models if you don't have clear contracts and monitoring in place.

## Monitoring more than just the score {#monitoring}

It's tempting to monitor only top-line metrics and model scores. In practice, some of the most actionable alerts are about data shape and drift: which segments are over- or under-represented, which features are drifting fastest, where latency is creeping up.

None of this is glamorous, but it's the difference between a demo and a system the rest of the organization can rely on.
