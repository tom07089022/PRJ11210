import keras
import numpy as np
from iottalk import DAI, DAN

class Phonefocus:
    
    def __init__(self):
        self.md = keras.models.load_model('./models/Model_4types_IOT_LSTM.h5')
        self.olddata = []
        self.newdata = []
        DAI.register_to_iottalk()
    
    def preparefordata(self):
        while True:
            if (len(self.olddata) < 30):
                self.olddata = DAI.dai(self.olddata)
            else:
                self.newdata = np.array(self.olddata)
                self.newdata = self.newdata.reshape(1,30,1)
                break
    
    def axispredict(self):
        result = self.md.predict_classes(self.newdata)
        result = int(result)
        del self.olddata[0]
        del self.olddata[1]
        del self.olddata[2]
        self.olddata = DAI.dai(self.olddata)
        self.newdata = np.array(self.olddata)
        self.newdata = self.newdata.reshape(1,30,1)
        return result