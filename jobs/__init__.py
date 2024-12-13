from load_locations import LoadLocationJob
from nautobot.apps.jobs import register_jobs

register_jobs(LoadLocationJob)