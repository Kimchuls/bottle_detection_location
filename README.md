# bottle_detection_location
cv期末作业数据

iou_for_com.py ：默认学习率的图片数据处理
iou_for_lr.py ：学习率变化的图片数据处理
result-\*\*\*.txt : iou_for_com.py和iou_for_lr.py的结果
./learning_rate_exp/ : 学习率变化的图片处理数据，其中文件夹“\*\*\_x\_y”表示\*\*算法，学习率倍数为（1-5，,0.5），（1-10，,0.1），（1-20，,0.05），（5-1，,5），（10-1，,0）
./learning_rate_exp/ : 学习率变化的图片处理数据，其中文件夹命名表示“某个算法”在“某个数据集上训练”并在“某个数据集上测试”的标注文件
allfile文件夹为所有图片的总和，drawrec包含图片可视化结果，drawontxt.py为标注程序
