from django import template

register = template.Library()

nav_pills = {
    "Patients": {
        "url_main": "patients:patient-list",
        "bootstrap_icon": "bi-person",
        "apps": {
            "patients": {
                "name": "Patients",
                "link": "patients:patient-list"
            },
        }
    },
    "Lab": {
        "url_main": "lab:lab-list",
        "bootstrap_icon": "bi-flask",
        "apps": {
            "lab": {
                "name": "Lab",
                "link": "lab:lab-list"
            },
            "panels": {
                "name": "Panels",
                "link": "panels:panel-list"
            },
            "tests": {
                "name": "Tests",
                "link": "tests:test-list"
            },
        }
    },
    "MC Reports": {
        "url_main": "mc_reports:mcr-list",
        "bootstrap_icon": "bi-file-text",
        "apps": {
            "mc_reports": {
                "name": "MC Reports",
                "link": "mc_reports:mcr-list"
            },
        }
    },
    "X-Rays": {
        "url_main": "x_rays:x-rays-list",
        "bootstrap_icon": "bi-radioactive",
        "apps": {
            "x_rays": {
                "name": "X-Rays",
                "link": "x_rays:x-rays-list"
            }
        }
    }
}

@register.inclusion_tag("core/partials/nav_pills.html")
def get_nav_pills(app=None):
    return {"app": app, "nav_pills": nav_pills}

@register.inclusion_tag("core/partials/nav_tabs.html")
def get_nav_tabs(app=None):
    # A list of dictionaries, where each dictionary is a group of
    # related apps, with apps being the keys and their main page urls
    # being the values.
    tab_groups = [details["apps"] for pill, details in nav_pills.items()]
    
    return {"app": app, "tab_groups": tab_groups}