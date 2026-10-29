import pprint
import llm_prompts

pp = pprint.PrettyPrinter(indent=4, compact = True)

DATA_PATH = "./datasets/07_obfuscated/data.csv"
TARGET_COLUMN="x81"


llm_prompts.generate_prompt(DATA_PATH, TARGET_COLUMN)
