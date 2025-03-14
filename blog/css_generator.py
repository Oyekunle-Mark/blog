from pathlib import Path
import subprocess
from .config import CssGenerationError


class CssGenerator:
    def __init__(self, css_dir: str):
        self.css_dir = Path(css_dir)

    def generate_pygments_css(self) -> Path:
        """
        Generate pygments.css file using pygmentize command.
        Returns the path to the generated file.
        """

        try:
            self.css_dir.mkdir(parents=True, exist_ok=True)
            output_path = self.css_dir / 'pygments.css'

            # Run pygmentize to generate CSS
            result = subprocess.run(
                ['pygmentize', '-S', 'default', '-f', 'html', '-a', '.codehilite'],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                raise CssGenerationError(f"Pygments CSS generation failed: {result.stderr}")

            # Write the CSS to file
            output_path.write_text(result.stdout)
            print(f"Generated Pygments CSS: {output_path}")

            return output_path
        except subprocess.CalledProcessError as e:
            raise CssGenerationError(f"Failed to run pygmentize: {str(e)}")
        except Exception as e:
            raise CssGenerationError(f"Failed to generate Pygments CSS: {str(e)}")
