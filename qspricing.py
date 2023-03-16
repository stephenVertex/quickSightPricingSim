#!/usr/bin/env python3

import sim
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



qcol_6m = sim.QSUCollection(active_to_inactive_probability = 0.3,
                            acct_type = "author_ent",
                            current_month = 1,
                            N_users = 50,
                            time_to_removal = 6)
qcol_6m.forward_simulate(24)
d_6m = qcol_6m.get_data()
ud_6m = qcol_6m.summarize_user_data()

####################

qcol_3m = sim.QSUCollection(active_to_inactive_probability = 0.3,
                            acct_type = "author_ent",
                            current_month = 1,
                            N_users = 50,
                            time_to_removal = 3)
qcol_3m.forward_simulate(24)
d_3m = qcol_3m.get_data()
ud_3m = qcol_3m.summarize_user_data()

###################


qcol_1m = sim.QSUCollection(active_to_inactive_probability = 0.3,
                            acct_type = "author_ent",
                            current_month = 1,
                            N_users = 50,
                            time_to_removal = 1)
qcol_1m.forward_simulate(24)
d_1m  = qcol_1m.get_data()
ud_1m = qcol_1m.summarize_user_data()

##############################


pd_large = pd.DataFrame(d_6m + d_3m + d_1m)


# Set the plotting style
sns.set_style('whitegrid')


# Create the time series plot
sns.lineplot(x='month', y='cost', hue='time_to_removal', 
             legend='full', 
             data=pd_large)


# Show the plot
plt.show()


