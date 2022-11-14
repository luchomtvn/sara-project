def poderate_avg(profiles, property, limit):
    col = property + '_value_avg'
    if(profiles['upper_depth'] > limit):
        return 0.0 

    if(profiles['lower_depth'] > limit):
        partial_depth = limit - profiles['upper_depth']
        return (partial_depth * profiles[col])/limit
    else:
        return ((profiles['lower_depth'] - profiles['upper_depth']) * profiles[col])/limit

def get_profile_summary(df, property):
    prop_pond_col = property + '_pond_val'
    df[prop_pond_col] = df.apply(poderate_avg, args=(property, 30), axis=1)
    return df[['profile_id', 'country_name', prop_pond_col]].groupby(['profile_id', 'country_name']).sum().reset_index()