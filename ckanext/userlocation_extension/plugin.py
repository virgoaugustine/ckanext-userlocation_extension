import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from flask import Blueprint, render_template
import json
from urllib.request import urlopen

def user_location():
    '''Return user location and IP in the format:
     "You are accessing the ckan server from {ISP location} and your IP address is: {IP}"
     '''

    with urlopen('https://ipinfo.io/json') as url:
        isp_info = json.loads(url.read())
    
        return f"You are accessing the ckan server from {isp_info['city']}, {isp_info['region']} and your ISP address is: {isp_info['ip']}"


class UserlocationExtensionPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'userlocation_extension')

    def get_blueprint(self):
        blueprint = Blueprint(self.name, self.__module__)
        blueprint.template_folder = 'templates'
        blueprint.add_url_rule('/user_location','/user_location', user_location)
        return blueprint