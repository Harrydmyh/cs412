# voter_analytics/models.py
# model for the voter analytics application
# Author: Yihang Duanmu (harrydm@bu.edu), 10/28/2025

from django.db import models


# Create your models here.
class Voter(models.Model):
    """
    Store/represent the data from one Newton voter.
    Voter ID Number, Last Name, First Name, Residential Address,
    Date of Birth, Date of Registration, Party Affiliation, Precinct Number,
    v20state, v21town, v21primary, v22general, v23town, voter_score
    """

    # Personal information fields
    voter_id = models.CharField(max_length=12)
    last_name = models.TextField()
    first_name = models.TextField()
    residential_address = models.TextField()
    date_of_birth = models.DateField()

    # Voting related information fields
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=1)
    precinct_number = models.CharField(max_length=2)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        """Return a string representation of this model instance."""
        return f"{self.first_name} {self.last_name} from ({self.residential_address}"


def load_data():
    """Funtion to load data records from csv file into Django database"""

    Voter.objects.all().delete()

    filename = "/Users/apple/django/newton_voters.csv"
    f = open(filename, "r")  # open the file for reading

    # discard headers
    f.readline()

    # read several rows
    for line in f:
        fields = line.strip().split(",")

        # create a new instance of Result object with this record from CSV
        try:
            voter = Voter(
                voter_id=fields[0],
                last_name=fields[1],
                first_name=fields[2],
                residential_address=fields[3] + " " + fields[4],
                date_of_birth=fields[7],
                date_of_registration=fields[8],
                party_affiliation=fields[9],
                precinct_number=fields[10],
                v20state=fields[11].capitalize(),
                v21town=fields[12].capitalize(),
                v21primary=fields[13].capitalize(),
                v22general=fields[14].capitalize(),
                v23town=fields[15].capitalize(),
                voter_score=fields[16],
            )

            voter.save()

        except Exception as e:
            print("Something went wrong:")
            print(f"line={line}")

    print(f"Done. Created {len(Voter.objects.all())} Voters data")
