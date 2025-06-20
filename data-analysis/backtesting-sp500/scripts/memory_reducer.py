import numpy as np

# optimize the types to reduce its size and returns a memory optimized DataFrame.
def memory_reducer(df):
    for col in df.columns:
        # check if is numeric column
        if np.issubdtype(df[col], np.number):

            # check if it can be convert to integer
            if (df[col].dropna() == df[col].dropna().astype(int)).all():
                min = int(df[col].min())
                max = int(df[col].max())

                # Determine and apply the smallest datatype that can fit the range of values
                best_datatype = smallest_datatype(min, max)
                df[col] = df[col].astype(best_datatype)
    
            elif (df[col].dropna() == df[col].dropna().astype(float)).all():
                df[col] = df[col].astype(np.float32)

    return df

# Determine and apply the smallest datatype that can fit the range of values
def smallest_datatype(min, max):
    min_type = np.min_scalar_type(min)
    max_type = np.min_scalar_type(max)

    if min >= 0 or (min < 0 and max < 0):
        datatype = max_type
    elif max_type.itemsize >= min_type.itemsize:
        datatype = np.min_scalar_type(-1*max)

    return datatype