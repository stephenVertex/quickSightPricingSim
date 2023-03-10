
import random
import datetime
from collections import Counter
import statistics

acct_types = {
    "author_ent"     : 24,
    "author_ent_q"   : 34,
    "author_std"     : 9
}

class QuicksightUser:
    def __init__(self, user_creation_month, active_to_inactive_probability, acct_type, user_id):
        self.user_creation_month            = user_creation_month
        self.active_to_inactive_probability = active_to_inactive_probability
        self.acct_type                      = acct_type
        self.user_id                        = user_id
        #self.status_history                 = ["active"]
        self.status_history = { user_creation_month : "active" }

    def __repr__(self):

        max_month = max(self.status_history.keys())
        cur_status = self.status_history[max_month]
        # n_active = len(filter(lambda x: x == "active", self.status_history.values()))

        return(f"User: {self.user_id}, history: {cur_status}")

    def simulate_next_month(self, time_to_removal = 999999):
        """Simulates one month passing and updates the user's active status."""
        
        sh_max_month = max(self.status_history.keys())
        sh_ttr = max(1, sh_max_month - time_to_removal + 1)

        if self.status_history[sh_max_month] == "active":
            if random.random() < self.active_to_inactive_probability:
                self.status_history[sh_max_month + 1] = "inactive"
            else:
                self.status_history[sh_max_month + 1] = "active"
                

        else:
            if (len(self.status_history) > time_to_removal) and (all( [self.status_history[i] == "inactive" for i in range(sh_ttr, sh_max_month + 1)])):
                
                self.status_history[sh_max_month + 1] = "removed"
            else:
                self.status_history[sh_max_month + 1] = self.status_history[sh_max_month]



def count_values(lst):
    # create a Counter object from the list
    count = Counter(lst)
    # return a dictionary with the counts
    return dict(count)

class QSUCollection():
    def new_user(self):
        user_id = "user-" + str(len(self.users))
        nu = QuicksightUser(self.current_month,
                            self.active_to_inactive_probability,
                            self.acct_type,
                            user_id
                            )
        self.users.append(nu)
                            

    def __init__(self,
                 active_to_inactive_probability,
                 acct_type,
                 current_month,
                 N_users = 10,
                 N_new_users_per_month = 5,
                 time_to_removal = 999999
                 ):        
        self.active_to_inactive_probability = active_to_inactive_probability
        self.acct_type = acct_type
        self.current_month = current_month
        self.users = []
        self.N_new_users_per_month = N_new_users_per_month
        self.time_to_removal = time_to_removal
        for i in range(N_users):
            self.new_user()


    def forward_simulate(self, T):

        for t in range(T):
            print("--------------------")
            self.current_month = self.current_month + 1
            print(f"CURRENT MONTH: {self.current_month}")


            ## --------------------------------------------------
            ## For each of the current users,
            ##       simulate the next month.
            N_users = len(self.users)
            for i in range(N_users):
                #print(self.users[i])
                self.users[i].simulate_next_month(time_to_removal=self.time_to_removal)
        

            ## ----------------------------------------
            ## Adding new users.
            print(f"Adding {self.N_new_users_per_month} new users")
            for i in range(self.N_new_users_per_month):
                self.new_user()
        
            N_users = len(self.users)
            print(f"Number of users: {N_users}")

    def get_cost(self, m_v):
        monthly_costs = float ( (m_v['active'] + m_v['inactive'] ) * acct_types[self.acct_type])
        return(monthly_costs)

    def get_data(self):
        ## we want to get the number of active, inactive, and removed
        dlist = []
        for m in range(1, self.current_month + 1):
            ## get the current users, where user_creation_month <= self.current_month
            m_users = list(filter(lambda x: x.user_creation_month <= m, self.users))
            
            ## each get the status of each user
            m_status = [u.status_history[m] for u in m_users]  

            m_v = count_values(m_status)
            m_v['month'] = m
            m_v['time_to_removal'] = self.time_to_removal

            for d_key in ['inactive', 'removed']:
                if d_key not in m_v:
                    m_v[d_key] = 0

            m_v['billed_users'] = m_v['active'] + m_v['removed']
            m_v['cost'] = self.get_cost(m_v)

            dlist.append(m_v)
            

        return(dlist)


    def print_users_active_run(self):
        for u in self.users:
            print(count_values(list(u.status_history.values())))


    def summarize_user_data(self):
        cdx = [count_values(u.status_history.values()) for u in self.users]
        n_active = [ud['active'] for ud in cdx]
        d = self.get_data()

        r = {'avg_active' : statistics.mean(n_active),
             'sd_active' : statistics.stdev(n_active),
             'min_active' : min(n_active),
             'max_active' : max(n_active),
             'peak_active' : max([x['active'] for x in d[1:]])
             }
                    

        return(r)
