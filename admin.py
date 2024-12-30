from django.contrib import admin
from .models import Agent
from MultisiteControlPanel.models import Site
from django.urls import path
from django.shortcuts import render
from JobManager.admin import CustomAdminSite
from datetime import date

from django.http import HttpResponseRedirect
from django.contrib import messages
from JobManager.models import Job, Employer, JobPackageItem
from .git_operations import process_agent, create_pr  # Import your functions


class ExtendedAdminSite(CustomAdminSite):

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('webscrapsupervisor/monitor/', self.admin_view(self.monitor_view), name='monitor'),
        ]
        return custom_urls + urls

    def monitor_view(self, request):

        data_list = []

        primary_site_url = Site.get_primary_site().get_site_home_url()
        agents = Agent.objects.order_by('employer__registered_on')
        if agents.exists():
            for agent in agents:

                data = {}
                employer = agent.employer
                data['id'] = agent.id
                data['name'] = employer.name
                data['slug'] = employer.slug
                data['status'] = agent.status
                data['fetch_type'] = agent.fetch_type
                data['feed_url'] = agent.feed_url if agent.feed_url else "#"
                data['registered_on'] = employer.registered_on.strftime('%Y-%m-%d %H:%M:%S') if employer.registered_on else "-"
                data['primary_site_url'] = primary_site_url

                last_fetch_time = agent.last_fetch_time
                if last_fetch_time != None:
                    if last_fetch_time.date() == date.today():
                        data['last_fetch_time'] = last_fetch_time.strftime('Today %H:%M:%S')
                    else:
                        data['last_fetch_time'] = last_fetch_time.strftime('%Y-%m-%d %H:%M:%S')
                if employer.children.exists():
                    data['active_jobs_count'] = employer.getTotalActiveJobCountOfParentEmployer()
                    data['expired_jobs_count'] = employer.getTotalExpiredJobCountOfParentEmployer()
                else:
                    data['active_jobs_count'] = employer.getTotalActiveJobCount()
                    data['expired_jobs_count'] = employer.getTotalExpiredJobCount()

                last_reported_log = agent.last_reported_log if agent.last_reported_log else None
                if last_reported_log:
                    data['error'] = last_reported_log.get('error', {})
                    data['warnings'] = last_reported_log.get('warnings', [])

                data['credits'] = employer.recruiter.getTotalCredits()
                data['balance'] = employer.recruiter.getTotalBalanceCredits()

                if employer.recruiter.has_unlimited_package():
                    data['unlimited'] = "Unlimited"
                else:
                    data['unlimited'] = ""

                data['ats_name'] = agent.ats_name if agent.ats_name else ""
                data['email_for_ats'] = agent.email_for_ats if agent.email_for_ats else ""
                data['notes'] = agent.notes if agent.notes else ""

                data_list.append(data)

        return render(request, 'monitor_page.html', {'data_list': data_list})


class AgentAdmin(admin.ModelAdmin):

    list_display = ('employer', 'status', 'parent_agent')
    search_fields = ['employer__actual_name', 'employer__display_name', 'ats_name', 'parent_agent__employer__actual_name', 'parent_agent__employer__display_name']
    list_filter = ['status', 'employer']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/remove-agent/', self.admin_site.admin_view(self.remove_agent_confirmation), name='webscrapsupervisor_agent_remove'),
            path('<path:object_id>/perform-remove-agent/', self.admin_site.admin_view(self.remove_agent_and_deactivate), name='webscrapsupervisor_agent_perform_remove'),
        ]
        return custom_urls + urls

    def remove_agent_confirmation(self, request, object_id):
        """Show the confirmation page with sidebar intact"""
        agent = Agent.objects.get(id=object_id)
        employer = agent.employer
        jobs_to_update = Job.objects.filter(employer=employer, status=Job.ACTIVE)
        job_package_items = JobPackageItem.objects.filter(owner=employer.recruiter, status=JobPackageItem.ACTIVE)

        context = {
            'agent': agent,
            'employer': employer,
            'jobs_to_update': jobs_to_update,
            'job_package_items': job_package_items,
            'opts': self.model._meta,  # Required for the admin sidebar
            'app_label': self.model._meta.app_label,  # Ensure app_label is passed
        }
        return render(request, 'remove_agent_confirmation.html', context)

    def remove_agent_and_deactivate(self, request, object_id):
        """This view performs the actual removal and deactivation of the agent and related items"""
        try:
            agent = Agent.objects.get(id=object_id)
            employer = agent.employer
            jobs_to_update = Job.objects.filter(employer=employer, status=Job.ACTIVE)
            jobs_to_update.update(status=Job.INACTIVE)

            employer.status = Employer.INACTIVE
            employer.save()

            agent.status = Agent.DEACTIVATED
            agent.save()

            job_package_items = JobPackageItem.objects.filter(owner=employer.recruiter, status=JobPackageItem.ACTIVE)
            job_package_items.update(status=JobPackageItem.DEACTIVATED)

            success = process_agent(employer.name)
            if success:
                github_token = "wglfwelk"
                create_pr(f"remove-agent-{employer.name}", github_token)

                messages.success(
                    request,
                    f"Successfully deactivated agent, employer, {jobs_to_update.count()} jobs, "
                    f"and {job_package_items.count()} job package items."
                )
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

        return HttpResponseRedirect('/admin/WebScrapSupervisor/agent/')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_remove_agent'] = True  # Add this to ensure the custom flag is set

        # Do not hide the sidebar here
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


registered_models = admin.site._registry.items()


admin.site = ExtendedAdminSite()

for model, model_admin in registered_models:
    admin.site.register(model, model_admin.__class__)

admin.site.register(Agent, AgentAdmin)
