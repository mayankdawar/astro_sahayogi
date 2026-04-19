"""Ayanamsa strategy: configures Swiss Ephemeris sidereal mode."""
from __future__ import annotations
from abc import ABC, abstractmethod
import swisseph as swe

from astro_sahayogi.data.constants import (
    AYANAMSA_LAHIRI, AYANAMSA_RAMAN, AYANAMSA_FAGAN,
    AYANAMSA_KP_NEW, AYANAMSA_KP, AYANAMSA_WESTERN,
)


class AyanamsaStrategy(ABC):
    @abstractmethod
    def apply(self) -> None: ...

    @abstractmethod
    def is_sidereal(self) -> bool: ...


class LahiriAyanamsa(AyanamsaStrategy):
    def apply(self):
        swe.set_sid_mode(swe.SIDM_LAHIRI)

    def is_sidereal(self) -> bool:
        return True


class RamanAyanamsa(AyanamsaStrategy):
    def apply(self):
        swe.set_sid_mode(swe.SIDM_RAMAN)

    def is_sidereal(self) -> bool:
        return True


class FaganAyanamsa(AyanamsaStrategy):
    def apply(self):
        swe.set_sid_mode(swe.SIDM_FAGAN_BRADLEY)

    def is_sidereal(self) -> bool:
        return True


class KPNewAyanamsa(AyanamsaStrategy):
    def apply(self):
        try:
            swe.set_sid_mode(swe.SIDM_KRISHNAMURTI_VP291)
        except AttributeError:
            swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)

    def is_sidereal(self) -> bool:
        return True


class KPAyanamsa(AyanamsaStrategy):
    def apply(self):
        swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)

    def is_sidereal(self) -> bool:
        return True


class WesternAyanamsa(AyanamsaStrategy):
    def apply(self):
        pass  # No sidereal mode for tropical

    def is_sidereal(self) -> bool:
        return False


AYANAMSA_STRATEGIES: dict[str, AyanamsaStrategy] = {
    AYANAMSA_LAHIRI: LahiriAyanamsa(),
    AYANAMSA_RAMAN: RamanAyanamsa(),
    AYANAMSA_FAGAN: FaganAyanamsa(),
    AYANAMSA_KP_NEW: KPNewAyanamsa(),
    AYANAMSA_KP: KPAyanamsa(),
    AYANAMSA_WESTERN: WesternAyanamsa(),
}


def apply_ayanamsa(name: str) -> AyanamsaStrategy:
    strategy = AYANAMSA_STRATEGIES.get(name, KPAyanamsa())
    strategy.apply()
    return strategy
