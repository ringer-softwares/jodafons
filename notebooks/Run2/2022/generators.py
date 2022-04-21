#__all__ = ['generator_v8']

import numpy as np

def generator_v8( df ):
    columns= ['trig_L2_cl_ring_%d'%i for i in range(100)]
    rings = df[columns].values.astype(np.float32)
    def norm1( data ):
        norms = np.abs( data.sum(axis=1) )
        norms[norms==0] = 1
        return data/norms[:,None]
    rings = norm1(rings)
    return [rings]


def generator_v9( df ):

    col_names= ['trig_L2_cl_ring_%d'%i for i in range(100)]
    rings = df[col_names].values.astype(np.float32)
    def norm1( data ):
        norms = np.abs( data.sum(axis=1) )
        norms[norms==0] = 1
        return data/norms[:,None]
    
    data_rings = norm1(rings)
    n = data_rings.shape[0]
    data_reta   = df['trig_L2_cl_reta'].astype(np.float32).to_numpy().reshape((n,1))  / 1.
    data_eratio = df['trig_L2_cl_eratio'].astype(np.float32).to_numpy().reshape((n,1))  / 1.
    data_f1     = df['trig_L2_cl_f1'].astype(np.float32).to_numpy().reshape((n,1))  / 0.6
    data_f3     = df['trig_L2_cl_f3'].astype(np.float32).to_numpy().reshape((n,1))  / 0.04
    data_weta2  = df['trig_L2_cl_weta2'].astype(np.float32).to_numpy().reshape((n,1))  / 0.02
    data_wstot  = df['trig_L2_cl_wstot'].astype(np.float32).to_numpy().reshape((n,1))  / 1.
    # Fix all shower shapes variables
    data_eratio[data_eratio>10.0]=0
    data_eratio[data_eratio>1.]=1.0
    data_wstot[data_wstot<-99]=0
    data_shower = np.concatenate( (data_reta,data_eratio,data_f1,data_f3,data_weta2, data_wstot), axis=1)

    return [data_rings,data_shower]


def generator_v10( df ):
    return generator_v8(df)


def generator_v11( df ):
    return generator_v9(df)


def generator_v12( df ):

    # for new training, we selected 1/2 of rings in each layer
    #pre-sample - 8 rings
    # EM1 - 64 rings
    # EM2 - 8 rings
    # EM3 - 8 rings
    # Had1 - 4 rings
    # Had2 - 4 rings
    # Had3 - 4 rings
    prefix = 'trig_L2_cl_ring_%i'

    # rings presmaple 
    presample = [prefix %iring for iring in range(8//2)]
    # EM1 list
    sum_rings = 8
    em1 = [prefix %iring for iring in range(sum_rings, sum_rings+(64//2))]
    # EM2 list
    sum_rings = 8+64
    em2 = [prefix %iring for iring in range(sum_rings, sum_rings+(8//2))]
    # EM3 list
    sum_rings = 8+64+8
    em3 = [prefix %iring for iring in range(sum_rings, sum_rings+(8//2))]
    # HAD1 list
    sum_rings = 8+64+8+8
    had1 = [prefix %iring for iring in range(sum_rings, sum_rings+(4//2))]
    # HAD2 list
    sum_rings = 8+64+8+8+4
    had2 = [prefix %iring for iring in range(sum_rings, sum_rings+(4//2))]
    # HAD3 list
    sum_rings = 8+64+8+8+4+4
    had3 = [prefix %iring for iring in range(sum_rings, sum_rings+(4//2))]
    col_names = presample+em1+em2+em3+had1+had2+had3
    rings = df[col_names].values.astype(np.float32)

    def norm1( data ):
        norms = np.abs( data.sum(axis=1) )
        norms[norms==0] = 1
        return data/norms[:,None]
    
    data_rings = norm1(rings)
    return [data_rings]


def generator_v13( df ):

    # for new training, we selected 1/2 of rings in each layer
    #pre-sample - 8 rings
    # EM1 - 64 rings
    # EM2 - 8 rings
    # EM3 - 8 rings
    # Had1 - 4 rings
    # Had2 - 4 rings
    # Had3 - 4 rings
    prefix = 'trig_L2_cl_ring_%i'

    # rings presmaple 
    presample = [prefix %iring for iring in range(8//2)]
    # EM1 list
    sum_rings = 8
    em1 = [prefix %iring for iring in range(sum_rings, sum_rings+(64//2))]
    # EM2 list
    sum_rings = 8+64
    em2 = [prefix %iring for iring in range(sum_rings, sum_rings+(8//2))]
    # EM3 list
    sum_rings = 8+64+8
    em3 = [prefix %iring for iring in range(sum_rings, sum_rings+(8//2))]
    # HAD1 list
    sum_rings = 8+64+8+8
    had1 = [prefix %iring for iring in range(sum_rings, sum_rings+(4//2))]
    # HAD2 list
    sum_rings = 8+64+8+8+4
    had2 = [prefix %iring for iring in range(sum_rings, sum_rings+(4//2))]
    # HAD3 list
    sum_rings = 8+64+8+8+4+4
    had3 = [prefix %iring for iring in range(sum_rings, sum_rings+(4//2))]
    col_names = presample+em1+em2+em3+had1+had2+had3
    rings = df[col_names].values.astype(np.float32)

    def norm1( data ):
        norms = np.abs( data.sum(axis=1) )
        norms[norms==0] = 1
        return data/norms[:,None]

    data_rings = norm1(rings)
    n = data_rings.shape[0]
    data_reta   = df['trig_L2_cl_reta'].astype(np.float32).to_numpy().reshape((n,1))  / 1.
    data_eratio = df['trig_L2_cl_eratio'].astype(np.float32).to_numpy().reshape((n,1))  / 1.
    data_f1     = df['trig_L2_cl_f1'].astype(np.float32).to_numpy().reshape((n,1))  / 0.6
    data_f3     = df['trig_L2_cl_f3'].astype(np.float32).to_numpy().reshape((n,1))  / 0.04
    data_weta2  = df['trig_L2_cl_weta2'].astype(np.float32).to_numpy().reshape((n,1))  / 0.02
    data_wstot  = df['trig_L2_cl_wstot'].astype(np.float32).to_numpy().reshape((n,1))  / 1.
    # Fix all shower shapes variables
    data_eratio[data_eratio>10.0]=0
    data_eratio[data_eratio>1.]=1.0
    data_wstot[data_wstot<-99]=0
    data_shower = np.concatenate( (data_reta,data_eratio,data_f1,data_f3,data_weta2, data_wstot), axis=1)

    return [data_rings,data_shower]


def generator_v14(df):
    return generator_v12(df)

def generator_v15(df):
    return generator_v13(df)


def generator_v16(df):


    def reshape_to_vortex( input_data):
    
        # NOTE: Do not change this if you dont know what are you doing
        frame =     [ [72,73,74,75,76,77,78,79,80,81],
                      [71,42,43,44,45,46,47,48,49,82],
                      [70,41,20,21,22,23,24,25,50,83],
                      [69,40,19,6 ,7 ,8 ,9 ,26,51,84],
                      [68,39,18,5 ,0 ,1 ,10,27,52,85],
                      [67,38,17,4 ,3 ,2 ,11,28,53,86],
                      [66,37,16,15,14,13,12,29,54,87],
                      [65,36,35,34,33,32,31,30,55,88],
                      [64,63,62,61,60,59,58,57,56,89],
                      [99,98,97,96,95,94,93,92,91,90],
                    ]
        from copy import deepcopy
        zeros_to_complete = np.zeros((input_data.shape[0],100-input_data.shape[1]))
        data = deepcopy(np.hstack([input_data, zeros_to_complete]))
        d = deepcopy(data.reshape( 1,10,10,data.shape[0] ))
        data=data.T
        for i in range(10):
            for j in range(10):
                d[0][i][j][::] = data[ frame[i][j] ][::]
        d=d.T
        return d
   
    def norm1( data ):
        norms = np.abs( data.sum(axis=1) )
        norms[norms==0] = 1
        return data/norms[:,None]
    
    col_names= ['trig_L2_cl_ring_%d'%i for i in range(100)]
    rings = df[col_names].values.astype(np.float32)
    data_rings = norm1(rings)
    data_rings = reshape_to_vortex(data_rings)
    return [data_rings]