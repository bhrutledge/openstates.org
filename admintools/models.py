from admintools import issues
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from opencivicdata.core.models import Jurisdiction


class DataQualityIssue(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=300)
    content_object = GenericForeignKey('content_type', 'object_id')
    jurisdiction = models.ForeignKey(Jurisdiction, related_name="dataquality_issues")
    alert = models.CharField(max_length=50)
    issue = models.CharField(max_length=150, choices=issues.IssueType.choices())
    reporter = models.CharField(max_length=300, blank=True)

    class Meta:
        db_table = 'opencivicdata_dataqualityissue'
        index_together = [
            ['alert', 'issue']
        ]

    def __str__(self):
        return '{} issue type - {}'.format(self.issue,
                                           self.alert)


class PeopleReport(models.Model):
    jurisdiction = models.ForeignKey(Jurisdiction, related_name='people_report')
    updated_at = models.DateTimeField(auto_now=True)
    missing_phone_count = models.PositiveIntegerField(default=0)
    missing_email_count = models.PositiveIntegerField(default=0)
    missing_address_count = models.PositiveIntegerField(default=0)
    missing_photo_count = models.PositiveIntegerField(default=0)

    def _get_total_warnings(self):
        return (self.missing_email_count + self.missing_phone_count +
                self.missing_address_count + self.missing_photo_count)

    warnings_count = property(_get_total_warnings)

    class Meta:
        db_table = 'admintools_people_report'


class OrganizationReport(models.Model):
    jurisdiction = models.ForeignKey(Jurisdiction, related_name='organization_report')
    updated_at = models.DateTimeField(auto_now=True)
    unmatched_person_count = models.PositiveIntegerField(default=0)
    no_memberships_count = models.PositiveIntegerField(default=0)

    def _get_total_warnings(self):
        return self.unmatched_person_count

    warnings_count = property(_get_total_warnings)

    class Meta:
        db_table = 'admintools_org_report'


class BillReport(models.Model):
    jurisdiction = models.ForeignKey(Jurisdiction, related_name='bill_report')
    updated_at = models.DateTimeField(auto_now=True)
    no_actions_count = models.PositiveIntegerField(default=0)
    no_sponsors_count = models.PositiveIntegerField(default=0)
    no_versions_count = models.PositiveIntegerField(default=0)
    unmatched_person_sponsor_count = models.PositiveIntegerField(default=0)
    unmatched_org_sponsor_count = models.PositiveIntegerField(default=0)

    def _get_total_warnings(self):
        return (self.no_sponsors_count + self.no_versions_count +
                self.unmatched_person_sponsor_count +
                self.unmatched_org_sponsor_count)

    warnings_count = property(_get_total_warnings)

    class Meta:
        db_table = 'admintools_bill_report'


class VoteEventReport(models.Model):
    jurisdiction = models.ForeignKey(Jurisdiction, related_name='voteevent_report')
    updated_at = models.DateTimeField(auto_now=True)
    missing_bill_count = models.PositiveIntegerField(default=0)
    missing_voters_count = models.PositiveIntegerField(default=0)
    missing_counts_count = models.PositiveIntegerField(default=0)
    bad_counts_count = models.PositiveIntegerField(default=0)
    unmatched_voter_count = models.PositiveIntegerField(default=0)

    def _get_total_warnings(self):
        return (self.missing_voters_count + self.bad_counts_count +
                self.unmatched_voter_count)

    warnings_count = property(_get_total_warnings)

    class Meta:
        db_table = 'admintools_voteevent_report'
