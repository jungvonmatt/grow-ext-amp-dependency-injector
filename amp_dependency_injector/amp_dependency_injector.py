# -*- coding: utf-8 -*-
import re
from io import BytesIO

from grow import extensions
from grow.documents import document
from grow.extensions import hooks

try:
    from lxml import etree
    print("NOTICE: AMP dependency injector running with lxml.etree")
except ImportError:
    try:
        import xml.etree.cElementTree as etree
        print("NOTICE: AMP dependency injector running with cElementTree")
    except ImportError:
        print("WARNING: No good ElementTree implementation available")

# See: https://www.ampproject.org/docs/reference/components
# TODO: Add remaining Media dependencies
VALID_DEPENDENCIES = {
    'amp-ad': True,
    'amp-ad-exit': True,
    'amp-analytics': True,
    'amp-auto-ads': True,
    'amp-call-tracking': True,
    'amp-experiment': True,
    'amp-pixel': True,
    'amp-sticky-ad': True,
    'amp-access-laterpay': True,
    'amp-access': True,
    'amp-bind': True,
    'amp-byside-content': True,
    'amp-consent': True,
    'amp-date-picker': True,
    'amp-form': True,
    'amp-geo': True,
    'amp-gist': True,
    'amp-google-document-embed': True,
    'amp-install-serviceworker': True,
    'amp-list': True,
    'amp-live-list': True,
    'amp-mustache': True,
    'amp-next-page': True,
    'amp-selector': True,
    'amp-user-notification': True,
    'amp-web-push': True,
    'amp-accordion': True,
    'amp-app-banner': True,
    'amp-carousel': True,
    'amp-fx-flying-carpet': True,
    'amp-fx-collection': True,
    'amp-iframe': True,
    'amp-image-lightbox': True,
    # 'amp-layout': True,
    'amp-lightbox': True,
    'amp-lightbox-gallery': True,
    'amp-orientation-observer': True,
    'amp-position-observer': True,
    'amp-sidebar': True,
}


class AmpDependencyInjectorPostRenderHook(hooks.PostRenderHook):
    """Handle the post-render hook."""

    def trigger(self, previous_result, doc, raw_content, *_args, **_kwargs):
        content = previous_result if previous_result else raw_content
        # TODO: Check if the page opted-out of injection

        # Quick check if the page is really a AMP page
        if not any(marker in content for marker in ['<html amp', '<html ⚡']):
            return content

        dependencies = self.find_dependencies(content)
        dependencies = self.verify_dependencies(dependencies)
        content = self.inject_dependencies(dependencies, content)

        return content

    def find_dependencies(self, content):
        """Checks the generated output for possible AMP dependencies."""
        # TODO: Extract code snippets before searching for deps
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
        # TODO: Add remainig bindable values
        AMP_BIND_MARKERS_REGEX = r"(<amp-state|<amp-bind-macro|\s\[(text|class|hidden|width|height|src|title|alt|srcset|open|selected|controls|loop|poster|preload|disabled|href|type|value)\]=)"
        if re.match(AMP_BIND_MARKERS_REGEX, content):
            dependencies.append('amp-bind')

        # Checks if document depends on <amp-mustache>
        if '<template type="amp-mustache"' in content:
            dependencies.append('amp-mustache')

        # Checks if document uses <amp-fx-collection>
        if 'amp-fx="' in content:
            dependencies.append('amp-fx-collection')

        return dependencies

    def verify_dependencies(self, dependencies):
        """Verifies that the found dependencies are valid components."""
        dependencies = list(
            filter(lambda dependency: dependency in VALID_DEPENDENCIES,
                   dependencies))
        return dependencies

    def inject_dependencies(self, dependencies, content):
        # TODO: Parse document via etree.iterparse
        content = etree.HTML(content)
        head = content.find('head')
        for dependency in dependencies:
            # TODO: Handle different versions by configuration
            attributes = {
                'async': '',
                'src': 'https://cdn.ampproject.org/v0/{}-0.1.js'.format(dependency),
            }

            if dependency is not 'amp-mustache':
                attributes['custom-element'] = dependency
            else:
                attributes['custom-template'] = dependency

            script = head.makeelement('script', attributes)
            head.append(script)

        return etree.tostring(content, pretty_print=False, method='html')


class AmpDependencyInjectorExtension(extensions.BaseExtension):
    """AMP Dependency Injector Extension."""

    @property
    def available_hooks(self):
        """Returns the available hook classes."""
        return [AmpDependencyInjectorPostRenderHook]
