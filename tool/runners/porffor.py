import errno
import subprocess
import tempfile

from tool.runners.wrapper import SubmissionWrapper
from tool.runners.exceptions import CompilationError, RuntimeError

class SubmissionPorffor(SubmissionWrapper):
    def __init__(self, file):
        SubmissionWrapper.__init__(self)
        tmp = tempfile.NamedTemporaryFile(prefix="aoc")
        tmp.close()
        print(f"Compiling {file} to {tmp.name}")
        compile_output = subprocess.check_output(
            [
                "npx",
                "--yes",
                "porffor",
                "native",
                file,
                tmp.name,
            ]
        ).decode()
        if compile_output:
            raise CompilationError(compile_output)
        self.executable = tmp.name

    def exec(self, input):
        try:
            return subprocess.check_output([self.executable, input]).decode()
        except OSError as e:
            if e.errno == errno.ENOENT:
                # executable not found
                return CompilationError(e)
            else:
                # subprocess exited with another error
                return RuntimeError(e)

    # def __call__(self):
    #     return SubmissionPorffor(self.file)
