DEFAULT_TEMPLATE = """
    The following are extracted titles from a research paper.
    Organize them into a JSON object with five keys: "main_heading" (int), "sub_heading" (int), "sub_sub_heading" (int), "heading_type" (string), and "title" (string). The "main_heading" key should store the main heading number the title belongs to (e.g., for "1.2.4", the "main_heading" key should store 1). If the title is not a main heading, it should store -1. The same applies to "sub_heading" and "sub_sub_heading" keys, which should store the respective heading numbers, or -1 if there is no value. The "heading_type" key should store the type of heading ("main heading", "sub-heading", or "sub-sub-heading"). The "title" key should store the title value from the input JSON (numbers and text of the title in one string). Your response should consist solely of the JSON object, without any other characters outside of the JSON object. Here is an example:

    Input:
    {{"title": "1. Introduction"}},
    {{"title": "2. Explainability: What, Why, What For and How?"}},
    {{"title": "2.1. Terminology Clarification"}},
    {{"title": "2.2. What?"}},
    {{"title": "2.3. Why?"}},
    {{"title": "2.4. What for?"}},
    {{"title": "2.5. How?"}},
    {{"title": "2.5.1. Levels of Transparency in Machine Learning Models"}},
    {{"title": "2.5.2. Post-hoc Explainability Techniques for Machine Learning Models"}}

    Output:
    {{"main_heading": 1, "sub_heading": -1, "sub_sub_heading": -1, "heading_type": "main heading", "title": "1. Introduction"}},
    {{"main_heading": 2, "sub_heading": -1, "sub_sub_heading": -1, "heading_type": "main heading", "title": "2. Explainability: What, Why, What For and How?"}},
    {{"main_heading": 2, "sub_heading": 1, "sub_sub_heading": -1, "heading_type": "sub-heading", "title": "2.1. Terminology Clarification"}},
    {{"main_heading": 2, "sub_heading": 2, "sub_sub_heading": -1, "heading_type": "sub-heading", "title": "2.2. What?"}},
    {{"main_heading": 2, "sub_heading": 3, "sub_sub_heading": -1, "heading_type": "sub-heading", "title": "2.3. Why?"}},
    {{"main_heading": 2, "sub_heading": 4, "sub_sub_heading": -1, "heading_type": "sub-heading", "title": "2.4. What for?"}},
    {{"main_heading": 2, "sub_heading": 5, "sub_sub_heading": -1, "heading_type": "sub-heading", "title": "2.5. How?"}},
    {{"main_heading": 2, "sub_heading": 5, "sub_sub_heading": 1, "heading_type": "sub-sub-heading", "title": "2.5.1. Levels of Transparency in Machine Learning Models"}},
    {{"main_heading": 2, "sub_heading": 5, "sub_sub_heading": 2, "heading_type": "sub-sub-heading", "title": "2.5.2. Post-hoc Explainability Techniques for Machine Learning Models"}}

    Now process the following titles:
    {titles}
    """

NUMBER_HEADINGS_TEMPLATE = """
    The following are extracted titles from a research paper. Each JSON object should have only one key: "title". The "title" key should contain both the number and the title as a single string. If the titles already have numbers, do not edit them and return the JSON unedited. If the titles do not have numbers, add them sequentially based on the hierarchical structure. Subsections should follow the main sections appropriately, e.g., 1, 1.1, 1.2, 2, 2.1, and so on.
    Your response should consist solely of the JSON object, without any other characters outside of the JSON object. Here is an example:

    Input:
    1. Introduction
    Explainability: What, Why, What For and How?
    Terminology Clarification
    What?
    Why?
    What for?
    How?
    Levels of Transparency in Machine Learning Models
    Post-hoc Explainability Techniques for Machine Learning Models

    Output:
    [
        {{"title": "1. Introduction"}},
        {{"title": "2. Explainability: What, Why, What For and How?"}},
        {{"title": "2.1. Terminology Clarification"}},
        {{"title": "2.2. What?"}},
        {{"title": "2.3. Why?"}},
        {{"title": "2.4. What for?"}},
        {{"title": "2.5. How?"}},
        {{"title": "2.5.1. Levels of Transparency in Machine Learning Models"}},
        {{"title": "2.5.2. Post-hoc Explainability Techniques for Machine Learning Models"}}
    ]

    Now process the following titles:
    {titles}
    """


