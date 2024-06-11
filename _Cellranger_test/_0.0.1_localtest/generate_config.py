import kfp
from kfp import dsl

def cellranger_count_op(fastq_dir, sample_name, transcriptome, output_dir):
    volume = dsl.PipelineVolume(pvc="hostpath-pvc")
    
    return dsl.ContainerOp(
        name='CellRanger Count',
        image='nfcore/cellranger:7.2.0', 
        command=['cellranger', 'count'],  
        arguments=[
            "--id={}".format(sample_name),
            "--transcriptome={}".format(transcriptome),
            "--fastqs={}".format(fastq_dir),
            "--localcores=8",
            "--localmem=64",
            "--output-dir={}".format(output_dir)    
        ],

        pvolumes={"/home/sunhao": volume}
    )

@dsl.pipeline(
    name='CellRanger Analysis Pipeline',
    description='Pipeline to process single-cell data using CellRanger'
)
def cellranger_pipeline(fastq_dir: str, sample_name: str, transcriptome: str, output_dir: str):
    cellranger_count_task = cellranger_count_op(fastq_dir, sample_name, transcriptome, output_dir)

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(cellranger_pipeline, 'cellranger_pipeline.yaml')
