from django.db import models

# Create your models here.
class JobFunctions(models.Model):
    # function=models.ForeignKey(Jobs, related_name='job_functions', on_delete=models.CASCADE)
    jobFunction=models.TextField(max_length=200)

class Industries(models.Model):
    # loca=models.ForeignKey(Jobs, related_name='job_locations', on_delete=models.CASCADE)
    industry=models.TextField(max_length=200)
    
class Location(models.Model):
    # loca=models.ForeignKey(Jobs, related_name='job_locations', on_delete=models.CASCADE)
    location=models.TextField(max_length=200)
    
class Type(models.Model):
    # tim=models.ForeignKey(Jobs, related_name='job_time', on_delete=models.CASCADE)
    time=models.CharField(max_length=200)
class Jobs(models.Model):
    title = models.TextField(max_length=5000)
    link = models.URLField(max_length=5000)
    location = models.ForeignKey(Location, related_name='job_locations', on_delete=models.CASCADE)
    job_type = models.ForeignKey(Type, related_name='job_types', on_delete=models.CASCADE) 
    job_function = models.ForeignKey(JobFunctions, related_name='job_functions', on_delete=models.CASCADE)
    industries = models.ForeignKey(Industries, related_name='job_industries', on_delete=models.CASCADE)
    
class JobDetail(models.Model):
    job= models.ForeignKey(Jobs,related_name='job_details', on_delete=models.CASCADE)
    details=models.TextField(max_length=20000)
    bold=models.BooleanField(default=False)
    

    