import subprocess
import pelican
from pelican import signals


def compile_jsx(path: str, prod=True) -> str:
    if prod:
        proc = subprocess.run(
            f'npx babel --presets react-app/prod {path}',
            shell=True, stdout=subprocess.PIPE, check=True
        )
        return '<script type="text/javascript">' + proc.stdout.decode() + '</script>'
    else:
        with open(path) as f:
            content = f.read()
        return """
            <script src="/theme/js/react.development.js" crossorigin></script>
            <script src="/theme/js/react-dom.development.js" crossorigin></script>
            <script src="/theme/js/babel.min.js"></script>
            """ + '<script type="text/babel">' + content + '</script>'


def add_filter(pelican):
    pelican.env.filters.update({'compile_jsx': compile_jsx})


def register():
    """Plugin registration."""
    signals.generator_init.connect(add_filter)