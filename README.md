# Kubeflow_pipline_module
Kubeflow_pipline_module, use docker as base component.
# CONTENT
- [Development mode](https://github.com/OOAAHH/Kubeflow_pipline_module/edit/main/README.md#development-mode)
- [Sketch](https://github.com/OOAAHH/Kubeflow_pipline_module/edit/main/README.md#sketch)
- [Update](https://github.com/OOAAHH/Kubeflow_pipline_module/edit/main/README.md#Update)
- [Example](https://github.com/OOAAHH/Kubeflow_pipline_module/edit/main/README.md#example)
- [Useage](https://github.com/OOAAHH/Kubeflow_pipline_module/edit/main/README.md#useage)

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


# Attachment
First prepare your image file: [example](https://github.com/v-wan/k3d-gpu)

### Docker images
```bash
who@oem:~$ docker images
REPOSITORY                         TAG                 IMAGE ID       CREATED        SIZE
vlatitude/k3d-gpu/rancher/k3s      v1.26.4-k3s1-cuda   5ebcdf68ea83   5 days ago     533MB
ghcr.io/k3d-io/k3d-tools           5.6.3               3e61fe13415d   2 months ago   20.2MB
ghcr.io/k3d-io/k3d-proxy           5.6.3               2f9ac4724f73   2 months ago   61.2MB
```
### Installation dependency
We use [k3d](https://k3d.io/v5.6.3/) as k8s foundation.

### Create you cluster
#### Create you cluster
```bash
k3d cluster create "kubeflow" \
  --image "vlatitude/k3d-gpu/rancher/k3s:v1.26.4-k3s1-cuda" \
  --gpus all
```
#### Install NVDIA gpu support
```bash
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.15.0/deployments/static/nvidia-device-plugin.yml
```
or You could test with this pods:
```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod
spec:
  restartPolicy: Never
  containers:
    - name: cuda-container
      image: nvcr.io/nvidia/k8s/cuda-sample:vectoradd-cuda10.2
      resources:
        limits:
          nvidia.com/gpu: 1 # requesting 1 GPU
  tolerations:
  - key: nvidia.com/gpu
    operator: Exists
    effect: NoSchedule
EOF
```

### Deploy the kubeflow
```bash
git clone -b https://github.com/kubeflow/manifests
```
#### You can choose the version you like
```bash
git checkout v1.7.0
```
#### You can install all Kubeflow official components (residing under apps) and all common services (residing under common) using the following command:
- Be aware of **kustomize** compatibility issues

```bash
while ! kustomize build example | kubectl apply -f -; do echo "Retrying to apply resources"; sleep 20; done
```
Wait for all pods to run successfully
[_Attatchment/Screenshot 2024-06-06 at 17.11.13.png](https://github.com/OOAAHH/Kubeflow_pipline_module/blob/main/_Attatchment/Screenshot%202024-06-06%20at%2017.11.13.png)

**Kubeflow Start!!!**
```bash
kubectl port-forward svc/istio-ingressgateway -n istio-system 12345:80
```
