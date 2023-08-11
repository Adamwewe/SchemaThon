import warnings

from utils_loading import spot_id

from typing import Dict, List, Callable, Tuple

def schemaFormatter(items: Dict[str, List[str]], 
                    relationships: List[str]) -> Dict[str, Dict[str, List[Tuple[str]]]]:
    """
    tba, use type hints for now
    """

    schema = {}
    schema["child_less"] = []
    
    for parent, child, col in relationships:  # this can be moved to the loop below but we miss the logging opportunity of missed tables
        schema[parent] = {"children" : []}

    
    for parent, child, col in relationships:
        schema[parent]["children"].append((child, col))

    
    schema_check = items.keys() - schema.keys()
    if schema_check:
        warnings.warn("Table {} has no children!!".format(schema_check))
        schema["child_less"] = list(schema_check)
        

    return schema



def searchGraphV2(items: Dict[str, List[str]], threshold: float=0.7, 
                  funcFormat: Callable[[List[str]], Dict[str, List[str]]]=schemaFormatter, 
                  funcRegex:Callable[[str], bool] =spot_id) -> Dict[str, List[str]]:

    """
    tba, use type hints for now
    """
    
    rela = []

    for t1_n, t1_d in items.items():
        for t2_n, t2_d in items.items():
            
            if t1_n != t2_n:
                common_col = set(t1_d.columns) & set(t2_d.columns)
                #print(common_col)
                
                if len(common_col) > 0:
                    for col in common_col:
                        warnings.warn("Add helper cardinality func here")
                        # more rows == intermediate. Think about adding row count score for intermediate tables and childless

                        # calculate jaccard index with a twist (intersection over union with a twist)
                            # mask with cardinality normalization missing in this implementation
                        intersection = set(t1_d[col]) & set(t2_d[col])
                        union = set(t1_d[col]) | set(t2_d[col])
                        similarity = len(intersection)/ len(union)
                        #print("Tables: {} and {} using Key {} have score of {}".format(t1_n, t2_n, col, similarity))
                        if similarity > threshold:
                            if funcRegex(col):  #to avoid duplicates
                                relationship = (t1_n, t2_n, col)
                                rela.append(relationship)
    schema = funcFormat(items, rela)
    return schema 

