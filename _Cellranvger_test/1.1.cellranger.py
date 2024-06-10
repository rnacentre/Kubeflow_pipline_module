import kfp
from kfp import dsl

def cellranger_count_op(fastq_dir, sample_name, transcriptome, output_dir):
    return dsl.ContainerOp(
        name='CellRanger Count',
        image='nfcore/cellranger:7.2.0',  # 使用你的 CellRanger 镜像
        command=['cellranger', 'count'],  # 明确指定命令
        arguments=[
            "--id={}".format(sample_name),
            "--transcriptome={}".format(transcriptome),
            "--fastqs={}".format(fastq_dir),
            "--localcores=8",
            "--localmem=64",
            "--output-dir={}".format(output_dir)    
        ]
    )

@dsl.pipeline(
    name='CellRanger Analysis Pipeline',
    description='Pipeline to process single-cell data using CellRanger'
)
def cellranger_pipeline(
    fastq_dir,  # 输入文件夹路径
    sample_name,  # 样本名
    transcriptome,  # 参考基因组路径
    output_dir  # 输出文件夹路径
):
    count_op = cellranger_count_op(fastq_dir, sample_name, transcriptome, output_dir)

import kfp.compiler as compiler
compiler.Compiler().compile(cellranger_pipeline, 'cellranger_pipeline.yaml')

