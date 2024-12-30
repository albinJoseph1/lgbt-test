import s
from s import handle_scrap_deletion_and_pr_creation

cn="Baker McKenzie"
created, responce = handle_scrap_deletion_and_pr_creation(cn)
print(responce)
# cf= find_company_folder(cn)

# if cf:
#     # r=process_company(cf)
#     # r=process_company(cn+'Marstons')
#     # if success:
#     #     print(value)
#     #     create_pr(value, s.access_token)
#     #     print(success)
#     # else:
#     #     print(value)
# else:
#     print('cf not')