# bottle_detection_location
cv期末作业数据

iou_for_com.py ：默认学习率的图片数据处理\\
iou_for_lr.py ：学习率变化的图片数据处理\\
result-\*\*\*.txt : iou_for_com.py和iou_for_lr.py的结果\\
数据整合.xlsx ： 所有关于mIoU，AP，FPS的数据统计\\
\\
bottle文件夹:\\
\*\_size文件夹表示\*类型的灰度图图片\\
resharp.py程序用于将灰度图转化为RGB格式的图片，存储在新建的文件夹中\\
\*\_annotation文件夹表示\*类型图片标注文件\\
xmls.py程序用于将RGB图片用对应标注文件的数据标上矩形框，存储到新建的文件夹中\\
\\
common_exp文件夹：\\
文件夹如“FR-deploy-on-circle-to-waterdrop”命名表示“FR算法”在“圆形瓶数据集上训练”并在“水滴形瓶数据集上测试”的标注文件\\
allfile文件夹包含三种数据集中的所有图片的RGB格式\\
drawontxt.py为标注程序\\
drawrec文件夹用于存储标注后的图片\\
\\
learning_rate_exp文件夹：\\
文件夹“\*\*\_x\_y”表示\*\*算法，学习率倍数为（1-5，,0.5），（1-10，,0.1），（1-20，,0.05），（5-1，,5），（10-1，,0）\\
allfile文件夹包含三种数据集中的所有图片的RGB格式
drawontxt.py为标注程序\\
drawrec文件夹用于存储标注后的图片\\
\\
