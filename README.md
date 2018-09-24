# grow-ext-amp-dependency-injector
Extension for the static-site generator Grow that auto injects &lt;script&gt; tags for used AMP components.

## Concept
This is a Grow PostRenderHook. After rendering the full page it searches the generated markup for hints of used AMP components. This is done by simple string lookups and though **may break for markup inside of `<code>` blocks**. This is work in progress.

After matching the found dependencies against a list of valid dependencies they get injected by creating a DOM of the rendered document and injecting `<script>` tags matching the dependencies into the document.

## Usage
### Initial setup
1. Create an `extensions.txt` file within your pod.
1. Add to the file: `git+git://github.com/jungvonmatt/grow-ext-amp-dependency-injector`
1. Run `grow install`.
1. Add the following section to `podspec.yaml`:

```
ext:
- extensions.amp_dependency_injector.AmpDependencyInjectorExtension
```

### Configuration
By default all pages that have a HTML tag of either `<html amp` or `<html ⚡` are considered AMP pages and get their dependencies injected. To opt out of this behaviour for a specific page set the following inside the document's frontmatter:

```yaml
$$injectAmpDependencies: False
```
