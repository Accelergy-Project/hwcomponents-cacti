# HWComponents-Cacti

This model connects CACTI to the HWComponents. It provides models for SRAM, DRAM, and
caches. This is adapted from the Accelergy CACTI plug-in.

These models are for use with the HWComponents package, found at
https://accelergy-project.github.io/hwcomponents/.

## Installation

Install from PyPI:

```bash
pip install hwcomponents-cacti

# Check that the installation is successful
hwc --list | grep SRAM
hwc --list | grep DRAM
hwc --list | grep Cache
```

## Citation

If you use this library in your work, please cite the following:

```bibtex
@INPROCEEDINGS{cimloop,
  author={Andrulis, Tanner and Emer, Joel S. and Sze, Vivienne},
  booktitle={2024 IEEE International Symposium on Performance Analysis of Systems and Software (ISPASS)},
  title={CiMLoop: A Flexible, Accurate, and Fast Compute-In-Memory Modeling Tool},
  year={2024},
  volume={},
  number={},
  pages={10-23},
  doi={10.1109/ISPASS61541.2024.00012}
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