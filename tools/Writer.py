import csv
import pathlib
import threading

class Writer():
    def __init__(self, filename):
        self.filename = filename
        self._lock = threading.Lock()

    def write(self, house_data, columns):
        try:
            file_to_check = pathlib.Path(self.filename)
            if file_to_check.exists():
                #using existing file
                
                with open(self.filename, 'a', newline='', encoding='utf-8') as file:
                    with self._lock:
                        writer = csv.writer(file)
                        writer.writerow(house_data.values())
                self.filename.close()    
            
            else:
                #column_names = house_data.keys()
                #creating a new file
                with open(self.filename, 'a', newline='', encoding='utf-8') as file:
                    with self._lock:
                        writer = csv.DictWriter(file, fieldnames=columns)
                        writer.writeheader()
                        writer.writerow(house_data.values()) 
                self.filename.close()

            return True
        except:
            return False

    def write_list(self, data_list):
        file_to_check = pathlib.Path(self.filename)
        if file_to_check.exists():
            print('using existing file..')
            with open(self.filename, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for data in data_list:
                    writer.writerow(vars(data).values())    
        
        else:
            first = vars(data_list[0])
            column_names = first.keys()
            print('creating a new file..')
            with open(self.filename, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=column_names)
                writer.writeheader()
                for data in data_list:
                    writer.writerow(vars(data)) 
        
        print('done writing to file..')