import barmajinodb as db



db = db.barmajinodb(db_file_path = "data\\mydata1.json")


db.create("users")

val = {
    'firstname' : "Ali",
    'lastname' : "Jaafar",
    'Age' : 30
    }
results = db.add(table = 'users', input_data = val)
print(f"add : {results}")

tables = db.get_tables_name()

print(f"tables : {tables}")


results = db.get(
    table = 'users',
    where = "type(Age) == int",
    res_type = "dictionary",
    select = ['id','firstname'])#'res_type' weel by equale one of this thre type of data (list, tuple, dictionary) 

print(f"get : {results}")

val = {
    "okok" : '9',
    }
results = db.update(table = 'users', where = "Age == 30", set_value = val)
print(f"update : {results}")

#results = db.drop(table = 'users', where = "Age == 30")
#print(f"drop : {results}")

#results = db.delete(name = 'users')
#print(results)


#print(len([ii for i in open("barmajinodb.py").read().split(" ") for ii in i.split("\n")])) == 3555
