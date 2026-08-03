import pandas as pd
import numpy as np

def extract_dataset_properties(data_path):
    df = pd.read_csv(data_path)
    description = df.describe()
    df_total_rows, df_total_columns = df.shape
    cprops = {}
    for c in df.columns:
        _type = df.dtypes[c]
        if _type == np.dtype("str") or _type == "str": #or f"{_type}"=="str"
            cprops.update(
                {str(c):
                    {
                        "type": str(_type),
                        #"null_count": df_total_rows - df[c].notna().sum(),
                        "null_count": (df[c]=="?").sum(),
                        #"non_null_count": df[c].notna().sum() ,
                        "non_null_count": (df[c]!="?").sum() ,
                        "max_length": max(df[c].str.len()),
                        "min_length": min(df[c].str.len())
                    }
                })
        else:
            cprops.update(
                {str(c):
                    {
                        "type": str(_type),
                        "null_count": df_total_rows - df[c].notna().sum(),
                        "non_null_count": df[c].notna().sum(),
                        "max_value" : df[c].max(),
                        "min_value" : df[c].min(),
                        "median_value" : df[c].median(),
                        "mean_value" : df[c].mean()
                    }
                })
        
    
    return cprops , df.shape, df


def make_llm_initial_prompt(cprops, shape, target_coumn, data_path):
    total_rows, total_columns = shape
    dataset_properties_string = f"""
        rows count: {total_rows},
        columns count: {total_columns}
    """

    for c, cdict in cprops.items():
        if(cdict["type"] == "str"):
            _str = f"\n    column '{c}': type {cdict["type"]}, {cdict["null_count"]} nulls, {cdict["non_null_count"]} non-nulls, maximum string length {cdict["max_length"]}, minimum string length {cdict["min_length"]}"
        else:
            _str = f"\n    column '{c}': type {cdict["type"]}, {cdict["null_count"]} nulls, {cdict["non_null_count"]} non-nulls, maximum value {cdict["max_value"]}, minimum value {cdict["min_value"]}, median value {cdict["median_value"]}, mean value {cdict["mean_value"]}"
            
        dataset_properties_string = dataset_properties_string + _str
    
    return f"""You are a data scientist trying to create a regression experiement in R. Considering a dataset located at {data_path} with the following properties:
    {dataset_properties_string}
    write a regression experiment using minimal code in which the variable '{target_coumn}' can be predicted from the other variables.
    You can use only the "lm", "glm", "glmmTMB" libraries.
    Use the most appropriate regression algorithm of the 3 above.
    Place the regression formula directly in the regression algorithm function call. Do not use variables as arguments for the formula.
    Explicitly transform all non-numerical columns into numerical columns before calling the regression algorithm.
    Make a 70%-30% train test split in the data and calculate RMSE on the test data.
    """

    

# def make_llm_fix_prompt():
#         """The line of code with the model training was passed through a linter that checked the code and the properties of the data.

#             The found issues are listed below.

#             Please rewrite the code in a way that will solve the found issues.

#             When reformulating the code solution: do not remove any columns, do not remove any samples, impute missing values.

#             Use the same 70-30 train test split as in the initial code with random seed 42.
#             Issues found:"""

    
# call LLM to get the code - regex to extract it

# CALL DATALINTER with the generated code

def generate_prompt(data_path, target_column):
    cprops, shape, _ = extract_dataset_properties(data_path)
    print(make_llm_initial_prompt(cprops, shape, target_column, data_path))
