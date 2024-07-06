DEFAULT_CLASSIFICATION_TEMPLATE = """

    Given the following definitions of Responsible AI (RAI), classify each definition into one of the four categories and group them by the titles of the papers they belong to:

    1. **Sub-pillar Approach**: The definition breaks down RAI into specific sub-pillars (e.g., accountability, sustainability, explainability, safety, privacy, transparency, reliability, robustness). This approach focuses on defining RAI through these detailed components, whether by addressing one or multiple sub-pillars.

    2. **Framework Approach**: The definition provides a broader, more abstract framework for RAI. This approach uses umbrella terms (e.g., ethical, functional) to create an interdependent definition that considers the relationships between sub-pillars or smaller umbrella terms. An example is a pyramid scheme where the AI system progresses through stages such as functional, legal, ethical, and philanthropic.

    3. **Other**: The definition does not fit neatly into either the sub-pillar approach or the framework approach due to significant differences.

    4. **Unclear or Unrelated**: The definition is very unclear, unrelated, or there is no definition provided at all.

    For each definition, provide the classification (Sub-pillar Approach, Framework Approach, Other, Unclear or Unrelated) and a brief explanation for your decision. Group the classifications by the titles of the papers they belong to. A paper may only belong to one category and you must classify all papers.

    Example Output with placeholders:

    ```
    Category 1: Sub-pillar Approach
    1. **Title: Paper 1**
    Reason: <reason for classification>
    2. **Title: Paper 2**
    Reason: <reason for classification>
    3. **Title: Paper 3**
    Reason: <reason for classification>

    Category 2: Framework Approach
    1. **Title: Paper 1**
    Reason: <reason for classification>
    2. **Title: Paper 2**
    Reason: <reason for classification>
    3. **Title: Paper 3**
    Reason: <reason for classification>

    Category 3: Other
    1. **Title: Paper 1**
    Reason: <reason for classification>
    2. **Title: Paper 2**
    Reason: <reason for classification>
    3. **Title: Paper 3**
    Reason: <reason for classification>

    Category 4: Unclear or Unrelated
    1. **Title: Paper 1**
    Reason: <reason for classification>
    2. **Title: Paper 2**
    Reason: <reason for classification>
    3. **Title: Paper 3**
    Reason: <reason for classification>
    ```

    Here are the definitions: 
    {definitions}
"""

SUB_PILLAR_CLASSIFICATION = """
    You are tasked with performing a thematic analysis on a collection of research papers that define "Responsible AI" (RAI). Each paper breaks down RAI into specific sub-pillars, such as accountability, sustainability, explainability, safety, privacy, transparency, reliability, and robustness. Your goal is to classify these definitions into categories based on their similarities.
    Instructions:
    Read the Definitions: For each research paper, examine the definition of Responsible AI (RAI) provided.
    Identify Sub-pillars: Note which sub-pillars (e.g., accountability, sustainability, explainability, safety, privacy, transparency, reliability, robustness) are mentioned and how they are emphasized.
    Classify Definitions: Based on the patterns observed across the definitions, classify them into categories. The categories should reflect the similarities in how the definitions approach and emphasize the sub-pillars.
    If a definition focuses predominantly on one sub-pillar (e.g., privacy) while ignoring or marginalizing others, place it in a category with similar definitions.
    If a definition gives equal weight to multiple sub-pillars without emphasizing one over the others, create a category for such balanced approaches.
    Identify other meaningful patterns and create appropriate categories for them.
    Form Category Names and Descriptions: For each category, provide:
    A clear and descriptive name.
    A concise description explaining the common characteristics of the definitions in this category.
    Provide Reasons for Classification: For each paper's classification, provide a direct reason explaining why it was placed in its respective category. Reference the specific sub-pillars and the emphasis placed on them.
    For each paper, list the title, category name, category description, and the reason for classification.
    Example output format with placeholders:
    ```
    Category 1: <Category Name>
    Category Description: <Description of Category>
    1. **Title: Paper 1**
    Reason: <reason for classification>
    2. **Title: Paper 2**
    Reason: <reason for classification>
    3. **Title: Paper 3**...
    Reason: <reason for classification>

    Category 2: <Category Name>
    Category Description: <Description of Category>
    1. **Title: Paper 1**
    Reason: <reason for classification>
    2. **Title: Paper 2**
    Reason: <reason for classification>
    3. **Title: Paper 3**...
    Reason: <reason for classification>

    Category <X>: <Category Name>
    Category Description: <Description of Category>
    1. **Title: Paper 1**
    Reason: <reason for classification>
    2. **Title: Paper 2**
    Reason: <reason for classification>
    3. **Title: Paper 3**...
    Reason: <reason for classification>

    ```
    Here are the definitions:
    {definitions}

"""

FRAMEWORK_CLASSIFICATION = """
    Your task is to write a prompt that instructs an LLM to learn patterns across the definitions to classify the definition frameworks into categories based on their similarities. For example, if two frameworks both emphasize functionality and similar umbrella terms the should be classified into the same category.

    Each definition should be classified using the paper’s title. 

    Example output format with placeholders:
    ```
    Category 1: <Category Name>
    Category Description: <Description of Category>
    1. **Title: Paper 1**
    Reason: <reason for classification>
    2. **Title: Paper 2**
    Reason: <reason for classification>
    3. **Title: Paper 3**...
    Reason: <reason for classification>

    Category 2: <Category Name>
    Category Description: <Description of Category>
    1. **Title: Paper 1**
    Reason: <reason for classification>
    2. **Title: Paper 2**
    Reason: <reason for classification>
    3. **Title: Paper 3**...
    Reason: <reason for classification>

    Category <X>: <Category Name>
    Category Description: <Description of Category>
    1. **Title: Paper 1**
    Reason: <reason for classification>
    2. **Title: Paper 2**
    Reason: <reason for classification>
    3. **Title: Paper 3**...
    Reason: <reason for classification>

    ```
    Here are the definitions:
    {definitions}
"""


DEFAULT_QUERY_TEMPLATE = """

<role>You are a researcher who's writing a paper surveying the existing papers on a subject. You are writing to answer a specific question based on the following definitions from all the papers.</role>

<task> You are given the following definitions of Responsible Artificial Intelligence (RAI) from all the papers. You are also given a question. Please answer the question by sythesizing the definitions. That means your answer should draw from the most relevant definitions. If the definition does not provide any relevant information, please do not use it. Each sentence of your answer should include at least one reference number in the form of "[number]", with the number representing the "id" of the paper that this sentence's statement is referencing or paraphrased from. An example of response is given below. </task> 

<example>
As black-box Machine Learning (ML) models are increasingly being employed to make important
predictions in critical contexts, the demand for transparency is increasing from the various stakeholders in
AI [6]. The danger is on creating and using decisions that are not justifiable, legitimate, or that simply do
not allow obtaining detailed explanations of their behaviour [7]. Explanations supporting the output of a
model are crucial, e.g., in precision medicine, where experts require far more information from the model
than a simple binary prediction for supporting their diagnosis [8, 12].</example>

<definitions> 
{definitions}
</definitions>
<question>
{question}
</question>
"""

LEGITMACY_QUESTION = {
    "name": "legitmacy", 
    "content": "What makes an AI system legitimate?"
}