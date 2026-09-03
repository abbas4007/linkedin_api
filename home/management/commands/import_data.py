import csv
import json
import re
from django.core.management.base import BaseCommand
from home.models import LinkedInProfile
from django.db import transaction


class Command(BaseCommand) :
    help = 'Import LinkedIn data'

    def add_arguments(self, parser) :
        parser.add_argument('file_path', type = str, help = 'Path to CSV/TXT file')

    def handle(self, *args, **options) :
        file_path = options['file_path']
        self.import_csv(file_path)

    @transaction.atomic
    def import_csv(self, file_path) :
        with open(file_path, 'r', encoding = 'utf-8') as f :
            reader = csv.DictReader(f)
            count = 0

            # casting to float
            def safe_float(value, default=0.0) :
                if not value or not str(value).strip() :
                    return default
                cleaned = re.sub(r'[^\d.]', '', str(value))
                try :
                    return float(cleaned) if cleaned else default
                except ValueError :
                    return default

            for row in reader :
                # for skils
                skills = []
                if row.get('skills') :
                    try :
                        skills = json.loads(row['skills'])
                    except :
                        skills = [s.strip() for s in row['skills'].replace("'", "").replace('"', '').split(',') if
                                  s.strip()]

                # for experience
                experience = []
                if row.get('experience') :
                    try :
                        experience = json.loads(row['experience'])
                    except :
                        pass

                # for education
                education = []
                if row.get('education') :
                    try :
                        education = json.loads(row['education'])
                    except :
                        pass

                # for emails
                emails = []
                if row.get('emails') :
                    try :
                        emails_data = json.loads(row['emails'])
                        if isinstance(emails_data, list) :
                            emails = [e.get('address', '') for e in emails_data if e.get('address')]
                    except :
                        emails = [row['emails']]

                #  for phone_numbers
                phone_numbers = []
                if row.get('phone_numbers') :
                    try :
                        phones = json.loads(row['phone_numbers'])
                        if isinstance(phones, list) :
                            phone_numbers = phones
                    except :
                        phone_numbers = [row['phone_numbers']]

                # create profiles.
                profile = LinkedInProfile.objects.create(
                    full_name = row.get('full_name', ''),
                    first_name = row.get('first_name', ''),
                    last_name = row.get('last_name', ''),
                    gender = row.get('gender', ''),
                    email = emails[0] if emails else '',
                    work_email = row.get('work_email', ''),
                    location = row.get('location_name', row.get('location_names', '')),
                    location_locality = row.get('location_locality', ''),
                    location_region = row.get('location_region', ''),
                    location_country = row.get('location_country', ''),
                    industry = row.get('industry', ''),
                    job_title = row.get('job_title', ''),
                    job_company_name = row.get('job_company_name', ''),
                    summary = row.get('summary', ''),
                    skills = skills,
                    experience = experience,
                    education = education,
                    phone_numbers = phone_numbers,
                    emails = emails,
                    linkedin_url = row.get('linkedin_url', ''),
                    linkedin_username = row.get('linkedin_username', ''),
                    linkedin_connections = safe_float(row.get('linkedin_connections', 0)),
                    inferred_years_experience = safe_float(row.get('inferred_years_experience', 0)),
                    inferred_salary = row.get('inferred_salary', ''),
                    profiles = [],
                    certifications = [],
                )
                count += 1


        self.stdout.write(self.style.SUCCESS(f' Successfully imported {count} profiles!'))
