# OD_ComplexYOLO_2-Stage_FasterRCNN

**FasterRCNN - ComplexYOLO track - training and test evaluation**

Part of the *Physical AI Object Detection* reference series of the **Statera Working Group**:
one algorithm and one task per repository, the same data, protocol and metrics for every algorithm -
only the algorithm differs.

## Model

- Paper: Ren, He, Girshick & Sun, *Faster R-CNN*, NeurIPS 2015 (arXiv:1506.01497); FPN: Lin et al., CVPR 2017
- Implementation source: torchvision fasterrcnn_resnet50_fpn components (official-equivalent of the Caffe / Detectron code)
- Parameters: 41.37 M (3 classes)

- ResNet-50 + FPN P2-P6
- RPN: 3 ratios per level, IoU 0.7 / 0.3
- RoIAlign 7 x 7 -> 2 x FC 1024 -> class + class-specific box

Detection layer / assignment / loss: Faster R-CNN with a rotated-box RoI branch (R2CNN-style): RPN on the axis-aligned box enclosing each rotated GT, RoI head regresses x, y, w, l (+ z, h) and (im, re); outputs in the Complex-YOLO / YOLO3D row layout

Differences from the original (common protocol):

- No ImageNet weights, trainable BN + PreciseBN, common init, no mean / std, no resizing (608 input), Adam 1e-4, common post-processing
- KITTI: Adam 1e-4 instead of the KITTI protocol 1e-3 (loss diverged repeatedly at 1e-3)

## Data: KITTI_5k (LiDAR bird's-eye-view, 3 classes)

5,000 KITTI object frames with LiDAR, split into train / test by the fixed list in `data_splits/KITTI_5k/`; classes Car, Pedestrian, Cyclist; 608 x 608 BEV maps.

The KITTI data must be obtained from http://www.cvlibs.net/datasets/kitti/ under its own license.

## Results

Test set: KITTI_5k test (2,470 frames), IoU 0.5, after 10 epochs (0.9 h on an RTX 4070 Laptop GPU).

| AP50 | mean | Car | Pedestrian | Cyclist |
| --- | --- | --- | --- | --- |
| BEV | **0.6642** | 0.8931 | 0.5888 | 0.5108 |
| 3D | **0.4246** | 0.6978 | 0.4286 | 0.1473 |

Complex-YOLO does not regress z / h (paper); the 3D AP uses fixed class heights.

Protocol: 10 epochs, Adam lr 1e-4 (constant), effective batch 8 (micro batch 2 x 4 accumulation), BEV 608, seed 777, no pretraining; point-cloud augmentation of the Legacy code.

## Usage

```bash
pip install -r requirements.txt
python data_processing_complex.py   # extracts KITTI_5k (see the script header for the source zip)
python train_complex_faster_rcnn.py               # training, then test evaluation (runs/complex_faster_rcnn/)
python evaluate_complex_faster_rcnn.py            # test evaluation of runs/complex_faster_rcnn/checkpoints/ (or --weights <file>)
```

Data are expected under `$PHYSICAL_AI_ROOT/datasets` (default `~/Physical_AI/datasets`).
Smoke test: `python train_complex_faster_rcnn.py --epochs 1 --max-train 8 --max-test 4`.

Trained weights: the GitHub Release of this repository contains `complex_faster_rcnn_kitti5k_e010.pth` (the run reported above).
Put it into `runs/complex_faster_rcnn/checkpoints/` or pass `--weights <file>` to the evaluation script.
Demo scripts using these weights will be added in a later release.

## Files

```
data_processing_*.py      step 1  data
train_complex_faster_rcnn.py         step 2  training + test evaluation
evaluate_complex_faster_rcnn.py      step 3  test evaluation
common/                   protocol (config), data loading, trainer, metrics, utilities
tasks/                    task definition (data sets, post-processing, evaluation)
detectors/                FasterRCNN (faster_rcnn, anchor_free)
THIRD_PARTY.md            sources and licenses of the reused code
```

Licenses: see `THIRD_PARTY.md`.

## Global Collaboration

Hills Robotics is currently participating in multiple projects in Korea and internationally.

We are actively interested in building relationships with organizations that can complement our technology with global sales networks, distribution channels, system integration capabilities, manufacturing ecosystems, AI infrastructure, robotics technologies, research capabilities, or strategic investment.

Several technology and business collaborations are already underway. Some partners, projects, system architectures, and commercial programs cannot be publicly disclosed because they are subject to confidentiality and business agreements.

We believe that the emerging Physical AI ecosystem cannot be built by a single company.
It requires a global network connecting robotics companies, AI researchers, semiconductor and computing companies, sensor manufacturers, software developers, universities, system integrators, industrial customers, investors, and global distribution partners.

We have now begun our serious exploration of the Physical AI frontier, and we welcome connections with people and organizations who want to build this ecosystem together.

## Research, Contribution, and Donation

The repositories of the Statera Working Group are intended to contribute to the broader technical discussion around Physical AI.

Researchers, engineers, developers, companies, universities, and independent contributors interested in these subjects are welcome to connect with us.

If you would like to collaborate on Physical AI or autonomous robotics, participate in research or technology development, discuss international business cooperation, propose technology or platform integration, contribute technical knowledge, or support this GitHub knowledge initiative through sponsorship or donation, please contact us.

## Contact

**Richard Minsoo Go**
Head of AI, Hills Robotics
Statera Working Group

Personal / Research Contact:
[gominsoo888@gmail.com](mailto:gominsoo888@gmail.com)

Hills Robotics / Business Contact:
[minsoo.go@hillslogis.com](mailto:minsoo.go@hillslogis.com)

Hills Robotics:
https://hillslogis.com/

For inquiries regarding next-generation outdoor autonomous robotic platforms, Physical AI Spider Grid, Intelligence Cabinet, Edge AI, or On-Premise AI architectures that are not yet publicly presented on the company website, please contact us directly.
