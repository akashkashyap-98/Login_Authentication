# from myapp.models import EmployeeSecondDB 

# class SecondaryDatabaseRouter:
#     def db_for_read(self, model, **hints):
#         if model == EmployeeSecondDB:
#             return 'second_db'
#         return None

#     def db_for_write(self, model, **hints):
#         if model == EmployeeSecondDB:
#             return 'second_db'
#         return None

#     def allow_relation(self, obj1, obj2, **hints):
#         if (
#             obj1.__class__ == EmployeeSecondDB and
#             obj2.__class__ == EmployeeSecondDB
#         ):
#             return True
#         return None

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         if app_label == 'myapp' and model_name == 'EmployeeSecondDB':
#             return db == 'second_db'
#         return None






