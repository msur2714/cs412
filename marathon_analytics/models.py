from django.db import models

# Create your models here.

class Result(models.Model):
    '''Store/represent the data from one runner at the Chicago Marathon 2023.
     
       Data attributes: BIB, First Name, Last Name, CTZ, City, State, Gender,Division,
                     Place Overall, Place Gender, Place Division, Start TOD, Finish TOD,
                     Finish, HALF1, HALF2'''
    
    # identification
    bib = models.IntegerField()
    first_name = models.TextField()
    last_name = models.TextField()
    ctz = models.TextField()
    city = models.TextField()
    state = models.TextField()

    # gender/division
    gender = models.CharField(max_length=6)
    division = models.CharField(max_length=6)

    # result place
    place_overall = models.IntegerField()
    place_gender = models.IntegerField()
    place_division = models.IntegerField()

    # timing-related
    start_time_of_day = models.TimeField()
    finish_time_of_day = models.TimeField()
    time_finish = models.TimeField()
    time_half1 = models.TimeField()
    time_half2 = models.TimeField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} ({self.city}, {self.state}), {self.time_finish}'
    
def load_data(): 
    '''Load data records from a CSV file into model instance'''

    # delete all records: clear out the database 
    Result.objects.all().delete()
    
    # open the file for reading: 
    filename ='/Users/MirutikkaS/Downloads/2023_chicago_results.csv'

    f = open(filename)
    headers = f.readline() #read/discard the headers 
    # print(headers)
    # line = f.read() #read a line for processing
    # fields = line.split(',') #create a list of fields 
    # print(fields)

    # show the elements in this list of fields with the index number
    # for i in range(len(fields)): 
    #     print(f'fields[{i}] = {fields[i]}')

    # loop to read all the lines in the file
    for line in f: 
        
        # provide protection around code that might have an exception
        try: 
            fields = line.split(',')

            # create a new instance of Result object with this record from CSV
            result = Result(bib=fields[0],
                            first_name=fields[1],
                            last_name=fields[2],
                            ctz = fields[3],
                            city = fields[4],
                            state = fields[5],
                                    
                            gender = fields[6],
                            division = fields[7],
                            place_overall = fields[8],
                            place_gender = fields[9],
                            place_division = fields[10],
                                
                            start_time_of_day = fields[11],
                            finish_time_of_day = fields[12],
                            time_finish = fields[13],
                            time_half1 = fields[14],
                            time_half2 = fields[15],
                        )
                
            result.save() # commit to database - save this instance to the database
            print(f'Created result: {result}')
        
        except: 
            print(f"Exception on {fields}")
