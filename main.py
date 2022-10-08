import subprocess
import sys
import zipfile
import io
from pathlib import Path

import requests

pb_id = "".join(letter for letter in "".join(
    sys.argv[1:]).lower() if letter.isalnum())
samples_url = f"{sys.argv[1]}/file/statement/samples.zip"
r = requests.get(samples_url)
r.raise_for_status()

with zipfile.ZipFile(io.BytesIO(r.content)) as z:
    for file in z.filelist:
        file_path = Path(file.filename)
        if file_path.suffix == ".in":
            test_input = z.read(file).decode("utf-8")
            test_answer = z.read(f"{file_path.stem}.ans").decode("utf-8")
            p = subprocess.run([sys.executable, sys.argv[2]],
                               input=test_input, encoding="utf-8", capture_output=True)
            if p.returncode != 0:
                print("Error:", p.stderr)
            print("Sample input:\n", test_input, sep="")
            if p.stdout != test_answer:
                print("Wrong answer!")
                print("Expected:,", len(test_answer),"\n", test_answer, sep="")
                print("Got:", len(p.stdout),"\n", p.stdout, sep="")
            else:
                print("Good answer!")
                print("Answer:\n", p.stdout, sep="")
