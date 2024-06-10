import kfp
from kfp import dsl

def cellranger_count_op(fastq_dir, sample_name, transcriptome):
    return dsl.ContainerOp(
        name='CellRanger Count',
        image='nfcore/cellranger:7.2.0',  # 使用你的 CellRanger 镜像
        command=['cellranger', 'count'],  # 明确指定命令
        arguments=[
            "cellranger", "count",
            "--id={}".format(sample_name),
            "--transcriptome={}".format(transcriptome),
            "--fastqs={}".format(fastq_dir),
            "--localcores=8",
            "--localmem=64",
            "--output-dir={}".format(output_dir),    
        ]
    )

def process_output_op(data_path):
    return dsl.ContainerOp(
        name='Process CellRanger Output',
        image='ooaahhdocker/py39_scanpy1-10-1',  # 使用你的数据处理镜像

        import scanpy as sc
        adata = sc.read_10x_h5("~{run_id}/outs/filtered_feature_bc_matrix.h5")
        adata.write_h5ad("~{run_id}/outs/~{sample}_filtered_feature_bc_matrix.h5ad")
    )

@dsl.pipeline(
    name='Extended CellRanger Pipeline',
    description='A pipeline that includes CellRanger count and post-processing.'
)
def extended_cellranger_pipeline(
    fastq_dir='/home/sunhao/fastq/',
    sample_name='sample',
    transcriptome='/home/sunhao/transcriptome/'
):
    # CellRanger count
    count_op = cellranger_count_op(fastq_dir, sample_name, transcriptome)

    # Process output
    process_output = process_output_op(count_op.outputs['output'])  # 假设这是 CellRanger 输出的路径

