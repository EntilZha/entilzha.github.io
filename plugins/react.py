import subprocess
import pelican
from pelican import signals
from rich.console import Console


console = Console()


def compile_jsx(path: str, prod=True) -> str:
    if prod:
        command = f'npx babel --presets react-app/prod {path}'
        console.log("Running: ", command)
        proc = subprocess.run(
            f'npx babel --presets react-app/prod {path}',
            shell=True, stdout=subprocess.PIPE, check=True, stderr=subprocess.PIPE
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