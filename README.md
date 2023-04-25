# yolov5DataTools  
##The tool can convert the yolov5 PyTorch txt to labelme json.  
##该工具可实现半自动标注yolov5训练集。  
##具体实现原理：  
###把yolov5推理生成的txt文件进行解析，转换成可用于labelme的json文件格式。  
##操作步骤：  
###1、创建两个文件夹，分别存放原图片和对应的txt文件。  
###2、调用generateJsonFile(img_files_path, txt_files_path, save_jsons_path)方法，传入对应的参数就可以生成json文件。  
###img_files_path是图片文件夹路径  
###txt_files_path是txt文件夹路径  
###save_jsons_path是存放json的文件夹路径  
