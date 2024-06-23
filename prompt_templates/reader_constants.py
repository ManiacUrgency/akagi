DEFAULT_TEMPLATE = """
    Task:
    Please analyze the following text from a research paper and identify how the author defines "Responsible AI." The definition should be described through related concepts such as privacy, accountability, fairness, etc. Provide a nuanced, concise, and detailed five to six sentence summary of the author's definition of "Responsible AI." Refer to the following example output.

    <<Example Output>>
    ```
    The authors define \"Responsible AI\" through a systematic, value-driven approach emphasizing principles such as Fairness, Transparency, Accountability, Reliability and Safety, Privacy and Security, and Inclusiveness. They propose that the means to achieve Responsible AI consist of developing Socially Responsible AI Algorithms, and the objective is to enhance both AI's capabilities and its benefits to society. The framework, inspired by Carroll\u2019s Pyramid of Corporate Social Responsibility, categorizes AI responsibilities into functional, legal, ethical, and philanthropic, thereby ensuring a holistic and multidimensional perspective on AI's social responsibilities. Functional responsibilities require AI systems to perform in a manner consistent with profits maximization, operating efficiency, and other key performance indicators. Legal responsibilities require AI systems to at least meet the minimal legal requirements. Ethical responsibilities are the obligation to do what is right, just, and fair, and to prevent or mitigate negative impact on stakeholders (e.g., users, the environment). Philanthropic responsibilities, expect AI systems to be good AI citizens and to contribute to tackling societal challenges such as cancer and climate change.
    ```

    Text:
    {text}

    Only return the definition.

    """

KEYWORD_DEFINITION_TEMPLATE = """
    Below is a passage from a research paper. Identify and define the keyword {term} within the context of this passage. Provide 2-3 sentence paragraph defintion that is detailed, clear, and concise based on the author's definition of the term in the given text. If the author does not give a definitin, doesn't mention the keyword, or gives a very unclear definition please state that.

    Text:
    {text}

    Only return the definition.

    """