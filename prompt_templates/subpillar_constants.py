DEFINITION_GENERATION_PROMPT = """
<role>
You are an expert academic researcher conducting research at a professorial and PhD level.
</role>

<task>
Given the following subpillars of Responsible AI and their definitions, create a holistic and interdependent definition of Responsible AI that emphasizes the importance of each subpillar according to their prominence in the literature. Highlight the relationships between these subpillars. Following the overall Responsible AI definition, provide detailed, nuanced, concise, and clear definitions for each subpillar. Explain the significance of each subpillar and why it was chosen. Your ouptut should be one paragraph written in formal academic language. 
</task>

The subpillars of Responsible AI are:
{keywords}

Definitions of each subpillar:
{definitions}
"""
