from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from enum import IntEnum

# Exercise models setup.
    
class BaseModel(models.Model):
    name = models.CharField(max_length = 200, default="New directory")
    desc = models.CharField(max_length = 200, blank=True)
    creation_date = models.DateTimeField("creation date", default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    alive = models.BooleanField(default=True)
    delete_date = models.DateTimeField("delete date", blank=True, null=True)
    change_date = models.DateTimeField("change date", blank=True, null=True)
    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class FileSystemAbstractModel(BaseModel):
    parent = models.ForeignKey('Directory', on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        abstract = True

class Directory(FileSystemAbstractModel):
    is_a_file = False
    class Meta:
        abstract = False

class File(FileSystemAbstractModel):
    text = models.CharField(max_length=10000, default="siema")
    is_a_file = True
    class Meta:
        abstract = False

class SectionTypes(IntEnum):
  PROCEDURE = 1
  COMMENT = 2
  DIRECTIVE = 3
  DECLARATION = 4
  ASSEMBLY = 5
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]
  
class SectionType(BaseModel):
    type = models.IntegerField(choices=SectionTypes.choices())

class SectionStatuses(IntEnum):
  COMPILING = 1
  NOT_COMPILING = 2
  WARNINGS = 3
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]
  
class StatusData(BaseModel):
    warning_line = models.IntegerField()

class SectionStatus(BaseModel):
    data = models.ForeignKey(StatusData, on_delete=models.CASCADE)
    type = models.IntegerField(choices=SectionStatuses.choices())

class FileSection(BaseModel):
    name = models.CharField(max_length = 200)
    desc = models.CharField(max_length = 200)
    creation_date = models.DateTimeField("creation date")
    start = models.IntegerField();
    end = models.IntegerField();
    type = models.ForeignKey(SectionType, on_delete=models.CASCADE)
    status = models.ForeignKey(SectionStatus, on_delete=models.CASCADE)
    parent = models.ForeignKey(File, on_delete=models.CASCADE)


# Compilation options setup
class Standard(models.Model):
    name = models.CharField(max_length = 10)
    def __str__(self):
        return self.name

class Optimization(models.Model):
    name = models.CharField(max_length = 100)
    active = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Processor(models.Model):
    name = models.CharField(max_length = 20)
    
    def __str__(self):
        return self.name
    
class DependantOption(models.Model):
    name = models.CharField(max_length = 50)
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)
    active = models.BooleanField()
    def __str__(self):
        return self.name

class CompilationSettings(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE, blank=True, null=True)