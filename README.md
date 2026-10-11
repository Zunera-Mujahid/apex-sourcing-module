# apex-sourcing-module
NLP-based CV and Job Description matching system

### Semantic Score Policy

The semantic score is used for reporting and supporting evidence only. It is not included in the candidate's final score.

The final score uses the following criteria:

- Technical skills: 55%
- Experience: 25%
- Education: 10%
- Soft skills: 10%

When a scoring component is unavailable, the available criteria are renormalized according to the implemented scoring logic.

Semantic similarity does not independently establish that a candidate possesses a required skill or meets an education requirement. Keeping semantic score separate preserves the defined scoring policy.