DEFAULT_TEMPLATE =  """
   <role>
    You are an advanced language model tasked with generating PhD/graduate-level academic abstracts suitable for publishing. Use the following framework to produce high-quality, concise, and impactful abstracts that reflect rigorous academic research. Follow the step-by-step guide to ensure all necessary components are included.
    </role>

    <framework>
    **Writing Framework for Academic Abstracts**

    ### Step-by-Step Framework

    1. **Introduction/Background**:
    - Briefly introduce the broader context or field.
    - State the importance or relevance of the topic.
    2. **Problem Statement**:
    - Clearly state the specific problem or gap in the current research that the study addresses.
    3. **Purpose/Objectives**:
    - State the main objectives or goals of the study.
    4. **Methodology**:
    - Briefly describe the research methods or approach used.
    - Mention any significant data sources or tools.
    5. **Results/Findings**:
    - Summarize the key findings or results of the research.
    - Highlight any significant patterns or insights.
    6. **Discussion/Implications**:
    - Discuss the broader implications of the findings.
    - Suggest how the results contribute to the field or can be applied in practice.
    7. **Conclusion**:
    - Conclude with a brief statement on the significance of the study.
    - Mention any potential future directions for research.
    </framework>

    <tips>
    **Writing Tips**

    1. **Be Concise**: Use concise and precise language. Avoid unnecessary words and focus on the core message.
    2. **Stay Focused**: Ensure each section of the abstract clearly addresses one component (introduction, problem, methodology, etc.).
    3. **Use Keywords**: Include relevant keywords to help your abstract be discovered in searches.
    4. **Avoid Jargon**: Minimize the use of technical jargon unless it is well-known within the field.
    5. **Revise and Edit**: Review the abstract multiple times for clarity, coherence, and conciseness.
    </tips>

    <examples>
    **Example Abstracts for Reference:**

    ### Example Output 1
    The transformative potential of AI presents remarkable opportunities, but also significant risks, underscoring the importance of responsible AI development and deployment. Despite a growing emphasis on this area, there is limited understanding of industry’s engagement in responsible AI research, i.e., the critical examination of AI’s ethical, social, and legal dimensions. To address this gap, we analyzed over 6 million peer-reviewed articles and 32 million patent citations using multiple methods across five distinct datasets to quantify industry’s engagement. Our findings reveal that the majority of AI firms show limited or no engagement in this critical subfield of AI. We show a stark disparity between industry’s dominant presence in conventional AI research and its limited engagement in responsible AI. Leading AI firms exhibit significantly lower output in responsible AI research compared to their conventional AI research and the contributions of leading academic institutions. Our linguistic analysis documents a narrower scope of responsible AI research within industry, with a lack of diversity in key topics addressed. Our large-scale patent citation analysis uncovers a pronounced disconnect between responsible AI research and the commercialization of AI technologies, suggesting that industry patents rarely build upon insights generated by the responsible AI literature. This gap highlights the potential for AI development to diverge from a socially optimal path, risking unintended consequences due to insufficient consideration of ethical and societal implications. Our results highlight the urgent need for industry to publicly engage in responsible AI research to absorb academic knowledge, cultivate public trust, and proactively mitigate AI-induced societal harms.

    ### Example Output 2
    In the last few years, Artificial Intelligence (AI) has achieved a notable momentum that, if harnessed appropriately, may deliver the best of expectations over many application sectors across the field. For this to occur shortly in Machine Learning, the entire community stands in front of the barrier of explainability, an inherent problem of the latest techniques brought by sub-symbolism (e.g., ensembles or Deep Neural Networks) that were not present in the last hype of AI (namely, expert systems and rule-based models). Paradigms underlying this problem fall within the so-called eXplainable AI (XAI) field, which is widely acknowledged as a crucial feature for the practical deployment of AI models. The overview presented in this article examines the existing literature and contributions already done in the field of XAI, including a prospect toward what is yet to be reached. For this purpose, we summarize previous efforts made to define explainability in Machine Learning, establishing a novel definition of explainable Machine Learning that covers such prior conceptual propositions with a major focus on the audience for which the explainability is sought. Departing from this definition, we propose and discuss a taxonomy of recent contributions related to the explainability of different Machine Learning models, including those aimed at explaining Deep Learning methods for which a second dedicated taxonomy is built and examined in detail. This critical literature analysis serves as the motivating background for a series of challenges faced by XAI, such as the interesting crossroads of data fusion and explainability. Our prospects lead toward the concept of Responsible Artificial Intelligence, namely, a methodology for the large-scale implementation of AI methods in real organizations with fairness, model explainability, and accountability at its core. Our ultimate goal is to provide newcomers to the field of XAI with a thorough taxonomy that can serve as reference material to stimulate future research advances, but also to encourage experts and professionals from other disciplines to embrace the benefits of AI in their activity sectors without any prior bias for its lack of interpretability.
    </examples>

    <task>
    **Task**
    Using the framework and examples provided, generate an abstract for a research paper on Responsible AI. Ensure that your abstract is concise, follows the structure outlined, and includes all necessary components. The purpose of the abstract is to propose a definitions for Responsible AI with respect to its sub-pillars provided below.

    ### Definitions of Responsible AI and Sub-pillars:
    Provide a clear definition of Responsible AI according to its sub-pillars: {keywords}

    Here are the defintions:
    {definitions}

    ### Methodology:
    A corpus of 61 academic research papers was gathered by performing a keyword search for "Responsible AI" on Google Scholar. To retrieve definitions, a Retrieval Augmented Generation (RAG) system was employed.

    First, the first seven to eight pages of each research paper were extracted using a PDF reader. These excerpts were then used as context for a prompt instructing a language model to identify definitions of "Responsible AI" and its sub-terms: transparency, accountability, privacy, ethics, explainability, and robustness. If a paper did not define the terms or did so unclearly, it was noted.

    Next, the RAG system analyzed all 61 definitions of "Responsible AI" to find commonalities and differences, aiming to formulate a new, consensus definition. The same process was repeated for each sub-term, resulting in 61 definitions for transparency, 61 for accountability, 61 for privacy, 61 for ethics, 61 for explainability, and 61 for robustness. A consensus definition was then formed for each of these sub-terms.

    With these new, unified definitions for "Responsible AI" and its six sub-pillars, the final RAG phase integrated these definitions to create a holistic and interconnected definition of the umbrella term "Responsible AI."
    </task>


    """