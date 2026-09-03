from django.db import models


class LinkedInProfile(models.Model) :
    full_name = models.CharField(max_length = 200, db_index = True)
    first_name = models.CharField(max_length = 100, blank = True)
    last_name = models.CharField(max_length = 100, blank = True)
    gender = models.CharField(max_length = 20, blank = True, null = True)
    email = models.EmailField(blank = True, null = True)
    work_email = models.EmailField(blank = True, null = True)
    phone_numbers = models.JSONField(default = list, blank = True)
    emails = models.JSONField(default = list, blank = True)
    location = models.CharField(max_length = 200, blank = True, null = True, db_index = True)
    location_locality = models.CharField(max_length = 100, blank = True, null = True)
    location_region = models.CharField(max_length = 100, blank = True, null = True)
    location_country = models.CharField(max_length = 100, blank = True, null = True)
    industry = models.CharField(max_length = 200, blank = True, null = True)
    job_title = models.CharField(max_length = 200, blank = True, null = True)
    job_company_name = models.CharField(max_length = 200, blank = True, null = True)
    linkedin_url = models.URLField(blank = True, null = True)
    linkedin_username = models.CharField(max_length = 100, blank = True, null = True)
    linkedin_connections = models.FloatField(default = 0)
    inferred_years_experience = models.FloatField(default = 0)
    inferred_salary = models.CharField(max_length = 100, blank = True, null = True)
    summary = models.TextField(blank = True, null = True)
    skills = models.JSONField(default = list, blank = True)
    experience = models.JSONField(default = list, blank = True)
    education = models.JSONField(default = list, blank = True)
    profiles = models.JSONField(default = list, blank = True)
    certifications = models.JSONField(default = list, blank = True)
    search_text = models.TextField(blank = True)

    class Meta :
        indexes = [
            models.Index(fields = ['full_name']),
            models.Index(fields = ['location']),
            models.Index(fields = ['job_title']),
        ]

    def save(self, *args, **kwargs) :

        search_parts = [
            self.full_name or '',
            self.first_name or '',
            self.last_name or '',
            self.location or '',
            self.job_title or '',
            self.job_company_name or '',
            self.industry or '',
        ]

        if self.skills and isinstance(self.skills, list) :
            search_parts.append(' '.join(self.skills))
        elif self.skills and isinstance(self.skills, str) :
            search_parts.append(self.skills)


        if self.summary :
            search_parts.append(self.summary)

        self.search_text = ' '.join(search_parts)

        super().save(*args, **kwargs)

    def __str__(self) :
        return self.full_name or f"Profile {self.id}"