import hls4ml
import json

def createProjectConfig():
    cfg = hls4ml.converters.create_config()
    cfg['Backend'] = 'Vivado'               # alt: VivadoAccelerator
    cfg['IOType'] = 'io_parallel'
    cfg['XilinxPart'] = 'xc7a100tcsg324-1'  # Nexys 4
    cfg['Part'] = cfg['XilinxPart']
    cfg['OutputDir'] = 'sinetest'
    cfg['ProjectName'] = 'sinetest'
    cfg['ClockPeriod'] = 10                 # 10 ns => 100MHz
    
    with open('project_cfg.json','w') as outfile:
        json.dump(cfg, outfile, indent=4, sort_keys=True)  
    
def createLayerConfig(model):
    # create config by layer name
    layer_cfg = hls4ml.utils.config_from_keras_model(model, granularity='name')
    with open(model.name+'_layer_cfg.json','w') as outfile:
        json.dump(layer_cfg, outfile, indent=4, sort_keys=True)
     
def createModelConfig(model):
    # create basic config
    model_cfg = hls4ml.utils.config_from_keras_model(model, granularity='model')
    with open(model.name+'_model_cfg.json','w') as outfile:
        json.dump(model_cfg, outfile, indent=4, sort_keys=True)
    
if __name__ == "__main__":
    createProjectConfig()