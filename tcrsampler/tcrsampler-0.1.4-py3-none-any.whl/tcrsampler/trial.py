
import pandas as pd

use_frequency = True
if use_frequency:
  col = 'freq'
else:
  col = 'count'

fn = 'britanova_chord_blood.csv'
dfg =df.groupby(['v_reps','j_reps'])
df = pd.read_csv(fn)
dfg =df.groupby(['v_reps','j_reps'])

dfgs = dfg[col].sum().reset_index()
t.ref_df.groupby(['v_reps','j_reps'])['freq'].sum().rese)t_index()
asesrt np.divide(vj.freq,vj.freq.sum()).sum() == 1
vj = vj.assign(freq = np.divide(vj.freq,vj.freq.sum()))


# There are two method of providing v_j stats.
# The frequency method 

# The unique clones method
