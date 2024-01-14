"""
Doctor-Patient Database API for MySQL
"""

from dbutils import DBUtils
from docpat_objects import Doctor, Patient

class DoctorPatientAPI:

    def __init__(self, user, password, database, host="localhost"):
        self.dbu = DBUtils(user, password, database, host)

    def register_patient(self, pat):
        """
        This method takes a Patient object as an argument and inserts a new record into the 
        patient table in the database. It constructs an SQL INSERT statement and uses the 
        insert_one method of the DBUtils instance to execute it.
        
        """
        sql = "INSERT INTO patient (lastname, firstname, sex, dob) VALUES (%s, %s, %s, %s) "
        val = (pat.last, pat.first, pat.sex, pat.dob)
        self.dbu.insert_one(sql, val)

    def accepting_patients(self, specialty):
        """
        This method takes a specialty as an argument and returns a list of Doctor objects who are accepting 
        new patients and have the specified specialty. It constructs an SQL SELECT statement and 
        uses the execute method of the DBUtils instance to execute it. The returned data frame 
        is then used to create a list of Doctor objects.
        """
        sql = """
                select doctor_id, lastname, firstname, new_patients, specialty, h.name hospital
                from doctor d join specialty using (specialty_id) 
                join hospital h using (hospital_id)
                where new_patients = 1
                and specialty like '""" + specialty + "'"
        df = self.dbu.execute(sql)
        docs = [Doctor(*df.iloc[i][1:]) for i in range(len(df))]
        return docs


