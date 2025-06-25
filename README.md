# HWComponents-Cacti

This estimator connects CACTI to the HWComponents. It provides estimators for SRAM,
DRAM, and caches. This is adapted from the Accelergy CACTI plug-in.

## Installation
Clone the repository and install with pip:

```bash
git clone --recurse-submodules https://github.com/Accelergy-Project/hwcomponents-cacti.git
cd hwcomponents-cacti
make build
pip3 install .

# Check that the installation is successful
hwc --list | grep SRAM
hwc --list | grep DRAM
hwc --list | grep Cache
```

## Citation

If you use this library in your work, please cite the following:

```bibtex
@misc{andrulis2024modelinganalogdigitalconverterenergyarea,
  title={Modeling Analog-Digital-Converter Energy and Area for Compute-In-Memory Accelerator Design}, 
  author={Tanner Andrulis and Ruicong Chen and Hae-Seung Lee and Joel S. Emer and Vivienne Sze},
  year={2024},
  eprint={2404.06553},
  archivePrefix={arXiv},
  primaryClass={cs.AR},
  url={https://arxiv.org/abs/2404.06553}, 
}
@inproceedings{accelergy,
  author      = {Wu, Yannan Nellie and Emer, Joel S and Sze, Vivienne},
  booktitle   = {2019 IEEE/ACM International Conference on Computer-Aided Design (ICCAD)},
  title       = {Accelergy: An architecture-level energy estimation methodology for accelerator designs},
  year        = {2019},
}
@article{shivakumar2001cacti,
  title={Cacti 3.0: An integrated cache timing, power, and area model},
  author={Shivakumar, Premkishore and Jouppi, Norman P},
  year={2001},
  publisher={Technical Report 2001/2, Compaq Computer Corporation}
}
@ARTICLE{wilton1996cacti,
  title={CACTI: an enhanced cache access and cycle time model}, 
  author={Wilton, S.J.E. and Jouppi, N.P.},
  journal={IEEE Journal of Solid-State Circuits}, 
  year={1996},
  volume={31},
  number={5},
  pages={677-688},
  keywords={Driver circuits;Costs;Decoding;Analytical models;Stacking;Delay estimation;Computer architecture;Equations;Councils;Wiring},
  doi={10.1109/4.509850}
}
@article{balasubramonian2017cacti,
  author = {Balasubramonian, Rajeev and Kahng, Andrew B. and Muralimanohar, Naveen and Shafiee, Ali and Srinivas, Vaishnav},
  title = {CACTI 7: New Tools for Interconnect Exploration in Innovative Off-Chip Memories},
  year = {2017},
  issue_date = {June 2017},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  volume = {14},
  number = {2},
  issn = {1544-3566},
  url = {https://doi.org/10.1145/3085572},
  doi = {10.1145/3085572},
  journal = {ACM Trans. Archit. Code Optim.},
  month = jun,
  articleno = {14},
  numpages = {25},
  keywords = {DRAM, Memory, NVM, interconnects, tools}
}
```