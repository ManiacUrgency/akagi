DEFAULT_TEMPLATE = """
<Role>
You are provided with 61 definitions of the same keyword. Your task is to synthesize these definitions into a new, consensus-driven definition of "{keyword}". Identify key similarities and disagreements, and emphasize the prominence of the keyword in the literature.
</Role>

<Task>
Create a one-paragraph definition of the keyword in the following steps:
1. Identify Common Themes: Highlight common themes, keywords, and concepts.
2. Note Unique Contributions: Include unique aspects from each definition.
3. Synthesize Information: Combine common themes and unique contributions into a coherent definition.
4. Emphasize Prominence: Indicate the prominence of the keyword in the literature.
5. Refine for Clarity: Ensure the definition is clear and concise, removing redundant or complex language.
</Task>

Output Format:
Consensus Definition (one paragraph):

[Your synthesized definition here]

Common Themes:
- [Theme 1]
- [Theme 2]
- [Theme 3]

Unique Contributions:
- [Unique Contribution 1]
- [Unique Contribution 2]
- [Unique Contribution 3]

Prominence:
- [Has this keyword been significantly mentioned in research?]

Key Similarities:
- Similarity 1: [Description]
- Similarity 2: [Description]
- Similarity 3: [Description]
...

Key Disagreements/Variations:
- Variation 1: [Description]
- Variation 2: [Description]
- Variation 3: [Description]
...

<Definitions>
{documents}
</Definitions>
"""

KEYWORD_TEMPLATE = """
Extract the keywords related to the definition of "Responsible AI" from the following paragraph. Focus on terms that relate to principles, attributes, or components of Responsible AI. Your output should be a list of keywords in comma-separated values (CSV) format.

Output format: 
[keyword1], [keyword2], [keyword3], ...

<< Example Number 1. >>
Query:
The author defines "Responsible AI" as AI systems designed to uphold human values through ethical principles and societal concerns, characterized by the ART principles: Accountability, Responsibility, and Transparency. Accountability involves explaining and justifying decisions clearly, facilitated by algorithms that allow derivation of decisions from moral and societal norms. Responsibility encompasses the capability of AI systems to recognize and address errors and unexpected outcomes, linking AI decisions to fair data use and stakeholder actions. Transparency necessitates the ability to describe, inspect, and replicate the decision-making mechanisms and data governance processes, particularly in an era where current AI algorithms are often opaque. Overall, Responsible AI is viewed as a multidimensional approach, fundamental to intelligence, requiring educational efforts, legal frameworks, and active participation from society to ensure its ethical deployment and impact.

Response:
accountability, responsibility, transparency, ethical

<Definitions> 
{documents}
</Definitions>

"""

