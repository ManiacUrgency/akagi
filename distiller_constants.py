DEFAULT_TEMPLATE =  """
<Role>You are a researcher who specializes in many disciplines: humanity, social science, nero science and computer science and others. </Role>

<Task>You are given a research question and a list of documents. Each document provides an Id, Name and an Answer to the research question. Please provide an analysis on what is the agreement and disagreement across all the Answers. Based on that, summarize what is the concensus and the future work required to resolve the points of disagreement. Please ONLY use the content provided below in the Documents section for your analysis. Do NOT use any other content except general knowledge. </Task>

<Question>
What is the definition of Responsible AI?
</Question>

<Documents> 
{documents}
</Documents>

"""