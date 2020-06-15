import numpy as np

import suanpan
from suanpan.app import app
from suanpan.app.arguments import Bool, Float, Int, Json, String
from suanpan.log import logger

images = app.modules.enable("images")


@app.title("测试标题")
@app.param(String(key="param1", default="1", label="String Param 1"))
@app.param(Int(key="param2", default=255, label="Int Param 2", step=20))
@app.param(Float(key="param3", default=3.0, label="Float Param 3"))
@app.param(Bool(key="param4", default=True, label="Bool Param 4"))
@app.param(Json(key="param5", default={"test": "json"}, label="Json Param 5"))
def testCall(context):
    args = context.args
    inImage = np.ones((100, 200), dtype=np.uint8) * args.param2
    # 保存处理前图片并触发前端更新
    images.saveDebugImageAndNotify(inImage, itype="input")

    # 自定义机器视觉处理代码
    logger.info(f"Call Custom CV function")
    outImage = inImage / 2

    # 保存处理后图片并触发前端更新
    images.saveDebugImageAndNotify(outImage, itype="output")


if __name__ == "__main__":
    suanpan.run(app)
