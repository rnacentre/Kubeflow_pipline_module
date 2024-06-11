# Kubeflow_pipline_module
Kubeflow_pipline_module, use docker as base component.

# Development mode
Prepare a full-fledged image file with fully functional python scripts inside. Every time docker starts, the python script starts.

# Sketch
soon
# Update
## 2024/06/11
Add pv and pvc for local path test

# Useage
- cellranger
```bash
kfp run --experiment my-experiment --pipeline-file cellranger_pipeline.yaml \
        --parameter fastq_dir=/home/localpath \
        --parameter sample_name=sample123 \
        --parameter transcriptome=/home/localpath \
        --parameter output_dir=/home/localpath
