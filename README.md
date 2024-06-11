# Kubeflow_pipline_module
Kubeflow_pipline_module, use docker as base component.

# Development mode
Prepare a full-fledged image file with fully functional python scripts inside. Every time docker starts, the python script starts.

# Sketch
Comming soon

# Update
### 2024/06/11
Add pv and pvc for local path test, and update readme.

# Example
```python
# 导入kfp（Kubeflow Pipelines）库，用于创建和管理机器学习工作流
import kfp
from kfp import dsl

# 定义一个函数，创建一个执行CellRanger Count命令的操作
def cellranger_count_op(fastq_dir, sample_name, transcriptome, output_dir):
    # 创建一个PipelineVolume对象，指定PVC（Persistent Volume Claim）的名称
    volume = dsl.PipelineVolume(pvc="hostpath-pvc")
    
    # 返回一个ContainerOp对象，表示一个容器操作
    return dsl.ContainerOp(
        name='CellRanger Count',  # 给这个操作起一个名字
        image='nfcore/cellranger:7.2.0',  # 指定要使用的Docker镜像
        command=['cellranger', 'count'],  # 指定要在容器中运行的命令
        arguments=[
            "--id={}".format(sample_name),  # 样本ID
            "--transcriptome={}".format(transcriptome),  # 转录组的路径
            "--fastqs={}".format(fastq_dir),  # FASTQ文件的目录
            "--localcores=8",  # 分配给该任务的CPU核心数
            "--localmem=64",  # 分配给该任务的内存大小（GB）
            "--output-dir={}".format(output_dir)  # 输出目录
        ],
        # 使用PipelineVolume对象来挂载PVC到容器的指定路径
        pvolumes={"/home/sunhao": volume}
    )

# 定义一个pipeline（工作流），这个工作流包含多个任务
@dsl.pipeline(
    name='CellRanger Analysis Pipeline',  # 工作流的名称
    description='Pipeline to process single-cell data using CellRanger'  # 工作流的描述
)
def cellranger_pipeline(fastq_dir: str, sample_name: str, transcriptome: str, output_dir: str):
    # 在工作流中添加一个任务，调用cellranger_count_op函数
    cellranger_count_task = cellranger_count_op(fastq_dir, sample_name, transcriptome, output_dir)

# 当这个脚本作为主程序运行时，编译工作流，并生成一个yaml文件
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(cellranger_pipeline, 'cellranger_pipeline.yaml')
```


# Useage
- cellranger
```bash
kfp run --experiment my-experiment --pipeline-file cellranger_pipeline.yaml \
        --parameter fastq_dir=/home/localpath \
        --parameter sample_name=sample123 \
        --parameter transcriptome=/home/localpath \
        --parameter output_dir=/home/localpath
```
