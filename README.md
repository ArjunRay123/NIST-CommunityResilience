# NIST Community Resilience

### Community Resilience Analysis Using NLP

This project supports an academic research collaboration involving **Johns Hopkins University**, **Michigan State University**, and researchers associated with the **Community Resilience Program at the National Institute of Standards and Technology (NIST)**.

The project focuses on understanding how resilience planning is discussed, documented, and implemented by municipalities across the United States. Rather than studying a single organization or community, the goal is to develop methods and tools that can support broader research on community resilience and inform future resilience-planning guidance.

A particular focus is placed on how local governments describe resilience priorities, identify risks and barriers, and communicate planning decisions and tradeoffs through publicly available documents.

## Project Overview

Communities across the United States face increasing risks from hazards such as extreme weather events, wildfires, floods, and earthquakes. Understanding how municipalities prepare for and respond to these risks requires analyzing a large and continually changing collection of public planning documents.

The primary goal of this project is to develop a reproducible and maintainable data pipeline that collects resilience-related information from municipal websites and converts it into a structured dataset suitable for Natural Language Processing (NLP) analysis.

The workflow begins with a collection of municipal URLs and is designed to:

- Retrieve documents and web content from municipal sources.
- Extract resilience-related text and relevant metadata.
- Store the extracted information in a structured and reusable dataset.
- Support repeated runs so that new or updated documents can be incorporated over time.
- Prepare the collected text for downstream NLP and resilience research.

Once the data-collection pipeline is established, the resulting dataset can be used to investigate how municipalities discuss resilience, identify common themes and priorities, and determine which types of documents are most useful for further NLP analysis.

The **reproducible workflow is the primary project deliverable**. The resulting dataset and initial research findings are important secondary outcomes.

## Research Questions

The project is guided by three main research questions:

1. **How can we build a reproducible workflow that starts with municipal URLs and produces a structured, updateable dataset of resilience-related text?**

2. **What metadata and document structure are necessary to make the dataset easy to search, maintain, refresh, and extend?**

3. **What initial patterns can be identified in how municipalities describe resilience goals, risks, barriers, and planning priorities?**

## Goal

The overall goal is to create a scalable and reusable foundation for collecting, organizing, and analyzing municipal resilience documents using NLP methods.
