from django.db import models

# Create your models here.
import csv
from django.utils.dateparse import parse_date
from datetime import datetime
  
class Voter(models.Model):
    ''' Store/represent the data for a registered voter in Newtown.
        
        Data Attributes: first name, last name, street number, street name, 
                         apartment number, zip code, DOB, DOR, party affiliation, 
                         precinct number, voting participation fields '''
    
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    street_number = models.CharField(max_length=10, blank=True, null=True)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=20)
    precinct_number = models.IntegerField()

    # Voting participation fields
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    # Voter score
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct_number}"

def load_data():
    '''Load data records from a CSV file into Voter model instances'''

    Voter.objects.all().delete()

    filename = '/Users/MirutikkaS/Downloads/newton_voters.csv'
    
    with open(filename, 'r') as f:
        headers = f.readline().strip().split(',')
        
        for line in f:
            try:
                fields = line.strip().split(',')
                
                # Clean party_affiliation
                party_affiliation = fields[9].strip()  

                # Validate the voter_score is numeric
                try:
                    voter_score_str = fields[-1].strip() 
                    # Check if the voter_score is a valid number, otherwise default to 0
                    voter_score = int(voter_score_str) if voter_score_str.isdigit() else 0
                except ValueError:
                    print(f"Invalid voter_score on line: {line.strip()}")
                    continue  # Skip this row if voter_score is not an integer

                # Parse the dates manually handling MM/DD/YY and DD/MM/YY formats
                try:
                    date_of_birth = parse_date(fields[7])
                except ValueError:
                    try:
                        date_of_birth = parse_date(fields[7])
                    except ValueError:
                        print(f"Invalid date format for date_of_birth on line: {line.strip()}")
                        continue  # Skip if the date format is incorrect

                try:
                    date_of_registration = parse_date(fields[8])
                except ValueError:
                    try:
                        date_of_registration = parse_date(fields[8])
                    except ValueError:
                        print(f"Invalid date format for date_of_registration on line: {line.strip()}")
                        continue  # Skip if the date format is incorrect

                # Create a new instance of the Voter model using the fields
                voter = Voter(
                    last_name=fields[1],
                    first_name=fields[2],
                    street_number=fields[3],
                    street_name=fields[4],
                    apartment_number=fields[5] if fields[5] else None,  
                    zip_code=fields[6],
                    date_of_birth=date_of_birth,
                    date_of_registration=date_of_registration,
                    party_affiliation=party_affiliation,  
                    precinct_number=int(fields[10]), 
                    v20state=fields[11] == 'TRUE', 
                    v21town=fields[12] == 'TRUE',
                    v21primary=fields[13] == 'TRUE',
                    v22general=fields[14] == 'TRUE',
                    v23town=fields[15] == 'TRUE',
                    voter_score=voter_score 
                )
                
                voter.save()
                print(f'Created voter: {voter}')
            
            except Exception as e:
                print(f"Exception on line: {line.strip()} - {e}")