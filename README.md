# NIST-CommunityResilience
Community Resilience using NLP

This project supports an academic research collaboration led through Johns Hopkins University and Michigan State University with guidance from researchers working with the Community Resilience program in the Engineering Laboratory at the National Institute of Standards and Technology (NIST). The effort is focused on helping communities better understand how resilience planning is discussed, documented, and implemented in practice across municipalities in the United States.
Rather than serving as a consulting project for a single private-sector organization, the work is intended to produce methods and insights that can help inform broader resilience-planning guidance. The community partner team is especially interested in practical evidence about how local governments frame resilience priorities, identify barriers to action, and communicate tradeoffs in public-facing documents.


# Project Overview
Extreme weather events, seismic activity, and wildfires increasingly threaten U.S. communities. A major
challenge for resilience research is not just analyzing documents once, but building a repeatable process for
finding, collecting, and updating relevant municipal materials over time.
The main goal of this project is to create a reproducible workflow that starts with a list of URLs, pulls
out resilience-related text and metadata, and stores the results in a structured, reusable dataset. Students
should begin by adapting the existing repositories UScityURL and UniScraper, which were developed by a
former MSU graduate student, then focus on making the pipeline easy to rerun, extend, and maintain as
new sources are added.
Once that workflow is working, the team can use the resulting dataset to explore how municipalities talk
about resilience, what topics appear most often, and which documents are most useful for downstream NLP
analysis. The workflow itself is the primary deliverable; the dataset and research findings are important, but
secondary to building a process that others can reliably update.

### Research Questions
• How can we build a reproducible workflow that starts from municipal URLs and produces a structured,
updateable resilience-text dataset?
• What metadata and document structure are needed to make the resulting dataset easy to query, refresh,
and extend?
• After the dataset is built, what initial patterns appear in how municipalities describe resilience goals,
risks, and planning priorities?
