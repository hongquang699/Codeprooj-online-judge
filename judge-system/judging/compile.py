"""
Compiler Manager for Judge System.
Compiles submissions for compiled languages and verifies syntax for interpreted ones.
"""

import os
import subprocess
from dataclasses import dataclass
from typing import Optional, List
import yaml

@dataclass
class CompileResult:
    success: bool
    binary_path: Optional[str]
    compiler_output: str
    error_message: str = ""

class Compiler:
    def __init__(self, languages_config_path: Optional[str] = None):
        if not languages_config_path:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            languages_config_path = os.path.join(current_dir, "..", "config", "languages.yml")
        
        self.languages = {}
        if os.path.exists(languages_config_path):
            with open(languages_config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                self.languages = data.get("languages", {})

    def compile(
        self,
        language: str,
        source_code: str,
        build_dir: str,
        time_limit_sec: float = 15.0
    ) -> CompileResult:
        """
        Compiles the source code inside build_dir.
        """
        os.makedirs(build_dir, exist_ok=True)
        lang_info = self.languages.get(language)
        if not lang_info:
            return CompileResult(
                success=False,
                binary_path=None,
                compiler_output="",
                error_message=f"Unsupported language: {language}"
            )

        source_file_name = lang_info.get("source_file", "solution.txt")
        source_path = os.path.join(build_dir, source_file_name)

        # Write source code
        with open(source_path, "w", encoding="utf-8") as f:
            f.write(source_code)

        # For non-compiled languages (Python, JS)
        is_compiled = lang_info.get("is_compiled", False)
        if not is_compiled:
            # Syntax validation if compile_cmd exists
            compile_cmd_template = lang_info.get("compile_cmd")
            if compile_cmd_template:
                cmd = [arg.replace("{source}", source_path) for arg in compile_cmd_template]
                try:
                    proc = subprocess.run(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        timeout=time_limit_sec
                    )
                    if proc.returncode != 0:
                        return CompileResult(
                            success=False,
                            binary_path=None,
                            compiler_output=proc.stderr or proc.stdout,
                            error_message="Syntax check failed"
                        )
                except Exception as e:
                    return CompileResult(
                        success=False,
                        binary_path=None,
                        compiler_output=str(e),
                        error_message="Compiler process error"
                    )

            return CompileResult(
                success=True,
                binary_path=source_path,
                compiler_output="Syntax check passed"
            )

        # For compiled languages
        binary_file_name = lang_info.get("binary_file", "solution.exe")
        binary_path = os.path.join(build_dir, binary_file_name)

        compile_cmd_template = lang_info.get("compile_cmd", [])
        if not compile_cmd_template:
            return CompileResult(
                success=False,
                binary_path=None,
                compiler_output="",
                error_message="No compile command configured for this language"
            )

        cmd = [
            arg.replace("{source}", source_path).replace("{binary}", binary_path)
            for arg in compile_cmd_template
        ]

        try:
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=time_limit_sec,
                cwd=build_dir
            )

            output = (proc.stdout + "\n" + proc.stderr).strip()

            if proc.returncode != 0 or not os.path.exists(binary_path):
                return CompileResult(
                    success=False,
                    binary_path=None,
                    compiler_output=output,
                    error_message=f"Compilation failed with exit code {proc.returncode}"
                )

            return CompileResult(
                success=True,
                binary_path=os.path.abspath(binary_path),
                compiler_output=output
            )

        except subprocess.TimeoutExpired:
            return CompileResult(
                success=False,
                binary_path=None,
                compiler_output="Compilation timed out",
                error_message="Compilation Time Limit Exceeded"
            )
        except Exception as e:
            return CompileResult(
                success=False,
                binary_path=None,
                compiler_output=str(e),
                error_message=f"Compiler exception: {str(e)}"
            )
