NER_KEYWORD_EXTRACT_TEMPLATE = """
You are given an input text. Please go through the following steps and output the result: 

1. Remove stop words and add the rest if the words to the result,
2. extract the name entities and search phases from the input text and add them to the result comma separated,
3. for each word in the result, find at least two synonyms and append them to the end of the result, comma separated,
4. If any of the word is an acronym, expand it to the full name and append to the end of the result, comma separated,
5. Output the result.

Examples:

Input: 
What is the name of the most famous speech by MLK? 

Output: 
name, famous, speech, MLK, title, designation, well-known, renowned, address, talk, Martin Luther King, Martin Luther King, Jr.

Input: 
What are the principles and best practices of ensuring privacy in AI development? 

Output: 
principles, best, practices, ensuring, privacy, AI, development, guidelines, standards, optimal, ideal, methods, techniques, securing, guaranteeing, confidentiality, secrecy, Artificial Intelligence, machine learning, growth, advancement, Artificial Intelligence

Input: 
Please list the top five common principles for responsible AI.

Output: 
list, top, five, common, principles, responsible, AI, catalog, enumerate, leading, foremost, 5, quintet, typical, prevalent, guidelines, standards, accountable, ethical, Artificial Intelligence, machine learning, Artificial Intelligence

Here is the input:
```{input}```

Please return the output.
"""