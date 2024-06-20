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
```
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
```

<Documents> 
{documents}
</Documents>

"""
