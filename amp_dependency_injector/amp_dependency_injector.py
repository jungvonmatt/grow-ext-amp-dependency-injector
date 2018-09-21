# -*- coding: utf-8 -*-
import re

import lxml
from grow import extensions
from grow.documents import document
from grow.extensions import hooks

AVAILABLE_COMPONENTS = ['amp-carousel', 'amp-bind']

class AmpDependencyInjectorPostRenderHook(hooks.PostRenderHook):
    """Handle the post-render hook."""

    def trigger(self, previous_result, doc, raw_content, *_args, **_kwargs):
        content = previous_result if previous_result else raw_content
        # Quick check if the page is really a AMP page
        if not any(marker in content for marker in ['<html amp', '<html ⚡']):
            return content

        dependencies = self.find_dependencies(content)
        dependencies = self.verify_dependencies(content)
        content = self.inject_dependencies(dependencies, content)

        return content

    def find_dependencies(self, content):
        dependencies = []

        # Finds all <amp-*> tags that may introduce a dependency to a component
        ELEMENT_REGEX = r"<(amp-\S*?)(>|\s)"
        for element in re.findall(ELEMENT_REGEX, content):
            # The first capturing group will be the component name
            component_name = element[0]
            dependencies.append(component_name)

        # Checks if document depends on <amp-form>
        if '<form' in content:
            dependencies.append('amp-form')

        # Checks if document depends on <amp-bind>, also see:
        # https://www.ampproject.org/docs/reference/components/amp-bind#element-specific-attributes
        # TODO: Add bindable values of <input>
        AMP_BIND_MARKERS_REGEX = r"(<amp-state|<amp-bind-macro|\s\[(text|class|hidden|width|height|src|title|alt|srcset|open|selected|controls|loop|poster|preload|disabled|href|type|value)\]=)"
        if re.match(AMP_BIND_MARKERS_REGEX, content):
            dependencies.append('amp-bind')

        # Checks if document depends on <amp-mustache>
        if '<template type="amp-mustache"'
            dependencies.append('amp-mustache')


    def verify_dependencies(self, dependencies):
        return dependencies

    def inject_dependencies(self, dependencies, content):
        return content

class AmpDependencyInjectorExtension(extensions.BaseExtension):
    """AMP Dependency Injector Extension."""

    @property
    def available_hooks(self):
        """Returns the available hook classes."""
        return [AmpDependencyInjectorPostRenderHook]
