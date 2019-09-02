import os 
import ta_helper.cloner as cloner

hw = 'hw1'
semester = 'ML2019SPRING'
hw_path = '/home/caleb/ML'

users = cloner.get_users(semester)

for user in users:
    cloner.clone_folder(user, semester, hw, hw_path)
