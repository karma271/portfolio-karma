---
slug: blog_1
title: When your metric fights your product
meta_description: A short field guide to noticing when your optimization metric is misaligned with the real outcomes you care about.
description: A field guide to noticing when an optimization metric is quietly misaligned with the real outcome you care about.
pill: Evaluation · Practice
published: "2025"
read_time: "~7 min read"
topics: Evaluation, product thinking
toc:
  - id: start-from-the-decision
    label: Start from the decision, not the model
  - id: guardrails-as-first-class
    label: Guardrails as first-class citizens
  - id: tell-the-story
    label: Tell the story in plain language
---

Many ML projects start with a metric and end with a dashboard. In between, we ship a model that does better on the metric and assume that must be good for the product. Sometimes that works. Sometimes the metric quietly fights the thing we actually care about.

This note is about the second case: how to recognize misaligned metrics early, and a few simple patterns I use to keep evaluation and product goals in the same rough direction.

## Start from the decision, not the model {#start-from-the-decision}

A useful question to ask at the beginning of any project is: *what decision changes if this model is good?* If you can't answer that clearly, you're probably at risk of optimizing the wrong thing.

Once the decision is clear, work backwards: what offline metric is a reasonable stand-in for that decision? What are the obvious ways it could fail? What guardrail metrics would catch those failures before users do?

## Guardrails as first-class citizens {#guardrails-as-first-class}

It's common to treat guardrails as an afterthought: we'll add them to the dashboard later, once we know the main metric is moving. In practice, I've found it more reliable to treat guardrails as co-equal with the primary metric from the start.

For example, if you're optimizing click-through, you might care just as much about long-term engagement, complaint rates, or some measure of perceived quality. Put those metrics in the same table as your primary win metric; they're part of the story, not a footnote.

## Tell the story in plain language {#tell-the-story}

Finally, make sure someone can explain the evaluation story without looking at a single chart. What changed, for whom, and how sure are we? If that story sounds off, the metric probably is too.

The goal isn't a perfect metric. It's a metric that is honest about what it captures, and a team that can recognize when the metric and the product are starting to pull in different directions.

If you'd like a deeper dive into this topic, I'm always happy to walk through real examples (wins and failures) in more detail.
