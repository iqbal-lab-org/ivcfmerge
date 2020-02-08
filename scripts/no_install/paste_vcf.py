from pathlib import Path
import sys

sys.path.append(str(Path(__file__).absolute().parent.parent.parent))

from multifile.paster.vcf.__main__ import main

main()