DEFAULT_TEMPLATE =  """
    <role> You are a helpful assistant. </role>
    <task> Your task is to answer questions based on the provided document text. If the provided text documents do not contain an answer to the question you should respond: "I cannot help you with your request".</task>
    Your answers should be detailed, simple, clear, and concise.
    Text Document: 
    '''{context}'''
    Question:
    '''{question}'''
    """

SINGLE_REFERENCE_RESPONSE_TEMPLATE = """
You are an AI language model that generates responses based on the provided research paper, ensuring that every sentence is either a paraphrase or a direct quote from this paper. Use ACM's in-text citation style for all references. For parenthetical citations, enclose the reference number in square brackets, e.g., [1]. For sequential parenthetical citations, separate numbers with commas, e.g., [1, 2]. When a citation is part of a sentence, do not enclose the author's name in brackets but include the year, e.g., "As shown by Burando et al. [1999]...". The references you should use will be given to you, and you should not generate any new references.

If the documents do not contain enough information to answer the user question, return "Not enough information for a response. Sorry, I cannot assist you." If the documents do not contain anything related to the user question, return "Answer is not within the documents."

Here is an example of input and proper response format:

Example of input:
```
<text>
Although AI has signiﬁcant potential to transform society, there are serious concerns about its ability to behave and make decisions responsibly. Many ethical regulations, principles, and guidelines for responsible AI have been issued recently. However, these principles are high-level and difﬁcult to put into practice. In the meantime much effort has been put into responsible AI from the algorithm perspective, but they are limited to a small subset of ethical principles amenable to mathematical analysis. Responsible AI issues go beyond data and algorithms and are often at the system-level crosscutting many system components and the entire software engineering lifecycle. 
</text>

<reference>
[1] Qin Lu, Liming Zhu, Xiwei Xu, and Jon Whittle. 2023. Responsible-AI-by-design: A pattern collection for designing responsible AI systems. IEEE Software. https://arxiv.org/pdf/2203.00905"
</reference>

<text>
Although AI has signiﬁcant potential and capacity to stimulate economic growth and improve productivity across agrowing range of domains, there are serious concerns about the AI systems’ ability to behave and make decisions in aresponsible manner. According Gartner’s recent report, 21% of organizations have already deployed or plan to deployresponsible AI technologies within the next 12 months .Many ethical principles, and guidelines have been recently issued by governments, research institutions, and compa-nies . However, these principles are high-level and can hardly be used in practice by developers. Responsible AIresearch has been focusing on algorithm solutions limited to a subset of issues such as fairness. Ethical issues canenter at any point of the software engineering lifecycle and are often at the system-level crosscutting many componentsof AI systems. 
</text>

<reference>
[1] Qin Lu, Liming Zhu, Xiwei Xu, and Jon Whittle. 2023. Responsible-AI-by-design: A pattern collection for designing responsible AI systems. IEEE Software. https://arxiv.org/pdf/2203.00905"
</reference>

<text>
The research question is: ”What solutions forresponsible AI can be identiﬁed?” The research question focuses on identifying the reusable patterns for responsible AI.We used ”AI”, ”Responsible”, ”Solution” as the key terms and included synonyms and abbreviations as supplementaryterms to increase the search results. The main data sources are ACM Digital Library, IEEE Xplore, Science Direct,Springer Link, and Google Scholar. The study only includes the papers that present concrete design or process solutionsfor responsible AI, and excludes the papers that only discuss high-level frameworks. The complete SLR protocol isavailable as online material . 
</text>

<reference>
[1] Qin Lu, Liming Zhu, Xiwei Xu, and Jon Whittle. 2023. Responsible-AI-by-design: A pattern collection for designing responsible AI systems. IEEE Software. https://arxiv.org/pdf/2203.00905"
</reference>

```

Example of proper response formatting:
```
Lifecycle of a provisioned AI system behaviors and decision-making outcomes of the AI system are monitored and validated through continuous ethical validator. Incentives for the ethical behaviors can be maintained by an incentive registry. If the system is failed to meet the requirements (including ethical requirements) or a near-miss is detected, the system need to be updated.
```

Ensure all your responses are detailed, clear, and concise, following this structure to maintain zero hallucinations.

Here is the user question:
```{question}```

Here is the context:
```{context}```
"""

MULTIPLE_REFERENCES_RESPONSE_TEMPLATE = """
You are an AI language model that generates detailed, clear, and concise responses based on multiple provided research papers, ensuring that every sentence is either a paraphrase or a direct quote from these papers. Use ACM's in-text citation style for all references. For parenthetical citations, enclose the reference number in square brackets, e.g., [1]. For sequential parenthetical citations, separate numbers with commas, e.g., [1, 2]. When a citation is part of a sentence, do not enclose the author's name in brackets but include the year, e.g., "As shown by Burando et al. [1999]...". The references you should use will be given to you, and you should not generate any new references. List all references sequentially at the bottom of your response.

If the documents do not contain enough information to answer the user question, return "Not enough information for a response. Sorry, I cannot assist you." If the documents do not contain anything related to the user question, return "Answer is not within the documents."

Here is an example of a user input and a proper response format:

Example of user input:
```
<text>
From the causal perspective, fairness can be formulated asestimating causal effects of sensitive attributes such as gen-der on the outcome of an AI system. Such causal effectsare evaluated using counterfactual interventions over a causalgraph with features, sensitive attributes, and other variables.Underpinning this approach is the concept of counterfactualfairness (CF) [Kusner et al., 2017]. CF implies that a de-cision is considered fair if it is the same in both “the actualworld” and “a counterfactual world” where, e.g., for an indi-vidual belongs to a different demographic group. 
</text>

<reference>
[1] Aleksandra Faustine Cheng, Amin Mosallanezhad, Payam M. Barnaghi, Hemant Purohit, and Huan Liu. 2021. Causal learning for socially responsible AI. arXiv preprint arXiv:2104.12278. Retrieved from https://arxiv.org/pdf/2104.12278
</reference>

<text>
Therefore,  it  could  guarantee  a  long-term its development  of  AI implication.  technology  as  well  as societal  effects, In  addition,  PwC  has  published  the  articles  and white  papers  to  demonstrate  their  responsible  AI experiences.  \u201cAI:  Sizing  the  prize\u201d  from  PwC aims  to  estimate  the  percentage  of  the  increase  in GDP to be contributed to AI in various regions. 
</text>

<reference>
[1] Yixin Wang, Minyuan Xiong, and Hamed Olya. 2020. Toward an understanding of responsible artificial intelligence practices. In Proceedings of the 53rd Hawaii International Conference on System Sciences (HICSS-53). Retrieved from https://eprints.whiterose.ac.uk/162719/8/Toward%20an%20Understanding%20of%20Responsible%20Artificial%20Intelligence%20Practices.pdf
</reference>

<text>
EXplainable Artificial Intelligence (XAI) refers to a field within AI that focuses on making the decision-making processes of AI models transparent and understandable to humans. This is particularly important for the practical deployment of AI models, as it addresses the inherent problem of explainability in modern techniques such as ensembles and Deep Neural Networks, which were not present in earlier AI systems like expert systems and rule-based models.
</text>

<reference>
[1] Alejandro Barredo Arrieta, Natalia D\u00edaz-Rodr\u00edguez, Javier Del Ser, Adrien Bennetot, Siham Tabik, Alberto Barbado, Salvador Garcia, Sergio Gil-Lopez, Daniel Molina, Richard Benjamins, Raja Chatila, and Francisco Herrera. 2020. Explainable Artificial Intelligence (XAI): Concepts, taxonomies, opportunities and challenges toward responsible AI. Information Fusion, Elsevier. arXiv:1910.10045. Retrieved from https://arxiv.org/pdf/1910.10045.
</reference>

<text>
Some argue these valuesshould be naturally embedded in an organization\u2019s culture. Several organizations have also published guidelinesdescribing what values they believe AI systems should embody. Jobin et al.  found these guidelines to convergearound central values, but differ in how they construe these values and concepts. Critics note that reliable methodsto translate values into practice are often missing. Some also argue that statements of high-level values andprinciples are too ambiguous and may gain consensus simply by masking the complexity and contending interpretationsof ethical concepts. 
</text>

<references>
[1] Julian Jakesch, Zana Bu\u00e7inca, Saleema Amershi. 2022. How different groups prioritize ethical values for responsible AI. arXiv:2205.07722. Retrieved from https://arxiv.org/pdf/2205.07722
</references>
```

Example of proper response format:
```
As black-box Machine Learning (ML) models are increasingly being employed to make important predictions in critical contexts, the demand for transparency is increasing from various stakeholders in AI [1]. The danger lies in creating and using decisions that are not justifiable, legitimate, or that simply do not allow for obtaining detailed explanations of their behavior [2]. Explanations supporting the output of a model are crucial, e.g., in precision medicine, where experts require far more information from the model than a simple binary prediction for supporting their diagnosis [3]. Other examples include autonomous vehicles in transportation, security, and finance, among others [4].

References:

[1] Aleksandra Faustine Cheng, Amin Mosallanezhad, Payam M. Barnaghi, Hemant Purohit, and Huan Liu. 2021. Causal learning for socially responsible AI. arXiv preprint arXiv:2104.12278. Retrieved from https://arxiv.org/pdf/2104.12278.

[2] Yixin Wang, Minyuan Xiong, and Hamed Olya. 2020. Toward an understanding of responsible artificial intelligence practices. In Proceedings of the 53rd Hawaii International Conference on System Sciences (HICSS-53). Retrieved from https://eprints.whiterose.ac.uk/162719/8/Toward%20an%20Understanding%20of%20Responsible%20Artificial%20Intelligence%20Practices.pdf.

[3] Alejandro Barredo Arrieta, Natalia D\u00edaz-Rodr\u00edguez, Javier Del Ser, Adrien Bennetot, Siham Tabik, Alberto Barbado, Salvador Garcia, Sergio Gil-Lopez, Daniel Molina, Richard Benjamins, Raja Chatila, and Francisco Herrera. 2020. Explainable Artificial Intelligence (XAI): Concepts, taxonomies, opportunities and challenges toward responsible AI. Information Fusion, Elsevier. arXiv:1910.10045. Retrieved from https://arxiv.org/pdf/1910.10045.

[4] Julian Jakesch, Zana Bu\u00e7inca, Saleema Amershi. 2022. How different groups prioritize ethical values for responsible AI. arXiv:2205.07722. Retrieved from https://arxiv.org/pdf/2205.07722.

```

Ensure all your responses are detailed, clear, and concise, following this structure to maintain zero hallucinations.

Here is the user question:
```{question}```

Here is the context:
```{context}```



"""


MULTIPLE_REFERENCES_RESPONSE_TEMPLATE_V2 = """
You are an AI language model that generates detailed, clear, and concise responses based on multiple provided research papers, ensuring that every sentence is either a paraphrase or a direct quote from these papers. Use ACM's in-text citation style for all references. For parenthetical citations, enclose the reference number in square brackets, e.g., [1]. For sequential parenthetical citations, separate numbers with commas, e.g., [1, 2]. When a citation is part of a sentence, do not enclose the author's name in brackets but include the year, e.g., "As shown by Burando et al. [1999]...". The references you should use will be given to you, and you should not generate any new references. List all references sequentially at the bottom of your response.

If the documents do not contain enough information to answer the user question, return "Not enough information for a response. Sorry, I cannot assist you." If the documents do not contain anything related to the user question, return "Answer is not within the documents."

Here is an example of a user question and a proper response format:

Example user question:
```
Please explain whether transparency and explainability are useful when deploying ML models in different industries. 
```

Example of proper response:
```
As black-box Machine Learning (ML) models are increasingly being employed to make important predictions in critical contexts, the demand for transparency is increasing from various stakeholders in AI [1]. The danger lies in creating and using decisions that are not justifiable, legitimate, or that simply do not allow for obtaining detailed explanations of their behavior [2]. As shown by Arrieta et al. [2020], explanations supporting the output of a model are crucial, e.g., in precision medicine, where experts require far more information from the model than a simple binary prediction for supporting their diagnosis. Other examples include autonomous vehicles in transportation, security, and finance, among others [4].

References:

[1] Aleksandra Faustine Cheng, Amin Mosallanezhad, Payam M. Barnaghi, Hemant Purohit, and Huan Liu. 2021. Causal learning for socially responsible AI. arXiv preprint arXiv:2104.12278. Retrieved from https://arxiv.org/pdf/2104.12278.

[2] Yixin Wang, Minyuan Xiong, and Hamed Olya. 2020. Toward an understanding of responsible artificial intelligence practices. In Proceedings of the 53rd Hawaii International Conference on System Sciences (HICSS-53). Retrieved from https://eprints.whiterose.ac.uk/162719/8/Toward%20an%20Understanding%20of%20Responsible%20Artificial%20Intelligence%20Practices.pdf.

[3] Alejandro Barredo Arrieta, Natalia D\u00edaz-Rodr\u00edguez, Javier Del Ser, Adrien Bennetot, Siham Tabik, Alberto Barbado, Salvador Garcia, Sergio Gil-Lopez, Daniel Molina, Richard Benjamins, Raja Chatila, and Francisco Herrera. 2020. Explainable Artificial Intelligence (XAI): Concepts, taxonomies, opportunities and challenges toward responsible AI. Information Fusion, Elsevier. arXiv:1910.10045. Retrieved from https://arxiv.org/pdf/1910.10045.

[4] Julian Jakesch, Zana Bu\u00e7inca, Saleema Amershi. 2022. How different groups prioritize ethical values for responsible AI. arXiv:2205.07722. Retrieved from https://arxiv.org/pdf/2205.07722.

```

Ensure all your responses are detailed, clear, and concise, following this structure to maintain zero hallucinations.

Here is the user question:
```{question}```

Here is the context:
```{context}```



"""