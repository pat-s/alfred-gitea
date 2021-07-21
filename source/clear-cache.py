# encoding: utf-8
from workflow import Workflow

# log = None

def main(wf):
    wf.clear_cache()

if __name__ == u"__main__":
    wf = Workflow()
    log = wf.logger
    wf.run(main)
