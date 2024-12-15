from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_GNEWS_KEY"),  # This is the default and can be omitted
)

def extract_relevance_and_location(article_text):
    """
    Extracts locations mentioned in a news article using OpenAI's GPT-4 Turbo API.
    :param article_text: The text of the news article.
    :return: A list of locations mentioned in the article.
    """

    prompt = f"""
    Please review the following article and extract the following attributes: 

    isRelated: Is this article related to "opioid crisis"? 
    isNational: Is the event happened at the national level, that it is not specific to any location of the country?  
    location: the location where the event covered in the article occurred, if the event is at the local level and we can detect the location. We may have multiple locations. For each location, we list the city and state as part of the value of location if we can detect any or both of them. 
    city: the primary city chosen from all the cities identified. The same city if there's only one city identified.
    state: the primary state chosen from all the states identified. The same state if there's only one state identified.

    Output should be in the JSON format such as: 
    {{ 
        "isRelated": true,
        "isNational": false,
        "city": "San Francisco", 
        "state": "California"
        location: [{{
            "city": "San Francisco", 
            "state": "California"
        }},
        location: {{
            "city": "San Jose", 
            "state": "California"
        }}]
    }}

    {article_text}
    
    Return the locations as a comma-separated list.
    """

    # Extract all the locations (e.g., cities, states, countries, landmarks, etc.) mentioned in the following news article:
    
    try:
        # Call the GPT-4 Turbo model
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an assistant skilled at extracting information from text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0  # For consistent and precise outputs
        )
        
        # Extract locations from the response
        result = response.choices[0].message.content.strip()
        return result
    
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    # Example news article text
    # article_text = """
    # Thousands of people gathered in Washington, D.C., to voice their concerns about recent legislative changes. 
    # Across the Atlantic, similar gatherings took place in Berlin and Rome. 
    # In Asia, Tokyo and Beijing saw smaller but significant protests.
    # """
    article_texts = []
    article_texts.append('''
    To combat the ongoing opioid overdose crisis and support harm reduction strategies, Los Angeles County Library is expanding naloxone clinics, including a site at the West Hollywood Library, to offer free fentanyl test strips.

    The initiative, in partnership with the California Department of Health Care Service, aims to create safer and healthier communities by providing resources to help mitigate risks associated with opioid use.

    “Fentanyl poisonings are not something we can bury our heads in the sand on. Our young people are at risk, and parents are scared. Bringing these life-saving tools like test strips and naloxone into libraries and making them as accessible as possible to every community makes sense,” said Supervisor Janice Hahn, 4th District, who led the board of supervisors in establishing the naloxone clinics at county libraries. “I’m thankful to our L.A. County library staff for their willingness to be this critical resource for the communities they serve.”

    Fentanyl test strips are available the West Hollywood Library every Wednesday from noon-4 p.m. Twelve other county library branches will also provide the strips including the A.C. Bilbrew Library, Claremont Helen Renwick Library, Compton Library, East Los Angeles Library, El Monte Library, Lancaster Library, Leland R. Weaver Library, Lennox Library, Malibu Library, Norwalk Library, San Fernando Library and Temple City Library.

    “L.A. County Library is committed to supporting the health and well-being of our communities,” L.A. County Librarian and CEO Skye Patrick said. “By offering both naloxone and fentanyl test strips, we are taking proactive steps to reduce the devastating impact of the opioid crisis in Los Angeles County.”

    Fentanyl is a synthetic opioid up to 50 times stronger than heroin and 100 times more potent than morphine. It is often mixed into other substances without individuals being aware, making it extremely dangerous. Even a tiny amount can be fatal. Fentanyl test strips detect the presence of fentanyl, helping prevent accidental exposure and reducing the risk of fatal overdoses.

    The West Hollywood Library is located at 625 N. San Vicente Blvd. For information, visit lacountylibrary.org/naloxone.
    ''')

    article_texts.append('''
    STORY: Analysts believe President-elect Donald Trump's upcoming term could be the start of a bruising four-year trade war.

    And on Thursday (Nov 28), China hit back against Trump's pledge to put additional tariffs on Chinese goods over fentanyl flows.

    A spokesperson for China's commerce ministry said the incoming administration was pushing to blame China for the U.S. opioid crisis.

    (SOUNDBITE) (Mandarin) CHINESE COMMERCE MINISTRY SPOKESPERSON, HE YADONG, SAYING:

    "China's stance of opposing unilateral tariff increases has been consistent. Imposing tariffs arbitrarily on trade partners cannot solve the problems within the United States itself."

    Trump, who takes office on January 20th, said on Monday he would impose a 10% tariff on Chinese goods.

    He says he wants Beijing to do more to stop the trafficking of Chinese-made chemicals used in fentanyl, a highly addictive narcotic.

    He also threatened tariffs in excess of 60% on Chinese goods while on the campaign trail.

    Related Videos

    00:26

    01:04

    02:33

    06:32

    (SOUNDBITE) (Mandarin) CHINESE COMMERCE MINISTRY SPOKESPERSON, HE YADONG, SAYING:

    "The United States should abide by World Trade Organisation rules and work with China to promote the stable and sustainable development of economic and trade relations, in accordance with the principles of mutual respect, peaceful coexistence and win-win cooperation."

    Trump's comments fired the starting gun for what some expect to be a trade war, potentially much worse than his first term.

    That saw tariffs of between 7% and 25%, and global supply chains uprooted.

    Recommended Stories
    ''')

    article_texts.append('''
    SUNY Broome is providing an invaluable opportunity for eligible New York State residents to pursue their passion for helping individuals struggling with addiction through full scholarships offered for the Chemical Dependency Counseling Associate of Applied Science (AAS) degree in conjunction with the Credentialed Alcoholism and Substance Abuse Counselor (CASAC) program.

    Supported by the New York State Opioid Settlement Fund and overseen by the New York State Office of Addiction Services and Supports (OASAS), these scholarships hope to address the critical need for certified CASACs in combatting addiction across New York.

    The funding covers not only the cost of tuition and mandatory fees but also the CASAC credential application and exam fees, easing the financial burden on students pursuing this important certification. Additionally, stipends are provided to students during corresponding internships as part of the program.

    Eligibility Criteria

    The scholarship program is open to New York State residents who are at least 18 years old by the completion of the first semester of the program and hold a high school diploma or high school equivalency (HSE) diploma.

    Priority for scholarship consideration is given to employees of specific programs under OASAS, OMH, or DOH. Following the consideration of priority populations, individuals working within the addictions field or those interested in pursuing a career in eligible OASAS, OMH, or DOH settings are also eligible to apply.

    Application Process

    To apply for the scholarship program, interested individuals must start by completing a free application to SUNY Broome and submitting their official high school transcript or GED certificate and transcript to admissions@sunybroome.edu.

    Applicants are required to fill out the OASAS Scholarship Application and send the completed application via email to Kristen Oliver at oliverkl2sunybroomeedu.

    Prospective students are advised to fill out the application as quickly as possible as the spring semester begins on January 27, 2025. For more information and to begin the application process, please visit the Chemical Dependency Counseling AAS Scholarships website.
    ''')

    article_texts.append('''
    Heyo. It’s 6:41 a.m. And we are on the Long Island Expressway. For most of you, Thanksgiving is going to mean either hosting or being hosted for a very special meal. So yeah, we’re going to be sitting in traffic for quite some time. And when we thought about that, our minds immediately went to the great host of our times, Ina Garten, a.k.a. the Barefoot Contessa. And she invited us into her absolutely idyllic home. Let us into her barn, which is her test kitchen. “Thank you so much. That’s really sweet.” “We don’t have to drink it, but we could.” “We could.” And there she taught us how to make the perfect glazed ham that is completely ready by the time you walk in her door. “Ham, meet ham.” And how to make the perfect seasonal cocktail. In this case, it was a cranberry martini. “It’s really nice.” “Isn’t it good.” And for your benefit, we recorded the entire thing. And it is today’s “Daily.” Happy Thanksgiving, everyone.                     
    ''')

    for i, article_text in enumerate(article_texts):
        print("\nArticle ", i, ":\n")
        result = extract_relevance_and_location(article_text)
        print(result)
        
    # result = extract_relevance_and_location(article_texts[3])
    # print(result)