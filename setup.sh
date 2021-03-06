#Flask variables
export FLASK_ENV='development'
export FLASK_APP='app.py'
export FLASK_RUN_PORT=5000
export FLASK_RUN_HOST=localhost

#Auth0 variables
export AUTH0_DOMAIN='dev-juanchete.eu.auth0.com'
export DATABASE_URL='postgresql://jrbuleo:vacaburra@localhost:5433/videogames'
export API_AUDIENCE='videoGamesAPI'
export CLIENT_ID='VpsuaVE5l6k5XnV0E2fd75aZHzVv676V'
export REDIRECT_URI="http://$FLASK_RUN_HOST:$FLASK_RUN_PORT/login-results"
export REDIRECT_LOGIN="http://$FLASK_RUN_HOST:$FLASK_RUN_PORT/login"

#Test variables for unittest 
export TOKEN_ROLE_USER='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldhbVBQOUtXZnZwYjc5QUg0SlFJcyJ9.eyJpc3MiOiJodHRwczovL2Rldi1qdWFuY2hldGUuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWM3ZDRhNjdlODc0MGMxZWRlMGNmOSIsImF1ZCI6InZpZGVvR2FtZXNBUEkiLCJpYXQiOjE1ODc0ODQwMTMsImV4cCI6MTU4NzQ5MTIxMywiYXpwIjoiVnBzdWFWRTVsNms1WG5WMEUyZmQ3NWFaSHpWdjY3NlYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpjYXRlZ29yaWVzIiwiZ2V0OnN0dWRpb3MiLCJnZXQ6dmlkZW9nYW1lcyJdfQ.ZQsrmABtBdN5WgMwkwA6DIQHmaR_XnClp5tA8044He7vUNDODCp8uIKetSy5BTPar8cxGZC5yvmMu-zVDIwvuie9UWS4ri82Tw4ynlicshVRIyJl_7CxAnHkbHtdE5ydjJ0a69SWZI0GPx_82J6TsMDCMjX_miWKLClUOuNpWVzzfTTE9VKIjj-LHz22EnVzz5Bpv5wSfFokA14ffuRzUUx-8lltpdx5NK0fzorMI2A-jKQA7RVWdJEPVkP5N6sxSgzLHMDbZK7GMt0S33kLYzxd7LiaXdPBetwV9r5e9ZHrdXiOe8kZBfc2mh3PiGY4nqQdkgkeipffR26qJitE5w'
export TOKEN_ROLE_STUDIO='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldhbVBQOUtXZnZwYjc5QUg0SlFJcyJ9.eyJpc3MiOiJodHRwczovL2Rldi1qdWFuY2hldGUuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWM3ZDcyNjg0YTAxMGMyMjg5ODVjMSIsImF1ZCI6InZpZGVvR2FtZXNBUEkiLCJpYXQiOjE1ODc0ODQwNjIsImV4cCI6MTU4NzQ5MTI2MiwiYXpwIjoiVnBzdWFWRTVsNms1WG5WMEUyZmQ3NWFaSHpWdjY3NlYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTp2aWRlb2dhbWVzIiwiZ2V0OmNhdGVnb3JpZXMiLCJnZXQ6c3R1ZGlvcyIsImdldDp2aWRlb2dhbWVzIiwicGF0Y2g6c3R1ZGlvcyIsInBhdGNoOnZpZGVvZ2FtZXMiLCJwb3N0OnZpZGVvZ2FtZXMiXX0.iZ9Rwf9LAvPAZYq68HA1Bt57YmUyY7DwXOuTURlz_5KnCN2lc-1evnW19rdE9Cbob7M-G0TXyqu2TuHnKxjkx0twW4qJUnXIRwkPNX2LioBdTzit_JOaAQEBNcg1aHMXOo2lII5A4E1BaHyNLOTXR1LnQRDx2VFdjWxcfEx0YJXq4yLvNIyWWbgGBcQzyvuj8In5rys5Y5otLZyPXVq4EeG2E2PKad9vbGN9UM8m_PfGGIs9skCXu9qCMo-PHpnaXNCz7n_kSSU4s_2Suw75NdTCAnaE8SSqa5vhfYWBWuvgstIeAaANJb2j7O0A6AGQn8Ms0mk0h6QwrsjIEw_reg'
export TOKEN_ROLE_MANAGER='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldhbVBQOUtXZnZwYjc5QUg0SlFJcyJ9.eyJpc3MiOiJodHRwczovL2Rldi1qdWFuY2hldGUuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOWM3ZDk4OWI0MzU4MGMxZTAwODEwOCIsImF1ZCI6InZpZGVvR2FtZXNBUEkiLCJpYXQiOjE1ODc0ODM5ODQsImV4cCI6MTU4NzQ5MTE4NCwiYXpwIjoiVnBzdWFWRTVsNms1WG5WMEUyZmQ3NWFaSHpWdjY3NlYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjYXRlZ29yaWVzIiwiZGVsZXRlOnN0dWRpb3MiLCJkZWxldGU6dmlkZW9nYW1lcyIsImdldDpjYXRlZ29yaWVzIiwiZ2V0OnN0dWRpb3MiLCJnZXQ6dmlkZW9nYW1lcyIsInBhdGNoOmNhdGVnb3JpZXMiLCJwYXRjaDpzdHVkaW9zIiwicGF0Y2g6dmlkZW9nYW1lcyIsInBvc3Q6Y2F0ZWdvcmllcyIsInBvc3Q6c3R1ZGlvcyIsInBvc3Q6dmlkZW9nYW1lcyJdfQ.H7wlbmzPaPW7BxMY0xDbc4fGgOfAHMim7blopzVdVbJSK8A-HrluMQSczUmjUi42lE3x5wA2OoQGO1Y7zIIavuum69Xhe4rPn8fDBCjzGEWd1A3BpaKQ_dGPR-BvTgKkkvZBV9yCQ56movbYyc6Waj9SKzSrW6WBq0-1QiC2UARADuwUs6gj-QkMMOQLIgeKZikwEPIG6Zg6Yhgy5IO-wr8qJTzI6kBJqfrA-GU7KF6PFBhe61VZ9-9xV2TuHiJ7xK-ZuU3qQ3T91k5tDRk9E-RyVbIc-J_--KBAZJY_bEBIa9IMksNgVt814FptFPH45lhH27SC7s-4MJlWwNwzHg'

#Application variable por pagination
export VIDEOGAMES_PER_PAGE=5

