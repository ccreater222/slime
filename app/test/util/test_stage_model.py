from util.stage_model import *
def test_base_model():
    base_model = BaseModel()
    base_model.tag = ['test']
    base_model.taskid = '1233123123123'
    model = InfoCollectModel.generate(base_model, 'thisisname')
    model.abc = 123
    assert 'abc' in model.toDict().keys()
    base_model.abc = 123
    model2 = InfoCollectModel.generate(base_model, 'thisisname')
    assert 'abc' in model2.toDict().keys()
