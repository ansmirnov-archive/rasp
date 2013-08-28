from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Week(models.Model):

    num = models.IntegerField()

    def __unicode__(self):
        return str(self.num)


class Group (models.Model):
    name = models.CharField(max_length=100)
    weeks = models.ManyToManyField(Week)

    def __unicode__(self):
        return self.name


class Day (models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class PairNumber (models.Model):
    num = models.IntegerField()

    def __unicode__(self):
        return str(self.num)


class SubGroup (models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group)

    def __unicode__(self):
        return self.name


class PairType (models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Subject (models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Aud (models.Model):
    name = models.CharField(max_length=100)


class Caf (models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Prep (models.Model):
    name = models.CharField(max_length=100)
    dol = models.CharField(max_length=100)
    caf = models.ForeignKey(Caf)

    def __unicode__(self):
        return self.name


class Pair (models.Model):
    group = models.ForeignKey(Group)
    subgroup = models.ForeignKey(SubGroup)
    day = models.ForeignKey(Day)
    pair_number = models.ManyToManyField(PairNumber)
    week = models.ManyToManyField(Week)
    pair_type = models.ForeignKey(PairType)
    subject = models.ForeignKey(Subject)
    aud = models.ForeignKey(Aud)
    prep = models.ForeignKey(Prep, blank=True, null=True)

    def pair_numbers(self):
        return ','.join([str(x.num) for x in self.pair_number.all()])

    def __unicode__(self):
        return self.subject.name
