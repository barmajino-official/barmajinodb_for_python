import json, re, os

class barmajinodb(object):
    """description of class"""
    def __init__(self,db_file_path=None):
        self.db_file_path = db_file_path
        if(os.path.isfile(self.db_file_path) == False):
            with open(self.db_file_path, "w") as jsonFile:
                json.dump({}, jsonFile)

    def _open(self):
        with open(self.db_file_path, "r") as jsonFile:
            data = json.load(jsonFile)
        return data

    def get_tables_name(self):
        data = self._open()
        tables = [i for i in data]
        return tables

    def get(self, table = None, select = "All", where = 'True', res_type = None):
        data = self._open()
        new_temp_data = data
        if(table not in data):
            return (f"Error: table name '{table}' not exist in data base")
        data = data[table]
        data.pop("id_counter")
        
        """
        if type of 'select' is str and equale to "All" so the system well return all data
        if 'res_type' equale to "list" the result well return by list with out data key example ["ali", "jaafar","barmajino"]
        if 'res_type' equale to "tuple" the result well return by tuple with out data key example ("ali", "jaafar","barmajino")
        if 'res_type' equale to "dictionary" the result well return by dictionary with data key example
       {
        "first_name": "Ali",
        "last_name": "Jaafar",
        "username": "barmajino"
       }

        """ 
        where_tmp = where
        if(where != 'True'):
            pattern = r'or|and'
            pattern2 = r'==|!=|not in|in|\''
            result = re.split(pattern, where_tmp.replace("\"","'").replace('type(\'',""))
            result_list = [re.split(pattern2, result_)[0].split()[0] for result_ in result]

        if(res_type == "list" or res_type == "tuple"):
            results = []
            for id_x in data:
                result_temp_data_list = []
                try:
                    the_testing_where_result = bool(True in (x.replace("type(", "").replace(")","") in data[id_x].keys() for x in result_list))
                except:
                    the_testing_where_result = 1
                if(the_testing_where_result or where == "True"):
                    if(eval(f"""%condition%""".replace("%condition%", where), data[id_x])):
                        if(select != "All"):
                            if("id" in select): result_temp_data_list = [id_x]
                            for result_temp_data_ in select:
                                if(result_temp_data_ != 'id'):
                                    result_temp_data_list.append(data[id_x][result_temp_data_])
                        else:
                            result_temp_data_list = [id_x]
                            for result_temp_data_ in data[id_x]:
                                if('__builtins__' != result_temp_data_):
                                    result_temp_data_list.append(data[id_x][result_temp_data_])
                        if(res_type == "tuple"): results.append(tuple(result_temp_data_list))
                        else:
                            results.append(result_temp_data_list)
                else:
                    for x in result_list:
                        if(x not in data[id_x].keys()):
                            if("type(" in x): x = x.replace("type(", "").replace(")","")
                            return (f"Error : '{x}' is not defind")
           
            if(res_type == "tuple"):
                results = tuple(results)
            
        elif(res_type == "dictionary"):  
            results = {}
            for id_x in data:
                result_temp_data_list = []
                try:
                    the_testing_where_result = bool(True in (x.replace("type(", "").replace(")","") in data[id_x].keys() for x in result_list))
                except:
                    the_testing_where_result = 1
                if(the_testing_where_result or where == "True"):
                    if(eval(f"""%condition%""".replace("%condition%", where), data[id_x])):
                        if(select != "All"):
                            if("id" in select): new_temp_data[table][id_x].update({"id": id_x})
                            for i in data[id_x].copy():
                                if(i not in select) :
                                    new_temp_data[table][id_x].pop(i)
                        else:
                            new_temp_data[table][id_x].update({"id": id_x})
                else:
                    for x in result_list:
                        if(x not in data[id_x].keys()):
                            if("type(" in x): x = x.replace("type(", "").replace(")","")
                            return (f"Error : '{x}' is not defind")
                            
                results[id_x] = data[id_x]
        return results
        
    def update(self, table = None, where = 'True', set_value = None):
        where_tmp = where
        data = self._open()
        if(table not in data):
            return (f"Error: table name '{table}' not exist in data base")
        data_ = self.get(table = table, res_type = "dictionary", select = "All", where = 'True',)
        a = {}
        for i in data_:
            a[i] = {}
            a[i]['self'] = self
            for ii in data_[i]:
                exec(f'a[i][ii] = data[i][ii]', {'a' : a, "data":data_, "i":i,"ii":ii})
        for i in a:
            the_testing_where_result = True
            if(where != 'True'):
                pattern = r'or|and'
                pattern2 = r'==|!=|not in|in|\''
                
                result = re.split(pattern, where_tmp.replace("\"","'").replace('type(\'',""))
                result_list = [re.split(pattern2, result_)[0].split()[0] for result_ in result]
                the_testing_where_result = bool(True in (x in a[i].keys() for x in result_list))
            if(the_testing_where_result):
                try:
                    if(eval("%condition%".replace("%condition%", where),a[i])):
                        return (self.updating_(table = table, set_value = set_value, id = a[i]['id']))
                except Exception as error:
                    print(f"Error : {error}")
            else:
                for x in result_list:
                    if(x not in a[i].keys()):
                        return (f"Error : '{x}' is not defind")

    def updating_(self, table = None, set_value = None, id = None):
        data = self._open()

        for i,y in set_value.items():
                data[table][id][i] = y
                if(y == 'sys001'):
                    data[table][id].pop(i)

        with open(self.db_file_path, "w") as jsonFile:
            json.dump(data, jsonFile)
        return "updating Done"

    def add(self, table = None, input_data = None):
        data = self._open()
        if(table not in data):
            return (f"Error: table name '{table}' not exist in data base")
        if(data[table]['id_counter'] == None):
            data[table]['id_counter'] = 0
            id_x = 0
        else:
            id_x = data[table]['id_counter']+1
        data[table][f"id_{id_x}"] = {}
        for i,y in input_data.items():
                data[table][f"id_{id_x}"][i] = y
        data[table]['id_counter'] = id_x
        with open(self.db_file_path, "w") as jsonFile:
            json.dump(data, jsonFile)

    def create(self, name = None, ):
        data = self._open()
        if(name not in data):
            data[name] = {'id_counter' : None}
            with open(self.db_file_path, "w") as jsonFile:
                json.dump(data, jsonFile)

    def delete(self, name = None, ):
        data = self._open()
        data.pop(name)
        with open(self.db_file_path, "w") as jsonFile:
            json.dump(data, jsonFile)
        return True

    def drop(self, table = None, where = None):
        data = self._open()
        data_ = self.get(table = table, res_type = "dictionary", select = "All", where = 'True',)
        where_tmp = where
        pattern = r'or|and'
        pattern2 = r'==|!=|not in|in|\''
        
        result = re.split(pattern, where_tmp.replace("\"","'").replace('type(\'',""))
        result_list = [re.split(pattern2, result_)[0].split()[0] for result_ in result]
        for i in data_:
            the_testing_where_result = bool(True in (x in data_[i].keys() for x in result_list))
            if(the_testing_where_result):
                try:
                    if('__builtins__' in data[table][i]): data[table][i].pop('__builtins__')
                    
                    if(eval("%condition%".replace("%condition%", where),data[table][i])):
                        data[table].pop(i)
                        with open(self.db_file_path, "w") as jsonFile:
                            json.dump(data, jsonFile)
                except Exception as error:
                    return(f"Error : {error}")
            else:
                for x in data:
                    if(x not in data[i].keys()):
                        return (f"Error : '{x}' is not defind") 
        return f"drop successfully 100%"
            
            
            
            







