from util.stage_model import *
import random
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

def test_save():
    base_model = BaseModel()
    i = random.randint(1,10000)
    base_model.test_id = i
    base_model.test_list = [i]
    base_model.test_dict = {'test': i}
    base_model.save()
    base_model.test_list = [i+1]
    base_model.test_dict = {'test2': i}
    base_model.save()
    record = db_resource.find_one({'test_id':i})
    assert 'test2' in record['test_dict'].keys() and 'test' in record['test_dict']
    assert i+1
    db_resource.delete_many({'test_id': {'$exists': True}})
    
