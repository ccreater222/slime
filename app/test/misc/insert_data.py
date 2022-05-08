from util.stage_model import *
import random
for i in range(100):
    p = PortDetectModel(random.randint(1,65535))
    p.save()