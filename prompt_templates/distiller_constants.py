DEFAULT_TEMPLATE =   """
<Role>You are provided with several definitions of Responsible AI. Your task is to synthesize these definitions to create a new, consensus-driven definition of Responsible AI. Additionally, you should identify and list the key similarities that form the basis of this consensus definition, as well as the main points of disagreement or variations among the definitions.</Role>

<Task>
1. Read and Analyze Definitions: Carefully read through each provided definition of Responsible AI.

2. Identify Key Similarities: Determine the core principles, values, and components that are common across all or most of the definitions. List these similarities clearly.

3. Identify Key Disagreements/Variations: Highlight the main differences or unique elements in the definitions. List these variations clearly.

4. Synthesize a Consensus Definition: Using the commonalities identified, create a new, cohesive definition of Responsible AI that reflects a consensus among the provided definitions. Ensure this new definition is clear, concise, and incorporates the key shared elements.

5. Document Findings: Provide a summary that includes:

- The new, consensus-driven definition of Responsible AI.
- A list of key similarities found in the definitions.
- A list of key disagreements or variations found in the definitions.</Task>

Output Format:
Consensus Definition:

[Your synthesized definition here]
Key Similarities:

Similarity 1: [Description]
Similarity 2: [Description]
Similarity 3: [Description]
...
Key Disagreements/Variations:

Variation 1: [Description]
Variation 2: [Description]
Variation 3: [Description]
...

<Definitions> 
{documents}
</Definitions>

"""

KEYWORD_DEFINITION_TEMPLATE =   """
<Role>You are provided with several definitions of the same keyword. Your task is to synthesize these definitions to create a new, consensus-driven definition of "{keyword}". Additionally, you should identify and list the key similarities that form the basis of this consensus definition, as well as the main points of disagreement or variations among the definitions.</Role>

<Task>
Identify Common Themes: Look for common themes, keywords, and concepts that appear across multiple definitions. Highlight or underline these commonalities.

Note Unique Contributions: Identify any unique aspects or additional insights provided by each definition. These might add depth to the final definition.

Synthesize Information: Combine the common themes and unique contributions into a single, coherent definition. Ensure that each sentence adds a specific piece of information.

Refine for Clarity and Conciseness: Revise the synthesized definition to ensure it is clear and concise. Remove any redundant or overly complex language.
</Task>

Output Format:
Consensus Definition:

[Your synthesized definition here]
Key Similarities:

Similarity 1: [Description]
Similarity 2: [Description]
Similarity 3: [Description]
...
Key Disagreements/Variations:

Variation 1: [Description]
Variation 2: [Description]
Variation 3: [Description]
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