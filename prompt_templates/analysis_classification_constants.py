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

<task> You are given the following definitions of Responsible Artificial Intelligence (RAI) from all the papers. You are also given a question. Please answer the question by sythesizing the definitions. That means your answer should draw from the most relevant definitions. If the definition does not provide any relevant information, please do not use it. Every sentence you generate, should be either a paraphase or direct quotation from one of the definitions provided below.

Each sentence of your answer should include at least one reference number in the form of "[number]", with the number representing the "id" of the paper that this sentence is paraphrasing or quoting from. An example of response is given below. </task> 

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

# Model validation and test
MODEL_QUESTION_CONTEXT = """
Algorithm selection is the second conceptual stage for building an AI model that starts with model training then evaluation. Once the model has been thoroughly tested and validated the model can be deployed. There are five RAI principles that must be accounted for which are 1) security, 2) privacy, 3) explainability for understandability, 4) sustainability, and 5) truthfulness.
"""

# Sythesizer script
SECURITY_QUESTION = {
    "name": "security",
    "content": MODEL_QUESTION_CONTEXT + "What makes an AI system secure?"
}
# User script: 
# What are the best practices such as methods, tools and techniques that makes an AI system secure? 

# Please write a simple definition for the "security" principle in model validation and testing for an AI system under the context of Responsbile AI.

PRIVACY_QUESTION = {
    "name": "privacy",
    "content": MODEL_QUESTION_CONTEXT + "What makes an AI system privacy compliant?"
}
# User script: 
# What are the best practices such as methods, tools and techniques that makes an AI system privacy compliant? 

EXPLAINABILITY_QUESTION = {
    "name": "explainability",
    "content": MODEL_QUESTION_CONTEXT + "What makes an AI system explainable so that all stakeholders can understand the system's behavior?"
}
# User script: 
# What are the best practices such as methods, tools and techniques that makes an AI system explainable and understandable? 

SUSTAINABILITY_QUESTION = {
    "name": "sustainability",
    "content": MODEL_QUESTION_CONTEXT + "What makes an AI system sustainable to maximize long-term benefits while minimizing negative environmental impact?"
}
# User script: 
# What are the best practices such as methods, tools and techniques that makes an AI system sustainable to minimize negative environmental impact? 

# Please write a simple definition for the "sustainability" principle in model validation and testing for an AI system under the context of Responsbile AI. It should focus on minimizing negative environmental impact.



# Used the user retrieval script instead due to few references using sythesizer script
# This means querying all the content (chucks) of all papers can produce better result than 
# querying only the processed RAI definitions (of all papers).  
TRUTHFULNESS_QUESTION = {
    "name": "truthfulness",
    "content": MODEL_QUESTION_CONTEXT + "What makes an AI system truthful in that it seeks facts and truth and does not give misinformation?"
}
# User script: 
# What are the best practices such as methods, tools and techniques that makes an AI system truthful adhereing to facts? 

MAINTAINABILITY_QUESTION = {
    "name": "maintainability",
    "content": MODEL_QUESTION_CONTEXT + "What are the best techincal practices and principles for Model monitoring?"
}
# User script: 
# What are the best practices such as methods, tools and techniques that makes an AI system maintainble? 

CONTESTABILITY_QUESION = {
    "name": "contestability",
    "content": MODEL_QUESTION_CONTEXT + "What are the best techincal practices and principles to make an AI model contestable?" 
}

AUDITABILITY_QUESION = {
    "name": "auditability",
    "content": MODEL_QUESTION_CONTEXT + "What are the best techincal practices and principles to make an AI model auditable?" 
}

# More queries for user script:

# Please write a simple defintion of "accountable" for AI system.   
# What are the best practices such as methods, tools and techniques that makes an AI system to be accountable?

# Please write a simple defintion for the "Legality" principle of System Design and Risk Assessment stage. 
# What are the best practices such as methods, tools and techniques that makes an AI system legal?
# Please write a simple defintion for the "Ethical" principle of System Design and Risk Assessment stage. 
# What are the best practices such as methods, tools and techniques that makes an AI system ethnical?


KEY_POINTS_ALIGNMENT_PROMPT = """

There are four stages of Responsible AI Life Cycle and their principles: 

Stage 1: System Design and Risk Assessment
1. Functionality 
A functional AI system is one that performs in a manner consistent with profit maximization, operating efficiency, and other key performance indicators.
2. Security 
The Security principle ensures that AI systems are protected from being attacked, co-opted, or misused by malicious actors.
3. Legality
The Legality principle of an AI system refers to the requirement that AI systems must be developed and used in compliance with existing and upcoming laws. This includes ensuring that AI systems respect citizens' fundamental rights and avoid potential liability. 

Stage 2: Data Validation and Testing
1. Fairness
Fairness in AI can be defined as the absence of any prejudice or favoritism toward an individual or a group based on their inherent or acquired characteristics. 
2. Privacy
An AI system is considered privacy compliant when it adheres to principles and practices that ensure the protection of personal data and respect for individuals' privacy rights throughout its lifecycle. 
3. Transparency
Transparency in AI systems refers to the clear, timely, easily understandable, and plain language explanation of what data is used, how it is collected, and how it influences the AI model's decisions.

Stage 3: Model Validation and Testing
1. Explainability for Understandability
An AI system is considered explainable when it provides clear, understandable, and transparent explanations of its decision-making processes to all stakeholders. 
2. Sustainability
Sustainability is the ability of the AI system to balance economic growth with social and environmental impacts. 
3. Truthfulness
An AI system is truthful if it describes the literal truth about the real world. Its output is consistent with facts that most domain experts agree upon.

Stage 4: System Monitoring
1. Maintainability
Maintainability refers to the ease with which an AI system can be modified to correct faults, improve performance, or adapt to a changed environment.

Stage 5: Algorithmic Auditing and Reassessment
1. Contestability
Contestability refers to the ability of individuals to challenge and seek redress against decisions made by AI systems. 
2. Auditability
Auditability is defined as the assessment of algorithms, data, and design processes while preserving the intellectual property related to the AI systems. This involves both internal and external auditors performing the assessment and making the reports available to contribute to the trustworthiness of the technology.
3. Accountability  
Accountability in AI systems refers to the mechanisms and practices that ensure individuals or organizations are held responsible for the actions and decisions made by AI systems.

Your task is to read the content below, and find out for each principle of each stage, which is the answer from the content:
1. Agree: because the content has similar definition, and provide a quote from your definition or explanation.
2. Disgree: because the content has a different definition, and provide a quote for that. 
3. No opinion: because the content hasn't discussed anything related.

Here's the content:
{context}

"""