# -*- coding: utf-8 -*-
import lxml
from grow import extensions
from grow.documents import document
from grow.extensions import hooks


class AmpDependencyInjectorPostRenderHook(hooks.PostRenderHook):
    """Handle the post-render hook."""

    def trigger(self, previous_result, doc, raw_content, *_args, **_kwargs):
        """Execute post-render modification."""
        content = previous_result if previous_result else raw_content

        # Do something to modify the contents.
        content = content + "<!-- test -->"

        return content

class AmpDependencyInjectorExtension(extensions.BaseExtension):
    """Example Extension."""

    @property
    def available_hooks(self):
        """Returns the available hook classes."""
        return [AmpDependencyInjectorPostRenderHook]
