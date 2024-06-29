from akagi.research_paper_distiller import main
input_dir = "responsible_ai_research_papers"
output_json = "output_definitions_json/responsible_ai_definitions.json"
main(input_dir, output_json, term="Responsible Artificial Intelligence")

from akagi.keywords_identifier import main
input_dir = "responsible_ai_research_papers"
main(input_dir)

from distiller import main
main()

from akagi.keyword_defintion_distiller import main
main()