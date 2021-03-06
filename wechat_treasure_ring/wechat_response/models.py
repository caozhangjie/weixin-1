from django.db import models


class RingUser(models.Model):
    user_id = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30)
    headimgurl = models.CharField(max_length=300)
    sex = models.CharField(max_length=30)
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    target = models.IntegerField()
    last_record = models.IntegerField()
    steps_totalused = models.IntegerField()


class Record(models.Model):
    user_name = models.CharField(max_length=30)
    startTime = models.IntegerField()
    endTime = models.IntegerField()
    type = models.IntegerField()
    distance = models.IntegerField()
    calories = models.IntegerField()
    steps = models.IntegerField()
    subType = models.IntegerField()
    actTime = models.IntegerField()
    nonActTime = models.IntegerField()
    dsNum = models.IntegerField()
    lsNum = models.IntegerField()
    wakeNum = models.IntegerField()
    wakeTimes = models.IntegerField()
    score = models.FloatField()

class RecordByDay(models.Model):
    user_name = models.CharField(max_length=30)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    dsNum = models.IntegerField()
    allNum = models.IntegerField()
    calories = models.IntegerField()
    steps = models.IntegerField()
    distance = models.IntegerField()
    score = models.FloatField()


class BirdUser(models.Model):
    openid = models.CharField(max_length=30)
    steps_used = models.IntegerField()
    score_today = models.IntegerField()
    score_total = models.IntegerField()


class RecordAttention(models.Model):
    source_user_id = models.CharField(max_length=30)
    target_user_id = models.CharField(max_length=30)
    attentionTime = models.IntegerField()


