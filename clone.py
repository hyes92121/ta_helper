import os 
import ta_helper.cloner as cloner

hw = 'hw1'                 # which HW to clone 
semester = 'ML2019SPRING'  # current semester 
hw_path = '/home/caleb/ML' # path to store all student repos 

# make sure that the path to data storage exists
if not os.path.exists(hw_path):
    os.mkdir(hw_path)
if not os.path.exists(f'{hw_path}/{hw}'):
    os.mkdir(f'{hw_path}/{hw}')

# get all users that has invited the TA
users = cloner.get_users(semester)

# clone the specified HW folder to the target directory 
for user in users:
    cloner.clone_folder(user, semester, hw, hw_path)
