import pandas as pd
import numpy as np
import pprint
pp = pprint.PrettyPrinter(indent=4, compact = True)

DATA_PATH = "d:/oxoa/DataLinter/LLM_Experiments/llm_dl_pipeline/datasets/concrete_compressive_strength_prediction/concrete_data.csv"

def p1(data_path):
    df = pd.read_csv(data_path)
    description = df.describe()
    df_total_rows, df_total_columns = df.shape
    cprops = {}
    for c in df.columns:
        _type = df.dtypes[c]
        if(_type == np.dtype("str")):
            cprops.update(
                {str(c):
                    {
                        "type": str(_type),
                        "null_count": df_total_rows - df[c].notna().sum(),
                        "non_null_count": df[c].notna().sum(),
                        "max_length": len(df[c].max()),
                        "min_length": len(df[c].min())
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
        
    
    return cprops , df.shape


def p2(p2_input):
    target = "concrete_compressive_strength"

    cprops, shape = p2_input
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
    
    return f"""You are a data scientist trying to create a regression experiement in R. Considering a dataset located at {DATA_PATH} with the following properties:
    {dataset_properties_string}
    create a regression experiment in which the variable '{target}' can be predicted from the other variables.
    Use the most appropriate regression algorithm.
    """
    

def main():
    #pp.pprint(p2(p1(DATA_PATH)))
    print(p2(p1(DATA_PATH)))
    



if __name__ == "__main__":
    main()



