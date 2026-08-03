import pprint
import llm_prompts

pp = pprint.PrettyPrinter(indent=4, compact = True)

# DATA_PATH = r"D:\oxoa\DataLinter\LLM_Experiments\llm_dl_pipeline\datasets\01_obfuscated\data.csv"
DATA_PATH = r"d:\oxoa\DataLinter\LLM_Experiments\llm_dl_pipeline\datasets\07_obfuscated\data.csv"
TARGET_COLUMN="x82"


llm_prompts.generate_prompt(DATA_PATH, TARGET_COLUMN)