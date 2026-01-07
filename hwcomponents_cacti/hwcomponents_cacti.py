from abc import abstractmethod
from logging import Logger
import math
import glob
import csv
import os
import subprocess
import tempfile
from typing import Callable, Optional, Union
from hwcomponents import ComponentModel, action
import csv
import hashlib


def _clean_tmp_dir():
    temp_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "cacti_inputs_outputs"
    )
    os.makedirs(temp_dir, exist_ok=True)
    # If there's more than 200 files in the directory, remove the oldest ones
    files = sorted(glob.glob(temp_dir), key=os.path.getctime, reverse=True)
    if len(files) > 200:
        for file in files[200:]:
            os.remove(file)
    return temp_dir


def _get_cacti_dir(logger: Logger) -> str:
    for to_try in ["cacti/cacti", "cacti"]:
        p = os.path.join(os.path.dirname(__file__), to_try)
        if os.path.exists(p) and os.path.isfile(p):
            return os.path.dirname(os.path.abspath(p))
    raise FileNotFoundError("CACTI executable not found")


class DRAM(ComponentModel):
    """

    DRAM model using a simple joules-per-bit energy. Assumes that leak power and area
    are both zero.

    Args:
        width: The width of the DRAM bus in bits.
        type: The type of DRAM. Must be one of the following:
            - LPDDR4
            - LPDDR
            - DDR3
            - GDDR5
            - HBM2
            - HMC

    Attributes:
        width: The width of the DRAM bus in bits.
        type: The type of DRAM.
    """

    component_name = ["DRAM", "dram"]
    priority = 0.3
    type2energy = {
        "LPDDR4": 8,  # Public data
        "LPDDR": 40,  # Malladi et al., ISCA'12
        "DDR3": 70,  # Chatterjee et al., MICRO'17
        "GDDR5": 14,
        "HBM2": 3.9,
        "HMC": 4.2,  # https://dl.acm.org/doi/10.1145/3093336.3037702
    }

    def __init__(self, width: int, type: str = "LPDDR4"):
        super().__init__(area=0, leak_power=0)
        assert (
            type in self.type2energy
        ), f"DRAM type {type} is not supported. Must be one of {list(self.type2energy.keys())}."
        self.type = type
        self.width = _assert_int(width, "width")

    @action(bits_per_action="width")
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one DRAM read.

        Args:
            bits_per_action: The number of bits to read.

        Returns:
            (energy, latency): Tuple in (Joules, seconds).
        """
        return self.type2energy[self.type] * 1e-12 * self.width, 0.0

    @action(bits_per_action="width")
    def write(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one DRAM write.

        Args:
            bits_per_action: The number of bits to write.

        Returns:
            (energy, latency): Tuple in (Joules, seconds).
        """
        return self.read()


class LPDDR4(DRAM):
    """
    LPDDR4 DRAM model using a simple joules-per-bit energy. Assumes that leak power and
    area are both zero.

    Parameters
    ----------
    width: int
        The width of the DRAM bus in bits.

    Attributes
    ----------
    width: int
        The width of the DRAM bus in bits.
    type: str
        The type of DRAM.

    """

    component_name = ["LPDDR4", "lpddr4"]
    priority = 0.3

    def __init__(self, width: int):
        super().__init__(width, type="LPDDR4")


class LPDDR(DRAM):
    """
    LPDDR DRAM model using a simple joules-per-bit energy. Assumes that leak power and
    area are both zero.

    Parameters
    ----------
    width: int
        The width of the DRAM bus in bits.

    Attributes
    ----------
    width: int
        The width of the DRAM bus in bits.
    type: str
        The type of DRAM.
    """

    component_name = ["LPDDR", "lpddr"]
    priority = 0.3

    def __init__(self, width: int):
        super().__init__(width, type="LPDDR")


class DDR3(DRAM):
    """
    DDR3 DRAM model using a simple joules-per-bit energy. Assumes that leak power and
    area are both zero.

    Parameters
    ----------
    width: int
        The width of the DRAM bus in bits.

    Attributes
    ----------
    width: int
        The width of the DRAM bus in bits.
    type: str
        The type of DRAM.
    """

    component_name = ["DDR3", "ddr3"]
    priority = 0.3

    def __init__(self, width: int):
        super().__init__(width, type="DDR3")


class GDDR5(DRAM):
    """
    GDDR5 DRAM model using a simple joules-per-bit energy. Assumes that leak power and
    area are both zero.

    Parameters
    ----------
    width: int
        The width of the DRAM bus in bits.

    Attributes
    ----------
    width: int
        The width of the DRAM bus in bits.
    type: str
        The type of DRAM.
    """

    component_name = ["GDDR5", "gddr5"]
    priority = 0.3

    def __init__(self, width: int):
        super().__init__(width, type="GDDR5")


class HBM2(DRAM):
    """
    HBM2 DRAM model using a simple joules-per-bit energy. Assumes that leak power and
    area are both zero.

    Parameters
    ----------
    width: int
        The width of the DRAM bus in bits.

    Attributes
    ----------
    width: int
        The width of the DRAM bus in bits.
    type: str
        The type of DRAM.
    """

    component_name = ["HBM2", "hbm2"]
    priority = 0.3

    def __init__(self, width: int):
        super().__init__(width, type="HBM2")


class HMC(DRAM):
    """
    HMC DRAM model using a simple joules-per-bit energy. Assumes that leak power and
    area are both zero.

    Parameters
    ----------
    width: int
        The width of the DRAM bus in bits.

    Attributes
    ----------
    width: int
        The width of the DRAM bus in bits.
    type: str
        The type of DRAM.
    """

    component_name = ["HMC", "hmc"]
    priority = 0.3

    def __init__(self, width: int):
        super().__init__(width, type="HMC")


def _assert_int(val, name: str, greater_than: int = 0):
    errstr = f"{name} must be an integer >{greater_than}. Got {val}."
    try:
        if isinstance(val, str):
            val = int(val)
        else:
            assert int(val) == val
            val = int(val)
    except Exception as e:
        val = None
    if val is None:
        raise ValueError(errstr)
    assert val > greater_than, errstr
    return val


def _interp_call(
    logger: Logger,
    param_name: str,
    callfunc: Callable,
    param: float,
    param_lo: float,
    param_hi: float,
    interp_point_calculator: Callable = None,
    **kwargs,
):
    if param_lo == param_hi:
        return callfunc(param_lo, **kwargs)
    if interp_point_calculator is not None:
        interp_point = interp_point_calculator(param, param_lo, param_hi)
    else:
        interp_point = (param - param_lo) / (param_hi - param_lo)

    logger.info(f"Interpolating {param_name} between {param_lo} and {param_hi}.")

    return tuple(
        (1 - interp_point) * l + interp_point * h
        for l, h in zip(callfunc(param_lo, **kwargs), callfunc(param_hi, **kwargs))
    )


class _Memory(ComponentModel):
    """
    Base class for all memory models.
    """

    def __init__(
        self,
        cache_type: str,
        tech_node: float,  # Must be 22-180nm
        width: int,  # Must be >=32 < CHANGES BY NUMBER OF BANKS !?!? >
        depth: int,  # Must be >=64 < CHANGES BY NUMBER OF BANKS !?!? >
        n_rw_ports: int = 1,  # Must be power of 2, >=1
        n_banks=1,  # Must be power of 2, >=1
        associativity: int = 1,  # Weird stuff with this one
        tag_size: Optional[int] = None,
    ):
        self.cache_type = cache_type
        self.width = _assert_int(width, "width")
        self.depth = _assert_int(depth, "depth")
        self.n_rw_ports = _assert_int(n_rw_ports, "n_rw_ports")
        self.n_banks = _assert_int(n_banks, "n_banks")
        self.associativity = _assert_int(associativity, "associativity")
        if self.associativity > 1:
            self.tag_size = _assert_int(tag_size, "tag_size")
        else:
            self.tag_size = 0

        self.tech_node = float(tech_node) * 1e9  # nm -> m

        self.read_energy: float = None
        self.write_energy: float = None
        self.cacti_leak_power: float = None
        self.cacti_area: float = None
        self.cycle_period: float = None
        self._called_cacti = False

        self._interpolate_and_call_cacti()
        super().__init__(self.cacti_area, self.cacti_leak_power)

    def log_bandwidth(self):
        bw = self.width * self.n_rw_ports * self.n_banks
        self.logger.info(f"Cache bandwidth: {bw/8} bytes/cycle")
        self.logger.info(f"Cache bandwidth: {bw/self.cycle_period} bits/second")

    def _interp_size(self, tech_node: float):
        # n_banks must be a power of two
        scaled_n_banks = 2 ** math.ceil(math.log2(self.n_banks))
        bankscale = self.n_banks / scaled_n_banks
        # Width must be >32, rounded to an 8
        scaled_width = max(math.ceil(self.width / 8) * 8, 32 * self.associativity)
        widthscale = self.width / scaled_width
        # Depth must be >64 * n_banks
        scaled_depth = max(self.depth, 64 * self.n_banks)
        depthscale = self.depth / scaled_depth

        (
            read_energy,
            write_energy,
            leak_power,
            area,
            cycle_period,
        ) = self._call_cacti(
            scaled_width * scaled_depth // 8,
            self.n_rw_ports,
            scaled_width // 8,
            tech_node / 1000,
            scaled_n_banks,
            self.tag_size,
            self.associativity,
        )
        # width: Area,dynamic,leakage energy scale linearly. Delay does not scale.
        # depth: Area,leakage energy scale linearly. Delay, dynamic energy scale with 1.56/2
        # n_banks: Area,leakage energy scale linearly. Delay, dynamic energy do not scale.

        # Found these empirically by testing different inputs with CACTI
        read_energy *= (widthscale * 0.7 + 0.3) * (depthscale ** (1.56 / 2))
        write_energy *= (widthscale * 0.7 + 0.3) * (depthscale ** (1.56 / 2))
        leak_power *= widthscale * depthscale
        area *= widthscale * depthscale
        cycle_period *= 1  # Dosn't scale strongly with anything
        return (
            read_energy,
            write_energy,
            leak_power,
            area,
            cycle_period,
        )

    def _interp_tech_node(self):
        supported_technologies = [22, 32, 45, 65, 90]
        # Interpolate. Below 16, interpolate energy with square root scaling (IDRS 2022),
        # area with linear scaling.
        # https://fuse.wikichip.org/news/7343/iedm-2022-did-we-just-witness-the-death-of-sram/
        if self.tech_node < min(supported_technologies) or self.tech_node > max(supported_technologies):
            scale = self.tech_node / min(supported_technologies)
            (
                read_energy,
                write_energy,
                leak_power,
                area,
                cycle_period,
            ) = self._interp_size(min(supported_technologies))
            read_energy *= scale**0.5
            write_energy *= scale**0.5
            area *= scale
            cycle_period *= scale
            # B. Parvais et al., "The device architecture dilemma for CMOS
            # technologies: Opportunities & challenges of finFET over planar
            # MOSFET," 2009 International Symposium on VLSI tech_node, Systems,
            # and Applications, Hsinchu, Taiwan, 2009, pp. 80-81, doi:
            # 10.1109/VTSA.2009.5159300.
            # finfets have approx. 21% less leakage power
            if self.tech_node < min(supported_technologies):
                leak_power *= scale**0.5 * 0.79
            return (
                read_energy,
                write_energy,
                leak_power,
                area,
                cycle_period,
            )
        # Beyond 180nm, squared scaling
        if self.tech_node > max(supported_technologies):
            return tuple(
                v * (self.tech_node / max(supported_technologies)) ** 2
                for v in self._interp_size(max(supported_technologies))
            )

        else:
            return _interp_call(
                self.logger,
                "tech_node",
                self._interp_size,
                self.tech_node,
                max(s for s in supported_technologies if s <= self.tech_node),
                min(s for s in supported_technologies if s >= self.tech_node),
            )

    def _interpolate_and_call_cacti(self):
        if self._called_cacti:
            return
        self._called_cacti = True
        if self.read_energy is not None:
            self.log_bandwidth()
            return
        (
            self.read_energy,
            self.write_energy,
            self.cacti_leak_power,
            self.cacti_area,
            self.cycle_period,
        ) = self._interp_tech_node()
        self.log_bandwidth()

    def _call_cacti(
        self,
        cache_size: int,
        n_rw_ports: int,
        block_size: int,
        tech_node_um: float,
        n_banks: int,
        tag_size: int,
        associativity: int,
    ):
        self.logger.info(
            f"Calling CACTI with {cache_size=} {n_rw_ports=} {block_size=} "
            f"{tech_node_um=} {n_banks=} {tag_size=} {associativity=}"
        )

        cfg = open(
            os.path.join(os.path.dirname(__file__), "default_cfg.cfg")
        ).readlines()
        cfg.append(
            "\n############## User-Specified Hardware Attributes ##############\n"
        )
        cfg.append(f"-size (bytes) {cache_size}\n")
        cfg.append(f"-read-write port  {n_rw_ports}\n")
        cfg.append(f"-block size (bytes) {block_size}\n")
        cfg.append(f"-technology (u) {tech_node_um}\n")
        cfg.append(f"-output/input bus width  {block_size * 8}\n")
        cfg.append(f"-UCA bank {n_banks}\n")
        cfg.append(f'-cache type "{self.cache_type}"\n')
        cfg.append(f"-tag size (b) {tag_size}\n")
        cfg.append(f"-associativity {associativity}\n")

        # Generate a unique name for the input file using Python's hash function
        temp_dir = _clean_tmp_dir()
        input_name = hashlib.sha256("".join(cfg).encode()).hexdigest()
        input_path = os.path.join(temp_dir, input_name)
        output_path = os.path.join(temp_dir, input_name + "cacti.log")
        output_path_csv = os.path.join(temp_dir, input_name + ".out")

        def read_csv_results(output_path_csv):
            with open(output_path_csv, "r") as f:
                csv_results = csv.DictReader(f.readlines())
                row = list(csv_results)[-1]
                return (
                    float(row[" Dynamic read energy (nJ)"]) * 1e-9,
                    float(row[" Dynamic write energy (nJ)"]) * 1e-9,
                    float(row[" Standby leakage per bank(mW)"]) * 1e-3 * self.n_banks,
                    float(row[" Area (mm2)"]) * 1e-6,
                    float(row[" Random cycle time (ns)"]) * 1e-9,
                )

        if os.path.exists(output_path_csv):
            try:
                return read_csv_results(output_path_csv)
            except Exception as e:
                self.logger.warning(
                    f"Error reading CACTI output file {output_path_csv}: {e}"
                )
                pass

        with open(input_path, "w") as f:
            f.write("".join(cfg))

        self.logger.info(f"Calling CACTI with input path {input_path}")
        self.logger.info(f"CACTI output will be written to {output_path}")

        cacti_dir = _get_cacti_dir(self.logger)

        exec_list = ["./cacti", "-infile", input_path]
        self.logger.info(
            f"Calling: cd {cacti_dir} ; {' '.join(exec_list)} >> {output_path} 2>&1"
        )
        result = subprocess.call(
            exec_list,
            cwd=cacti_dir,
            stdout=open(output_path, "w"),
            stderr=subprocess.STDOUT,
        )

        if result != 0 or not os.path.exists(output_path_csv):
            raise Exception(
                f"CACTI failed with exit code {result}. Please check {output_path} for CACTI output. "
                f"Run command: cd {cacti_dir} ; {' '.join(exec_list)} >> {output_path} 2>&1"
            )

        return read_csv_results(output_path_csv)


class SRAM(_Memory):
    """
    SRAM model using CACTI.

    Parameters
    ----------
        tech_node: The technology node of the SRAM in meters.
        width: The width of the read and write ports in bits. This is the number of bits
            that are accssed by any one read/write. Total size = width * depth.
        depth: The number of entries in the SRAM, each with `width` bits. Total size =
            width * depth.
        n_rw_ports: The number of read/write ports. Bandwidth will increase with more
            ports.
        n_banks: The number of banks. Bandwidth will increase with more banks.

    Attributes
    ----------
        component_name: set to "sram"
        priority: set to 0.8
        tech_node: The technology node of the SRAM in meters.
        width: The width of the read and write ports in bits. This is the number of bits
            that are accssed by any one read/write. Total size = width * depth.
        depth: The number of entries in the SRAM, each with `width` bits. Total size =
            width * depth.
        n_rw_ports: The number of read/write ports. Bandwidth will increase with more
            ports.
        n_banks: The number of banks. Bandwidth will increase with more banks.
    """

    component_name = ["SRAM", "sram"]
    priority = 0.3

    def __init__(
        self,
        tech_node: float,
        width: int,
        depth: int,
        n_rw_ports: int = 1,
        n_banks=1,
    ):
        super().__init__(
            cache_type="ram",
            tech_node=tech_node,
            width=width,
            depth=depth,
            n_rw_ports=n_rw_ports,
            n_banks=n_banks,
        )

    @action(bits_per_action="width")
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one SRAM read.

        Parameters
        ----------
        bits_per_action : int
            The number of bits to read.

        Returns
        -------
            (energy, latency): Tuple in (Joules, seconds).
        """
        self._interpolate_and_call_cacti()
        return self.read_energy, self.cycle_period

    @action(bits_per_action="width")
    def write(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one SRAM write.

        Parameters
        ----------
        bits_per_action : int
            The number of bits to write.

        Returns
        -------
            (energy, latency): Tuple in (Joules, seconds).
        """
        self._interpolate_and_call_cacti()
        return self.write_energy, self.cycle_period


class Cache(_Memory):
    """
    Cache model using CACTI.

    Parameters
    ----------
        tech_node: float
            The technology node of the cache in meters.
        width: int
            The width of the read and write ports in bits. This is the number of bits
            that are accssed by any one read/write. Total size = width * depth.
        depth: int
            The number of entries in the cache, each with `width` bits. Total size =
            width * depth.
        n_rw_ports: int
            The number of read/write ports. Bandwidth will increase with more ports.
        n_banks: int
            The number of banks. Bandwidth will increase with more banks.
        associativity: int
            The associativity of the cache. This is the number of sets in the cache.
            Bandwidth will increase with more associativity.
        tag_size: int
            The number of bits of the tag used to check for cache misses and hits.

    Attributes
    ----------
        component_name: str
            set to "cache"
        priority: float
            set to 0.8
        tech_node: float
            The technology node of the cache in meters.
        width: int
            The width of the read and write ports in bits. This is the number of bits
            that are accssed by any one read/write. Total size = width * depth.
        depth: The number of entries in the cache, each with `width` bits. Total size =
            width * depth.
        n_rw_ports: The number of read/write ports (each port supporting one read or
            one write per cycle). Bandwidth will increase with more ports.
        n_banks: The number of banks. Bandwidth will increase with more banks.
        associativity: int
            The associativity of the cache. This is the number of sets in the cache.
            Bandwidth will increase with more associativity.
        tag_size: int
            The number of bits of the tag used to check for cache misses and hits.
    """

    component_name = "cache"
    priority = 0.3

    def __init__(
        self,
        tech_node: float,
        width: int,
        depth: int,
        n_rw_ports: int = 1,
        n_banks: int = 1,
        associativity: int = 1,
        tag_size: Optional[int] = None,
    ):
        super().__init__(
            cache_type="cache",
            tech_node=tech_node,
            width=width,
            depth=depth,
            n_rw_ports=n_rw_ports,
            n_banks=n_banks,
            associativity=associativity,
            tag_size=tag_size,
        )

    @action(bits_per_action="width")
    def read(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one cache read.

        Parameters
        ----------
        bits_per_action : int
            The number of bits to read.

        Returns
        -------
            (energy, latency): Tuple in (Joules, seconds).
        """
        self._interpolate_and_call_cacti()
        return self.read_energy, self.cycle_period

    @action(bits_per_action="width")
    def write(self) -> tuple[float, float]:
        """
        Returns the energy and latency for one cache write.

        Parameters
        ----------
        bits_per_action : int
            The number of bits to write.

        Returns
        -------
            (energy, latency): Tuple in (Joules, seconds).
        """
        self._interpolate_and_call_cacti()
        return self.write_energy, self.cycle_period
