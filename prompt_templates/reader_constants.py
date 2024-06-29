DEFAULT_TEMPLATE = """
    Task:
    Please analyze the following text from 61 research papers and identify the top 6 most significant sub-pillars (keywords) that collectively define "Responsible AI." The sub-pillars should be determined based on their significance in the literature context provided. These sub-pillars will be definied as keywords such as privacy, accountability, fairness, etc. Make sure you only refer to the context provided to identify the sub-pillars.Return the sub-pillars in CSV format.

    <<Example Output>>
    ```
    Fairness, Transparency, Accountability, Reliability, Privacy, Inclusiveness
    ```

    Context:
    ```{text}```
    """

KEYWORD_DEFINITION_TEMPLATE = """
    Below is a passage from a research paper. Identify and define the keyword {term} within the context of this passage. Provide 2-3 sentence paragraph defintion that is detailed, clear, and concise based on the author's definition of the term in the given text. If the author does not give a definitin, doesn't mention the keyword, or gives a very unclear definition please state that.

    Text:
    {text}

    Only return the definition.

    """



