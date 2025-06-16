# /// script
# dependencies = ["pymhf==0.1.11.dev27"]
#
# [tool.uv.sources]
# pymhf = { index = "pypi_test" }
#
# [[tool.uv.index]]
# name = "pypi_test"
# url = "https://test.pypi.org/simple/"
# explicit = true
# 
# [tool.pymhf]
# exe = "NMS.exe"
# steam_gameid = 275850
# start_paused = false
# 
# [tool.pymhf.logging]
# log_dir = "."
# log_level = "info"
# window_name_override = "NMS TrueGear mod"
# ///



import threading
import ctypes
from typing import Annotated, Optional
import time
from logging import getLogger

from pymhf import Mod, load_mod_file, FUNCDEF
from pymhf.core.memutils import get_addressof
from pymhf.core.hooking import static_function_hook
from pymhf.core.hooking import function_hook, Structure
from pymhf.core.memutils import map_struct, get_addressof
from pymhf.utils.partial_struct import partial_struct, Field
from pymhf.extensions.cpptypes import std
from pymhf.core.utils import set_main_window_active
from pymhf.gui.decorators import gui_button
from truegear import TruegearPlayerClient


logger = getLogger("truegearmod")
###########################################
class cTkVector4f(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float),
        ("w", ctypes.c_float),
    ]

###########################################
@partial_struct
class TkAudioID(ctypes.Structure):
    mpacName: Annotated[Optional[str], Field(ctypes.c_char_p)]
    muID: Annotated[int, Field(ctypes.c_uint32)]
    mbValid: Annotated[bool, Field(ctypes.c_bool)]
###########################################
class cGcPlayer(Structure):
    @function_hook("48 8B C4 48 89 58 ?? 4C 89 48 ?? 44 89 40 ?? 55 56 57 41 54 41 55 41 56 41 57 48 8D A8")
    def TakeDamage(self, this: ctypes.c_uint64,damageAmount:ctypes.c_float, damageType:ctypes.c_uint32, damageId:ctypes.c_char_p, dir_:ctypes.POINTER(cTkVector4f), owner:ctypes.c_ulonglong, effectsDamageMultipliers:ctypes.c_ulonglong):
        pass

    @function_hook("40 53 48 81 EC E0 00 00 00 48 8B D9 E8 ?? ?? ?? ?? 83 78 10 05")
    def OnEnteredCockpit(self, this: ctypes.c_uint64):
        pass

    @function_hook("40 53 48 83 EC 20 48 8B 1D ?? ?? ?? ?? E8 ?? ?? ?? ?? 83 78 10 05 75 ?? 48 8B")
    def GetDominantHand(self, this: ctypes.c_uint64 ,_result_:ctypes.c_int64) -> ctypes.c_int64:
        pass
###########################################
class cTkAudioManager(Structure):
    @function_hook("48 83 EC ? 33 C9 4C 8B D2 89 4C 24 ? 49 8B C0 48 89 4C 24 ? 45 33 C9")
    def Play(
        self,
        this: ctypes.c_ulonglong,
        event: ctypes.c_ulonglong,
        object: ctypes.c_int64,
    ) -> ctypes.c_bool:
        pass
###########################################
class cGcLaserBeam(Structure):
    @function_hook("48 89 5C 24 10 57 48 83 EC 50 48 83 B9")
    def Fire(self, this: ctypes.c_uint64):
        pass
###########################################
class cGcTerrainEditorBeam(Structure):
    @function_hook("48 8B C4 48 89 58 18 48 89 70 20 55 57 41 54 41 55 41 57 48 8D A8 ?? ?? FF FF")
    def Fire(self, this: ctypes.c_uint64):
        pass  

    @function_hook("48 8B C4 48 89 58 10 48 89 70 18 55 57 41 56 48 8D 68 A1 48 81 EC ?? 00 00 00 8B")
    def StartEffect(self, this: ctypes.c_uint64):
        pass  

    @function_hook("4C 89 44 24 18 55 53 56 57 41 54 41 55 41 56 48 8D AC 24 ?? FE FF FF 48")
    def ApplyTerrainEditStroke(self, this: ctypes.c_uint64):
        pass  

    @function_hook("48 8B C4 4C 89 40 18 48 89 48 08 55 53 56 57 41 56 41 57 48 8D A8")
    def ApplyTerrainEditFlatten(self, this: ctypes.c_uint64):
        pass  
###########################################
class cGcNetworkWeapon(Structure):
    @function_hook("40 53 41 56 41 57 48 81 EC E0 00 00 00 8D 41 ?? 4D 8B D1")
    def FireRemote(self, this: ctypes.c_uint64):
        pass  
###########################################
class cGcLocalPlayerCharacterInterface(Structure):
    @function_hook("40 53 48 83 EC 20 48 8B 1D ?? ?? ?? ?? 48 8D 8B ?? ?? ?? 00 E8 ?? ?? ?? 00")
    def IsJetpacking(self, this: ctypes.c_uint64,result: ctypes.c_ubyte,_result_:ctypes.c_ubyte) ->  ctypes.c_ubyte:
        pass  
###########################################
class cGcSpaceshipComponent(Structure):
    @function_hook("48 89 5C 24 18 48 89 54 24 10 57 48 83 EC 70 41 0F B6 F8")
    def Eject(self, this: ctypes.c_uint64):
        pass  
###########################################
class cGcSpaceshipWarp(Structure):
    @function_hook("48 83 EC 38 48 8B 0D ?? ?? ?? ?? 41 B9 01 00 00 00 48 81 C1 30 B3 00 00 C7 44 24 20 FF FF FF FF BA 9A")
    def GetPulseDriveFuelFactor(self, this: ctypes.c_uint64,_result_:ctypes.c_float) -> ctypes.c_float:
        pass
###########################################
class cGcSpaceshipWeapons(Structure):
    @function_hook("48 63 81 ?? ?? 00 00 80 BC 08 ?? ?? 00 00 00 74 12")
    def GetOverheatProgress(self, this: ctypes.c_uint64,_result_:ctypes.c_float) -> ctypes.c_float:
        pass 

    @function_hook("48 89 5C 24 08 57 48 83 EC 20 48 8B D9 48 8B 49 08 48 8B 01 FF 90 90 01 00 00 84 C0 0F 85 88 00 00 00")
    def GetCurrentShootPoints(self, this: ctypes.c_uint64):
        pass
##########################################
class cGcPlayerCharacterComponent(Structure):
    @function_hook("48 8B C4 55 53 56 57 41 56 48 8D 68 A1 48 81 EC 90 00 00")
    def SetDeathState(self, this: ctypes.c_uint64):
        pass
###########################################
class TimerController:
    def __init__(self,true_gear_mod_instance):
        self.pistol_laser_interval = 0.07
        self.pistol_laser_running = False
        self.pistol_laser_thread = None
        self.pistol_laser_lock = threading.Lock()

        self.scan_interval = 0.1  # 100ms
        self.scan_running = False
        self.scan_thread = None
        self.scan_lock = threading.Lock()

        self.spacejump_interval = 1  # 100ms
        self.spacejump_running = False
        self.spacejump_thread = None
        self.spacejump_lock = threading.Lock()

        self.true_gear_mod = true_gear_mod_instance
    
    def _pistol_laser_worker(self):
        while True:
            with self.pistol_laser_lock:
                if not self.pistol_laser_running:
                    break
            if self.true_gear_mod.get_player_hand() == 0:
                # logger.info("RightHandPistolLaserShoot")
                _ws.send_play("RightHandPistolLaserShoot")
            else:
                # logger.info("LeftHandPistolLaserShoot")
                _ws.send_play("LeftHandPistolLaserShoot")
            time.sleep(self.pistol_laser_interval)
    
    def start_pistol_laser(self):
        with self.pistol_laser_lock:
            if self.pistol_laser_running:
                return
            self.pistol_laser_running = True
        
        self.pistol_laser_thread = threading.Thread(target=self._pistol_laser_worker, daemon=True,name="PistolLaserTimer")
        self.pistol_laser_thread.start()
    
    def stop_pistol_laser(self):
        with self.pistol_laser_lock:
            if not self.pistol_laser_running:
                return
            self.pistol_laser_running = False
        
        if self.pistol_laser_thread:
            self.pistol_laser_thread.join()

    def _scan_worker(self):
        while True:
            with self.scan_lock:
                if not self.scan_running:
                    break
            # logger.info("Scanning")
            _ws.send_play("Scanning")
            time.sleep(self.scan_interval)
    
    def start_scan(self):
        with self.scan_lock:
            if self.scan_running:
                return
            self.scan_running = True
        
        self.scan_thread = threading.Thread(target=self._scan_worker, daemon=True,name="ScanTimer")
        self.scan_thread.start()
    
    def stop_scan(self):
        with self.scan_lock:
            if not self.scan_running:
                return
            self.scan_running = False
        
        if self.scan_thread:
            self.scan_thread.join()

    def _spacejump_worker(self):
        while True:
            with self.spacejump_lock:
                if not self.spacejump_running:
                    break
            # logger.info("SpaceJump")
            _ws.send_play("SpaceshipPulse")
            time.sleep(self.spacejump_interval)
    
    def start_spacejump(self):
        with self.spacejump_lock:
            if self.spacejump_running:
                return
            self.spacejump_running = True
        
        self.spacejump_thread = threading.Thread(target=self._spacejump_worker, daemon=True,name="SpaceJumpTimer")
        self.spacejump_thread.start()
    
    def stop_spacejump(self):
        with self.spacejump_lock:
            if not self.spacejump_running:
                return
            self.spacejump_running = False
        
        if self.spacejump_thread:
            self.spacejump_thread.join()
###########################################
_ws = TruegearPlayerClient(_appId = "275850", _apiKey = "No Man's Sky")
class TrueGearMod(Mod):
    def __init__(self):
        super().__init__()
        _ws.start()
        self.isPistolLaserFire = False
        self.isInSpaceship = False
        self.isInSpaceJump = False
        self.lastFuelFactor = 1
        self.lastJetpackTime = 0
        self.lastLaserTime = 0
        self.playerHand = 0
        self.timerController = TimerController(self)
        time.sleep(5)

    def get_player_hand(self):
        return self.playerHand

    @cGcPlayerCharacterComponent.SetDeathState.after
    def SetDeathState(self, *args):
        # logger.info("PlayerDeath")
        _ws.send_play("PlayerDeath")
        # logger.info(args)

    @cGcPlayer.TakeDamage.after
    def TakeDamage(self, this, damageAmount, damageType, damageId, dir_, owner, effectsDamageMultipliers):
        direction = dir_.contents
        if damageId == "LANDING":
            # logger.info("FallDamage")
            _ws.send_play("FallDamage")
        else:
            # logger.info("DefaultDamage")
            _ws.send_play("DefaultDamage")
        # logger.info(f"damageAmount: {damageAmount},damageType :{damageType}, damageId: {damageId} , direction ({direction.x}, {direction.y}, {direction.z})")

    @cGcPlayer.OnEnteredCockpit.after
    def OnEnteredCockpit(self, *args):
        # logger.info(f"GetOnSpaceship")        
        self.isInSpaceship = True
        if not self.isInSpaceJump:
            _ws.send_play("GetOnSpaceship")
        # logger.info(args)

    @cGcPlayer.GetDominantHand.after
    def GetDominantHand(self, *args,_result_):
        self.playerHand = _result_
        # # logger.info(f"GetDominantHand")
        # # logger.info(f"Result:{_result_}")
        # # logger.info(args)

    @cTkAudioManager.Play.after
    def after_play(self, this, event, object_):
        audioID = map_struct(event, TkAudioID)
        if audioID.muID == 2149772978:
            # logger.info(f"ScanWave")
            _ws.send_play("ScanWave")
        elif audioID.muID == 2815161641:
            # logger.info(f"CollectItem")
            _ws.send_play("CollectItem")
        elif audioID.muID == 3451007219:
            if not self.isInSpaceJump:
                # logger.info(f"SpaceshipSpeedUp")
                _ws.send_play("SpaceshipSpeedUp")
        elif audioID.muID == 3903008093:
            # logger.info(f"SpaceshipOnGround")
            _ws.send_play("SpaceshipOnGround")
        elif audioID.muID == 514090887:
            # logger.info(f"SpaceshipTakeOff")
            _ws.send_play("SpaceshipTakeOff")
        elif audioID.muID == 1335995103:
            # logger.info(f"SpaceshipEnterGalaxyMap")
            _ws.send_play("SpaceshipSpeedUp")
        elif audioID.muID == 1261594536:
            # logger.info(f"StartSpaceJump")
            self.isInSpaceJump = True
            self.timerController.start_spacejump()
        elif audioID.muID == 1511168854 or audioID.muID == 2852869421:
            # logger.info(f"StopSpaceJump")
            self.isInSpaceJump = False
            self.timerController.stop_spacejump()
        elif audioID.muID == 2223503391 or audioID.muID == 3201991932 or audioID.muID == 3141878185:
            # logger.info(f"StartPistolLaser")
            self.isPistolLaserFire = True
            self.timerController.start_pistol_laser()
        elif audioID.muID == 2191565963 or audioID.muID == 867290390 or audioID.muID == 2852869421:
            # logger.info(f"StopPistolLaser")
            self.isPistolLaserFire = False
            self.timerController.stop_pistol_laser()
        elif audioID.muID == 3315033225:
            # logger.info(f"StartScan")
            self.timerController.start_scan()
        elif audioID.muID == 290149060 or audioID.muID == 2852869421:
            # logger.info(f"StopScan")
            self.timerController.stop_scan()

    @cGcNetworkWeapon.FireRemote.after
    def FireRemote(self, *args):
        if self.isPistolLaserFire:
            return
        if self.isInSpaceship:
            # logger.info("SpaceshipWeaponShoot")
            _ws.send_play("SpaceshipWeaponShoot")
        else:
            if self.playerHand == 0:
                # logger.info("RightHandPistolShoot")
                _ws.send_play("RightHandPistolShoot")
            else:
                # logger.info("LeftHandPistolShoot")
                _ws.send_play("LeftHandPistolShoot")

    @cGcLocalPlayerCharacterInterface.IsJetpacking.after
    def IsJetpacking(self,result, *args,_result_):
        if _result_ == 1:
            if time.perf_counter() - self.lastJetpackTime > 0.1:
                self.lastJetpackTime = time.perf_counter()
                # logger.info("PlayerUsingJetpack")
                _ws.send_play("PlayerUsingJetpack")
        # # logger.info(f"-----------------------------------------------")
        # # logger.info(f"cGcLocalPlayerCharacterInterface::IsJetpacking")
        # # logger.info(f"Result:{_result_}")
        # # # logger.info(f"cGcLocalPlayerCharacterInterface::IsJetpacking")
        # # logger.info(args)
        
    @cGcSpaceshipComponent.Eject.after
    def Eject(self, *args):
        # logger.info(f"GetOffSpaceship")
        self.isInSpaceship = False
        _ws.send_play("GetOffSpaceship")
        # logger.info(args)
    
    @cGcSpaceshipWarp.GetPulseDriveFuelFactor.after
    def GetPulseDriveFuelFactor(self,this, *args,_result_):
        if _result_ > self.lastFuelFactor:
            # logger.info(f"PulseEngineHealing")
            # _ws.send_play("PulseEngineHealing")
            self.lastFuelFactor = _result_
            return
        if self.lastFuelFactor != _result_:
            if self.lastFuelFactor == 1 and _result_ < 0.95:
                self.lastFuelFactor = _result_
                return
            self.lastFuelFactor = _result_
            # logger.info(f"SpaceshipPulse")
            _ws.send_play("SpaceshipPulse")
            # logger.info(f"Result:{_result_}")
            # logger.info(args)


if __name__ == "__main__":
    load_mod_file(__file__)